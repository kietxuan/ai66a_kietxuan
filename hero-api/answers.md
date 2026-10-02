# Week 9 Lab Answers

## Question 1

1. Inserting another `Avengers` team is blocked by the `UNIQUE` constraint on
   `team.name`.
2. Inserting `Ghost` with `team_id = 99` is blocked by the `FOREIGN KEY`
   constraint because team 99 does not exist.
3. Inserting a hero with only `age` is blocked by the `NOT NULL` constraint on
   `hero.name`.
4. Deleting team 1 is blocked by the `FOREIGN KEY` constraint because heroes
   still reference that team. The four statements do not exercise a primary-key
   violation because their IDs are generated automatically.

## Question 2

The foreign key belongs on `hero` because a team can have many heroes, while a
hero belongs to at most one team. The foreign key is therefore stored on the
many side of the one-to-many relationship.

## Question 3

A many-to-many relationship needs `hero`, `mission`, and a link table such as
`hero_mission_link`. The link table contains `hero_id` and `mission_id`, both
foreign keys, and uses `(hero_id, mission_id)` as its composite primary key.
That primary key prevents the same hero from being assigned to the same mission
twice.

## Question 4

Credentials should be read from an environment variable rather than written in
`database.py` because secrets would otherwise be exposed in source control.
It also lets the same code use a different database in local development,
testing, and production without changing the source code.

## Question 5

An object has no database-generated ID before it is inserted, so its ID is
typed as `int | None` and starts as `None`. After `commit()` and `refresh()`,
the database-generated integer ID is available.

## Question 6

`id`, `name`, `age`, `secret_name`, and `team_id` become columns in the
`hero` table. `team` does not become a column; it is an ORM relationship.
`back_populates` connects the two Python relationship attributes
(`Hero.team` and `Team.heroes`) so SQLModel/SQLAlchemy can navigate and keep
both sides of the relationship consistent.

## Question 7

SQLModel creates the columns, primary key, foreign key, unique index, and
regular indexes described by the model. Compared with the hand-written Part 1
table, the generated `hero` table also has `secret_name`; SQLModel creates
indexes for fields marked with `index=True`; and generated PostgreSQL SQL may
use `SERIAL`/identity details and separate index statements instead of the
exact inline syntax used by hand-written SQL.

## Question 8

`create_all()` creates only tables that do not already exist. It does not run
again for existing tables and does not alter them when a model changes.

## Question 9

The import of the model module in `main.py`, for example
`from app import models`, registers `Hero` and `Team` in `SQLModel.metadata`
before `create_all()` is called.

## Question 10

`session.add()` attaches a new object to the session but does not permanently
write it to the database. If `commit()` is removed, `refresh()` cannot refresh
the pending object into a valid persisted response, so the request normally
fails rather than returning a valid `HeroPublic` object, and no row is
durably stored. `commit()` writes the transaction, while `refresh()` reloads
database-generated values such as the ID and server defaults.

## Question 11

For a PATCH body of `{"age": 17}`, SQLAlchemy prints an `UPDATE` that changes
only the `age` column. This happens because `model_dump(exclude_unset=True)`
contains only fields that the client actually sent, so unspecified fields are
not overwritten.

## Question 12

`secret_name` is absent because the endpoint declares
`response_model=HeroPublic`. FastAPI serializes and filters the result using
that public schema, which intentionally does not include `secret_name`.

## Question 13

The SQL contains bound placeholders, such as `%(age_1)s` and
`%(team_id_1)s`; the values `18` and `1` are passed separately in the
parameter dictionary. The values are never concatenated into the SQL text, so
they cannot change its syntax and are safe from SQL injection.

## Question 14

Filtering in the database returns only the needed rows, lets the database use
indexes and its query planner, reduces memory and network use, and makes
pagination efficient. Fetching every row into Python and filtering there gets
slower as the table grows.

## Question 15

On restart, `create_all()` creates `mission` and `heromissionlink` because
they are new tables in the metadata and do not yet exist. It does nothing for
the existing `hero` table. The rule is that `create_all()` creates missing
tables; it does not modify existing ones.

## Question 16

The unit of work inserts the parent objects first, including teams and
missions, so PostgreSQL can generate their IDs. It then inserts heroes with
their resolved `team_id` values and inserts rows in the link table with the
resolved hero and mission IDs. Assigning relationships in Python is enough;
SQLAlchemy determines the dependency order during the flush.

## Question 17

There is no `power` column immediately after editing the model because
`create_all()` never alters an existing table. Dropping all tables and running
`create_all()` again is unacceptable in production because it destroys data,
causes downtime, and can break foreign-key dependencies. A migration changes
the schema without discarding existing data.

## Question 18

`upgrade()` adds the nullable `power` column to `hero`. `downgrade()` removes
that column so the database returns to the previous schema revision.

## Question 19

Alembic stores the database's current revision in the `alembic_version` table,
normally in its `version_num` column. The `migrations/` folder must be
committed to Git so every teammate and deployment applies the same reviewed
schema history in the same order.

## Question 20

Autogenerate usually interprets a rename from `secret_name` to `alias` as one
column drop and one column add. Applying that migration would lose existing
secret-name data. The safe migration should be edited to rename the column,
for example with:

```python
op.alter_column("hero", "secret_name", new_column_name="alias")
```

The downgrade should rename `alias` back to `secret_name`. The experimental
revision should not be applied; after reviewing it, delete the test revision
and restore the original model name.

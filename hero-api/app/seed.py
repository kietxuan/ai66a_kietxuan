"""Idempotent sample-data loader; run with ``python -m app.seed``."""

from sqlmodel import SQLModel, Session, select

from app import models  # noqa: F401 - register all model tables
from app.database import engine
from app.models import Hero, Mission, Team


def seed() -> None:
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        if session.exec(select(Team)).first() is not None:
            print("Already seeded; no data was added.")
            return

        avengers = Team(name="Avengers", headquarters="New York")
        x_men = Team(name="X-Men", headquarters="Westchester")

        sokovia = Mission(title="Battle of Sokovia")
        dark_phoenix = Mission(title="Stop the Dark Phoenix")

        heroes = [
            Hero(
                name="Tony Stark",
                age=45,
                secret_name="Iron Man",
                power="Powered armor",
                team=avengers,
                missions=[sokovia],
            ),
            Hero(
                name="Natasha Romanoff",
                age=35,
                secret_name="Black Widow",
                power="Espionage and martial arts",
                team=avengers,
                missions=[sokovia],
            ),
            Hero(
                name="Peter Parker",
                age=16,
                secret_name="Spider-Man",
                power="Spider abilities",
                team=avengers,
                missions=[sokovia],
            ),
            Hero(
                name="Logan",
                age=150,
                secret_name="Wolverine",
                power="Regeneration and adamantium claws",
                team=x_men,
                missions=[dark_phoenix],
            ),
            Hero(
                name="Jean Grey",
                age=32,
                secret_name="Phoenix",
                power="Telepathy and telekinesis",
                team=x_men,
                missions=[dark_phoenix],
            ),
        ]

        session.add_all([avengers, x_men, sokovia, dark_phoenix, *heroes])
        session.commit()
        print("Seeded 2 teams, 5 heroes, and 2 missions.")


if __name__ == "__main__":
    seed()

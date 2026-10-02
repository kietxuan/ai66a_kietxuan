"""FastAPI application and all endpoints required by lab week 9."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select

from app import models  # noqa: F401 - importing registers every table in metadata
from app.database import SessionDep, engine
from app.models import (
    Hero,
    HeroCreate,
    HeroPublic,
    HeroUpdate,
    Mission,
    MissionCreate,
    MissionPublic,
    Team,
    TeamCreate,
    TeamPublic,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Create missing tables when the application starts."""
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Hero API", lifespan=lifespan)


def get_hero_or_404(session: SessionDep, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


def get_team_or_404(session: SessionDep, team_id: int) -> Team:
    team = session.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


def get_mission_or_404(session: SessionDep, mission_id: int) -> Mission:
    mission = session.get(Mission, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@app.post("/heroes", response_model=HeroPublic, status_code=status.HTTP_201_CREATED)
def create_hero(hero_in: HeroCreate, session: SessionDep) -> Hero:
    if hero_in.team_id is not None:
        get_team_or_404(session, hero_in.team_id)

    hero = Hero.model_validate(hero_in)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/heroes", response_model=list[HeroPublic])
def list_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=10, ge=1, le=100),
    min_age: int | None = None,
    team_id: int | None = None,
    name: str | None = None,
) -> list[Hero]:
    statement = select(Hero)
    if min_age is not None:
        statement = statement.where(Hero.age >= min_age)
    if team_id is not None:
        statement = statement.where(Hero.team_id == team_id)
    if name is not None:
        statement = statement.where(Hero.name.ilike(f"%{name}%"))

    statement = statement.order_by(Hero.id).offset(offset).limit(limit)
    return list(session.exec(statement).all())


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    return get_hero_or_404(session, hero_id)


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero_in: HeroUpdate, session: SessionDep) -> Hero:
    hero = get_hero_or_404(session, hero_id)
    update_data = hero_in.model_dump(exclude_unset=True)

    if "team_id" in update_data and update_data["team_id"] is not None:
        get_team_or_404(session, update_data["team_id"])

    hero.sqlmodel_update(update_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.delete("/heroes/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int, session: SessionDep) -> Response:
    hero = get_hero_or_404(session, hero_id)
    session.delete(hero)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/teams", response_model=TeamPublic, status_code=status.HTTP_201_CREATED)
def create_team(team_in: TeamCreate, session: SessionDep) -> Team:
    team = Team.model_validate(team_in)
    session.add(team)
    try:
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise HTTPException(status_code=409, detail="Team name already exists") from error
    session.refresh(team)
    return team


@app.get("/teams", response_model=list[TeamPublic])
def list_teams(session: SessionDep) -> list[Team]:
    return list(session.exec(select(Team).order_by(Team.id)).all())


@app.get("/teams/{team_id}/heroes", response_model=list[HeroPublic])
def list_team_heroes(team_id: int, session: SessionDep) -> list[Hero]:
    team = get_team_or_404(session, team_id)
    return list(team.heroes)


@app.post(
    "/missions", response_model=MissionPublic, status_code=status.HTTP_201_CREATED
)
def create_mission(mission_in: MissionCreate, session: SessionDep) -> Mission:
    mission = Mission.model_validate(mission_in)
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


@app.post(
    "/heroes/{hero_id}/missions/{mission_id}", status_code=status.HTTP_204_NO_CONTENT
)
def assign_hero_to_mission(
    hero_id: int, mission_id: int, session: SessionDep
) -> Response:
    hero = get_hero_or_404(session, hero_id)
    mission = get_mission_or_404(session, mission_id)
    if mission not in hero.missions:
        hero.missions.append(mission)
        session.add(hero)
        session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/heroes/{hero_id}/missions", response_model=list[MissionPublic])
def list_hero_missions(hero_id: int, session: SessionDep) -> list[Mission]:
    hero = get_hero_or_404(session, hero_id)
    return list(hero.missions)

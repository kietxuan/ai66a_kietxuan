"""Database engine and FastAPI session dependency."""

import os
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

connect_args: dict[str, bool] = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def get_session() -> Generator[Session, None, None]:
    """Provide one database session for each request."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

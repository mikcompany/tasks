from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Field, create_engine, Session


class Task(SQLModel, table=True):
    id: int | None = Field(default = None, primary_key=True)
    description: str = Field(default="", max_length=255)
    done: bool = Field(default=False)

class TaskCreate(SQLModel, table=False):
    description: str = Field(default="", max_length=255)

class TaskUpdate(SQLModel, table=False):
    description: str = Field(default="", max_length=255)
    done: bool= Field(default=False)

sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

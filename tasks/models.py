from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(default="", max_length=255)
    done: bool = Field(default=False)


class TaskCreate(SQLModel, table=False):
    description: str = Field(default="", max_length=255)


class TaskUpdate(SQLModel, table=False):
    description: str | None = Field(default="", max_length=255)
    done: bool | None = Field(default=False)

from typing import Annotated
import typer
from mainapp.main import repository
from tasks.models import TaskCreate, TaskUpdate

app = typer.Typer()
tasks_app = typer.Typer()
app.add_typer(tasks_app, name="tasks")

@tasks_app.command()
def new(description: str):
    task = repository.create_task(TaskCreate(description=description))
    typer.echo(f"Created task: {task}")

@tasks_app.command()
def list():
    typer.echo(f"Task list: {repository.list_tasks()}")

@tasks_app.command()
def update(task_id: int, desc: Annotated[str | None, typer.Option(help="Description of the task")] = None, done: Annotated[bool | None, typer.Option(help="Status of the task")] = None):
    task = repository.update_task(task_id, TaskUpdate(description=desc, done=done))
    if task is None:
        typer.echo(f"Task with id {task_id} not found")
    else:
        typer.echo(f"Updated task: {task}")

@tasks_app.command()
def delete(task_id: int):
    task = repository.delete_task(task_id)
    if task is None:
        typer.echo(f"Task with id {task_id} not found")
    else:
        typer.echo(f"Deleted task: {task}")

if __name__ == "__main__":
    app()

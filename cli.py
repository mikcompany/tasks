import typer
from mainapp.main import repository
from tasks.models import TaskCreate

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
def delete(task_id: int):
    task = repository.delete_task(task_id)
    if task is None:
        typer.echo(f"Task with id {task_id} not found")
    else:
        typer.echo(f"Deleted task: {task}")

if __name__ == "__main__":
    app()

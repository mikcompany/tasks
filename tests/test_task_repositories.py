from tasks.task_repositories import InMemoryTaskRepository
from tasks.tasks import TaskCreate, TaskUpdate

class TestTaskRepositories:
    def setup_method(self):
        self.repository = InMemoryTaskRepository()
        self.repository.create_task(TaskCreate(description="buy milk"))
        self.repository.create_task(TaskCreate(description="buy eggs"))
        self.repository.create_task(TaskCreate(description="buy bread"))

    def test_create_task(self):
        assert(len(self.repository.tasks) == 3)
        task = self.repository.create_task(TaskCreate(description="buy cheese"))
        assert(len(self.repository.tasks) == 4)
        assert(task.description == "buy cheese")
        assert(task.done == False)

    def test_update_task(self):
        self.repository.update_task(1, TaskUpdate(description="buy 2 milks", done=True))
        task = self.repository.get_task(1)
        assert(task is not None)
        assert(task.description == "buy 2 milks")
        assert(task.done == True)

    def test_delete_task(self):
        task = self.repository.delete_task(1)
        assert(task is not None)
        assert(len(self.repository.tasks) == 2)
        task = self.repository.get_task(1)
        assert(task is None)

        task = self.repository.delete_task(33)
        assert(task is None)
        assert(len(self.repository.tasks) == 2)

    def test_get_task(self):
        task = self.repository.get_task(3)
        assert(task is not None)
        assert(task.description == "buy bread")
        assert(task.done == False)

    def test_list_tasks(self):
        tasks = self.repository.tasks
        assert(len(tasks) == 3)

    def test_task_ids_are_unique_after_deletion(self):
        self.repository.delete_task(2)
        assert(len(self.repository.tasks) == 2)
        new_task = self.repository.create_task(TaskCreate(description="buy apples"))
        assert(len(self.repository.tasks) == 3)
        assert(new_task.id != 2)
        task_ids = [task.id for task in self.repository.tasks.values()]
        assert(len(task_ids) == len(set(task_ids)))

import logging

from src.database.exceptions import NoTaskError
from src.database.repositories.tasks_repository import TasksRepository

LOGGER = logging.getLogger(__name__)


class TasksService:
    def __init__(self, tasks_repository: TasksRepository):
        self.tasks_repository = tasks_repository

    async def add_task(self, uid):
        return await self.tasks_repository.add(uid=uid)

    async def get_task_with_images(self, task_uid):
        try:
            task = await self.tasks_repository.get_with_images_with_faces(task_uid=task_uid)
            return task
        except NoTaskError as err:
            LOGGER.info(f"Cant get task with images, no task with {task_uid} in database")
            raise err

    async def delete_task(self, task_uid):
        try:
            await self.tasks_repository.delete(task_uid)
        except NoTaskError as err:
            LOGGER.info(f"Cant delete task, no task with {task_uid} in database")
            raise err

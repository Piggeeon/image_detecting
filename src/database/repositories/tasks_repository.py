import logging

from sqlalchemy import case, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func

from src.api.schemas import TaskSchema
from src.database.exceptions import NoTaskError
from src.database.models import FaceModel, ImageModel, TaskModel

LOGGER = logging.getLogger(__name__)


class TasksRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def add(self, uid):
        task = TaskModel(uid=uid)
        self.session.add(task)

    async def get_with_images_with_faces(self, task_uid):
        task: TaskModel = (
            await self.session.execute(select(TaskModel).where(TaskModel.uid == task_uid)
                                       .options(joinedload(TaskModel.images).joinedload(ImageModel.faces))
                                       )).unique().scalars().first()
        if not task:
            LOGGER.info(f"No task with task_uid: {task_uid}")
            raise NoTaskError()

        gender_stats = (await self.session.execute(
            select(
                func.count(case((FaceModel.gender == 'male', 1), else_=None)).label('men_total'),
                func.count(case((FaceModel.gender == 'female', 1), else_=None)).label('women_total'),
                func.avg(case((FaceModel.gender == 'male', FaceModel.age), else_=None)).label('avg_age_men'),
                func.avg(case((FaceModel.gender == 'female', FaceModel.age), else_=None)).label('avg_age_women')
            )
            .join(ImageModel, FaceModel.image_name == ImageModel.name)
            .join(TaskModel, ImageModel.task_uid == TaskModel.uid)
            .where(TaskModel.uid == task_uid)
        )).fetchone()

        task.men_total_number = gender_stats.men_total or 0
        task.women_total_number = gender_stats.women_total or 0
        task.faces_total_number = task.men_total_number + task.women_total_number
        task.average_age_of_men = gender_stats.avg_age_men or 0
        task.average_age_of_women = gender_stats.avg_age_women or 0

        return TaskSchema(**task.__dict__)

    async def delete(self, task_uid):
        task: TaskModel = (
            await self.session.execute(select(TaskModel).where(TaskModel.uid == task_uid))).scalars().first()

        if not task:
            LOGGER.info(f"No task with task_uid: {task_uid}")
            raise NoTaskError()

        await self.session.delete(task)

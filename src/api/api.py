import logging
import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from src.api.schemas import TaskSchema
from src.config import DATABASE_URL
from src.database.database_core import DatabaseCore
from src.database.exceptions import NoTaskError
from src.database.repositories.tasks_repository import TasksRepository
from src.facecloud.facecloud import FaceCloud, FaceCloudBadResponseError
from src.services.tasks_service import TasksService

LOGGER = logging.getLogger(__name__)

tasks_router = APIRouter(prefix="/tasks")

db_core = DatabaseCore(url=DATABASE_URL)


async def get_db_session():
    session = await db_core.get_session()
    yield session
    await session.close()


@tasks_router.get("/{task_uid}", status_code=status.HTTP_200_OK, response_model=TaskSchema)
async def get_task_with_images(task_uid: UUID, session=Depends(get_db_session)):
    try:
        tasks_repository = TasksRepository(session=session)
        tasks_service = TasksService(tasks_repository=tasks_repository)
        task = await tasks_service.get_task_with_images(task_uid=task_uid)
        return task
    except NoTaskError:
        LOGGER.info(f"Task with uid {task_uid} not found")
        raise HTTPException(status_code=404, detail=f"Item with uid {task_uid} not found")


@tasks_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(session=Depends(get_db_session)):
    uid = str(uuid.uuid4())

    tasks_repository = TasksRepository(session=session)
    tasks_service = TasksService(tasks_repository=tasks_repository)
    await tasks_service.add_task(uid=uid)
    await session.commit()
    return uid


@tasks_router.delete("/{task_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_uid: UUID, session=Depends(get_db_session)):
    try:
        tasks_repository = TasksRepository(session=session)
        tasks_service = TasksService(tasks_repository=tasks_repository)
        await tasks_service.delete_task(task_uid=task_uid)
        await session.commit()

    except NoTaskError:
        LOGGER.info(f"Task with uid {task_uid} not found")
        raise HTTPException(status_code=404, detail=f"Item with uid {task_uid} not found")

    except Exception as err:
        LOGGER.exception(f"Cant delete task with error: {err}")
        raise HTTPException(status_code=500, detail=f"Cant delete task with error: {err}")


@tasks_router.post("/{task_uid}/add_image", status_code=status.HTTP_201_CREATED)
async def add_image_to_task(task_uid: UUID, file: UploadFile, session=Depends(get_db_session)):
    try:

        file_bytes = await file.read()

        face_cloud_data = await FaceCloud.process_image(file_bytes=file_bytes, content_type=file.content_type)

        await FaceCloud.add_image_to_task(image_name=file.filename,
                                          face_cloud_data=face_cloud_data,
                                          file_bytes=file_bytes,
                                          db_session=session,
                                          task_uid=task_uid)
        await session.commit()

    except NoTaskError:
        LOGGER.info(f"Task with uid {task_uid} not found")
        raise HTTPException(status_code=404, detail=f"Item with uid {task_uid} not found")

    except FaceCloudBadResponseError:
        LOGGER.exception("FaceCloud service unavailable")
        raise HTTPException(status_code=503, detail="FaceCloud service unavailable")

    except Exception as err:
        LOGGER.exception(f"Cant add image to task with error: {err}")
        raise HTTPException(status_code=500, detail=f"Cant add image to task with error: {err}")

import json
import uuid
from pathlib import Path

import aiohttp

from src.api.schemas import FaceSchema, ImageSchema
from src.config import FACE_CLOUD_TOKEN, FACE_CLOUD_URL, IMAGES_DIRECTORY
from src.database.repositories.faces_repository import FacesRepository
from src.database.repositories.images_repository import ImagesRepository
from src.facecloud.exceptions import FaceCloudBadResponseError
from src.services.faces_service import FacesService
from src.services.images_service import ImagesService


class FaceCloud:

    @staticmethod
    async def process_image(file_bytes, content_type):
        headers = {
            "Authorization": f"Bearer {FACE_CLOUD_TOKEN}",
            "Content-Type": content_type,
        }

        params = {"demographics": "true"}

        async with aiohttp.ClientSession() as new_session:
            async with new_session.post(url=FACE_CLOUD_URL, headers=headers, data=file_bytes,
                                        params=params) as response:
                if not response.status == 200:
                    raise FaceCloudBadResponseError()

                face_cloud_data = (await response.json()).get("data")
                return face_cloud_data

    @staticmethod
    async def add_image_to_task(*, image_name, face_cloud_data, file_bytes, db_session, task_uid):
        image_name = image_name

        img_path = Path(IMAGES_DIRECTORY) / image_name
        Path(IMAGES_DIRECTORY).mkdir(exist_ok=True)
        img_path.write_bytes(file_bytes)

        images_repository = ImagesRepository(session=db_session)
        images_service = ImagesService(images_repository=images_repository)

        new_image = ImageSchema(name=image_name,
                                task_uid=task_uid)

        await images_service.add_image(image=new_image)

        await FaceCloud._add_faces_to_task(image_name=image_name,
                                           face_cloud_data=face_cloud_data,
                                           db_session=db_session)

    @staticmethod
    async def _add_faces_to_task(image_name, face_cloud_data, db_session):
        faces_repository = FacesRepository(session=db_session)
        faces_service = FacesService(faces_repository=faces_repository)

        for face in face_cloud_data:
            bbox = json.dumps(face.get("bbox"))
            demographic = face.get("demographics")
            gender = demographic.get("gender")
            age = demographic.get("age").get("mean")

            new_face = FaceSchema(uid=str(uuid.uuid4()),
                                  image_name=image_name,
                                  bbox=bbox,
                                  gender=gender,
                                  age=age)

            await faces_service.add_face(face=new_face)

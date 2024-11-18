from src.api.schemas import ImageSchema
from src.database.repositories.images_repository import ImagesRepository


class ImagesService:
    def __init__(self, images_repository: ImagesRepository):
        self.images_repository = images_repository

    async def add_image(self, image: ImageSchema):
        return await self.images_repository.add(image=image)

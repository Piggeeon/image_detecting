from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import ImageSchema
from src.database.models import ImageModel


class ImagesRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def add(self, image: ImageSchema):
        image = ImageModel(**image.model_dump())
        self.session.add(image)

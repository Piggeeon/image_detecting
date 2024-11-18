from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import FaceSchema
from src.database.models import FaceModel


class FacesRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def add(self, face: FaceSchema):
        task = FaceModel(**face.model_dump())
        self.session.add(task)

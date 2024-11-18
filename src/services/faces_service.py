from src.api.schemas import FaceSchema
from src.database.repositories.faces_repository import FacesRepository


class FacesService:
    def __init__(self, faces_repository: FacesRepository):
        self.faces_repository = faces_repository

    async def add_face(self, face: FaceSchema):
        return await self.faces_repository.add(face=face)

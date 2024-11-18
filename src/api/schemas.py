from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class TaskSchema(BaseSchema):
    uid: UUID
    faces_total_number: int = 0
    men_total_number: int = 0
    women_total_number: int = 0
    average_age_of_men: float = 0
    average_age_of_women: float = 0

    images: List["ImageWithFacesSchema"]


class ImageSchema(BaseSchema):
    name: str
    task_uid: UUID


class ImageWithFacesSchema(ImageSchema):
    faces: List["FaceSchema"]


class FaceSchema(BaseSchema):
    uid: UUID
    image_name: str
    bbox: str
    gender: str
    age: int

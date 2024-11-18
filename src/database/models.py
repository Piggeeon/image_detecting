import uuid
from typing import List

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()


class TaskModel(Base):
    __tablename__ = 'tasks'

    uid: Mapped[uuid.UUID] = mapped_column(type_=UUID, primary_key=True, nullable=False)
    images: Mapped[List["ImageModel"]] = relationship("ImageModel",
                                                      back_populates="task",
                                                      cascade="all, delete",
                                                      passive_deletes=True)


class ImageModel(Base):
    __tablename__ = 'images'

    name: Mapped[str] = mapped_column(primary_key=True)
    task_uid: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.uid", ondelete="CASCADE"), type_=UUID, nullable=False)

    faces: Mapped[List["FaceModel"]] = relationship("FaceModel",
                                                    back_populates="image",
                                                    cascade="all, delete",
                                                    passive_deletes=True)

    task = relationship("TaskModel",
                        back_populates="images")


class FaceModel(Base):
    __tablename__ = 'faces'

    uid: Mapped[uuid.UUID] = mapped_column(type_=UUID, primary_key=True, nullable=False)
    image_name: Mapped[str] = mapped_column(ForeignKey("images.name", ondelete="CASCADE"), nullable=False)
    bbox: Mapped[dict] = mapped_column(type_=JSONB)
    gender: Mapped[str]
    age: Mapped[int]

    image = relationship("ImageModel",
                         back_populates="faces")

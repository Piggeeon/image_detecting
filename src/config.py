import logging
import os

from dotenv import load_dotenv
from sqlalchemy import URL

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG, handlers=[stream_handler])


load_dotenv()

DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_DRIVER = os.getenv('DATABASE_DRIVER')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

DATABASE_URL = URL.create(
    drivername=DATABASE_DRIVER,
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_NAME,
)

FACE_CLOUD_URL = os.getenv('FACE_CLOUD_URL')
FACE_CLOUD_TOKEN = os.getenv('FACE_CLOUD_TOKEN')

IMAGES_DIRECTORY = os.getenv('IMAGES_DIRECTORY')

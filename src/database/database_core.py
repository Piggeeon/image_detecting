from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DatabaseCore:
    def __init__(self, url: URL):
        self.url = url
        self.engine = create_async_engine(url, echo=True)
        self.session_factory = async_sessionmaker(bind=self.engine)

    async def get_session(self):
        return self.session_factory()

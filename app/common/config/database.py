from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from common.config.settings import Settings

engine = create_engine(Settings.get_uri_db())
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()


class AbstractBase(object):
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


def init_db():
    import entities.entities as entities  # noqa
    Base.metadata.create_all(bind=engine)

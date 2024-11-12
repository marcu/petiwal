from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from entities import Base
from settings import SQLLITE_DB_PATH


def get_session():
    """Return a session to interact with the database"""
    engine = create_engine(SQLLITE_DB_PATH, echo=True)

    # Create the tables if they don't exist
    Base.metadata.create_all(engine)

    # Start a session to interact with the database
    session = Session(bind=engine)

    return session

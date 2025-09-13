"""Database setup and session management using SQLAlchemy."""
import os
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

load_dotenv()  # Load environment variables from .env file

DB_CONNECTION_STRING = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_CONNECTION_STRING, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

def init_db():
    """Initialize the database by creating all tables."""

    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db_session():
    """
    Provide a transactional scope around a series of operations.
    
    This context manager yields a SQLAlchemy session that can be used to 
    interact with the database. When the context exits:

    - If no exceptions occur, the session is committed.
    - If an exception occurs, the session is rolled back and the exception 
      is re-raised.
    - In all cases, the session is properly closed at the end.
    """
    session = db_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

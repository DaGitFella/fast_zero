from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db = create_engine('sqlite:///test.db')
session_factory = sessionmaker(bind=db)
session = session_factory()
Base = declarative_base()

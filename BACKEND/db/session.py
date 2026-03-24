from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

engine = create_engine(settings.db_connection_string, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
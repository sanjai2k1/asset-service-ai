from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

engine = create_engine(settings.postgresql_sqlalchemy_connection_string, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)



engine_ms = create_engine(settings.sqlserver_db_connection_string, echo=False)
SessionLocalMS = sessionmaker(bind=engine_ms, autoflush=False, autocommit=False)
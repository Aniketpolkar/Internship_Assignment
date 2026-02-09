from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "postgresql://postgres:aniket@localhost:5432/taskdb"

# db_url = "postgresql://postgres:aniket@localhost:5432/todolist"
# DATABASE_URL = "postgresql://postgres:password@localhost/taskdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

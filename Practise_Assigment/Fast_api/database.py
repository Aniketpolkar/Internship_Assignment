from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
# mongodb://localhost:27017/
# db_url = "mongodb://localhost:27017"
db_url = "postgresql://postgres:aniket@localhost:5432/todolist"
engine = create_engine(db_url)
session = sessionmaker(autocommit = False,autoflush = False, bind = engine)
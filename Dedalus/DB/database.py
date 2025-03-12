from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_FILE = "users.db"
engine = create_engine(f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False})

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)

if not os.path.exists(DB_FILE):
    Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

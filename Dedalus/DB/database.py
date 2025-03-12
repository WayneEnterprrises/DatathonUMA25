from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os

# Definir la base de datos SQLite
DB_FILE = "users.db"
engine = create_engine(f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False})

# Definir el modelo de base de datos
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    role = Column(String, nullable=False)  # "user" o "assistant"
    message = Column(Text, nullable=False)

    user = relationship("User", back_populates="chats")

# Crear la tabla si no existe
if not os.path.exists(DB_FILE):
    Base.metadata.create_all(engine)

# Crear la sesión de SQLAlchemy
SessionLocal = sessionmaker(bind=engine)

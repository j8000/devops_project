from sqlalchemy import Column, Integer, String
from app.src.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __repr__(self):
        return f'<User {self.name!r}>'

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    status = Column(String(20), default='pending')

    def __repr__(self):
        return f'<Task {self.title!r}>'

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False) # Store as cents

    def __repr__(self):
        return f'<Product {self.name!r}>'

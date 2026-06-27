from sqlalchemy import Column, Integer, String, Text, ForeignKey
from db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    emal = Column(String(100), unique=True)
    password = Column(String(100))
    
class Reports(Base):
    __tablename__="reports"
    
    id = Column(Integer, primary_key("users.id"))
    user_id = Column(Text)
    result = Column(Text)

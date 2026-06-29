# from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from db import Base

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True)
#     emall = Column(String(100), unique=True)
#     password = Column(String(100))
    
# class Reports(Base):
#     __tablename__="reports"
    
#     id = Column(Integer, primary_key("users.id"))
#     user_id = Column(Text)
#     result = Column(Text)


from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    reports = relationship(
        "Report",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    goal = Column(String(255), nullable=False)
    resume_text = Column(Text, nullable=False)
    result_json = Column(Text, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", back_populates="reports")
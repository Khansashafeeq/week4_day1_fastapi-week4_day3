from database import Base
from sqlalchemy import Column, Integer, String

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    grade = Column(String)
    city = Column(String)

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Student
from pydantic import BaseModel

app = FastAPI()

# Create tables
Student.__table__.create(engine)

class StudentRequest(BaseModel):
    name: str
    age: int
    grade: str
    city: str

@app.post("/students/")
def create_student(student: StudentRequest, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/")
def read_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentRequest, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.name = student.name
    db_student.age = student.age
    db_student.grade = student.grade
    db_student.city = student.city
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted"}

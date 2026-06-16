from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI(title="Registration Service")

# Synthetic student database (no real data)
students_db = []

# Student Model
class Student(BaseModel):
    student_id: str
    name: str
    department: str
    courses: List[str]

# Health Check
@app.get("/")
def home():
    return {
        "service": "Registration Service",
        "status": "Running",
        "timestamp": str(datetime.datetime.now())
    }

# Register a new student
@app.post("/register")
def register_student(student: Student):
    # Check if already registered
    for s in students_db:
        if s["student_id"] == student.student_id:
            return {
                "status": "Failed",
                "message": "Student already registered"
            }
    
    students_db.append(student.dict())
    return {
        "status": "Success",
        "message": f"Student {student.name} registered successfully",
        "data": student.dict()
    }

# Get all students
@app.get("/students")
def get_all_students():
    return {
        "status": "Success",
        "total_students": len(students_db),
        "students": students_db
    }

# Get student by ID
@app.get("/students/{student_id}")
def get_student(student_id: str):
    for s in students_db:
        if s["student_id"] == student_id:
            return {
                "status": "Success",
                "data": s
            }
    return {
        "status": "Failed",
        "message": "Student not found"
    }

# Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    for s in students_db:
        if s["student_id"] == student_id:
            students_db.remove(s)
            return {
                "status": "Success",
                "message": f"Student {student_id} removed"
            }
    return {
        "status": "Failed",
        "message": "Student not found"
    }
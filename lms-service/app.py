from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI(title="LMS Service")

# Synthetic data storage
courses_db = []
assignments_db = []
materials_db = []

# Models
class Course(BaseModel):
    course_id: str
    course_name: str
    instructor: str
    credits: int

class Assignment(BaseModel):
    assignment_id: str
    course_id: str
    title: str
    deadline: str

class Material(BaseModel):
    material_id: str
    course_id: str
    title: str
    content: str

# Health Check
@app.get("/")
def home():
    return {
        "service": "LMS Service",
        "status": "Running",
        "timestamp": str(datetime.datetime.now())
    }

# Add a course
@app.post("/courses")
def add_course(course: Course):
    courses_db.append(course.dict())
    return {
        "status": "Success",
        "message": f"Course {course.course_name} added",
        "data": course.dict()
    }

# Get all courses
@app.get("/courses")
def get_courses():
    return {
        "status": "Success",
        "total_courses": len(courses_db),
        "courses": courses_db
    }

# Add assignment
@app.post("/assignments")
def add_assignment(assignment: Assignment):
    assignments_db.append(assignment.dict())
    return {
        "status": "Success",
        "message": f"Assignment {assignment.title} added",
        "data": assignment.dict()
    }

# Get all assignments
@app.get("/assignments")
def get_assignments():
    return {
        "status": "Success",
        "total_assignments": len(assignments_db),
        "assignments": assignments_db
    }

# Add study material
@app.post("/materials")
def add_material(material: Material):
    materials_db.append(material.dict())
    return {
        "status": "Success",
        "message": f"Material {material.title} uploaded",
        "data": material.dict()
    }

# Get all materials
@app.get("/materials")
def get_materials():
    return {
        "status": "Success",
        "total_materials": len(materials_db),
        "materials": materials_db
    }

# Get course by ID
@app.get("/courses/{course_id}")
def get_course(course_id: str):
    for c in courses_db:
        if c["course_id"] == course_id:
            return {
                "status": "Success",
                "data": c
            }
    return {
        "status": "Failed",
        "message": "Course not found"
    }
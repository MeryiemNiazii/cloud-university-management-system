from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import datetime
import statistics

app = FastAPI(title="Examination Service")

# Synthetic data
exams_db = []
results_db = []

# Models
class Exam(BaseModel):
    exam_id: str
    course_id: str
    exam_date: str
    total_marks: int
    duration_minutes: int

class Result(BaseModel):
    result_id: str
    student_id: str
    exam_id: str
    marks_obtained: int
    total_marks: int

# Health Check
@app.get("/")
def home():
    return {
        "service": "Examination Service",
        "status": "Running",
        "timestamp": str(datetime.datetime.now())
    }

# Schedule an exam
@app.post("/exams")
def schedule_exam(exam: Exam):
    exams_db.append(exam.dict())
    return {
        "status": "Success",
        "message": f"Exam {exam.exam_id} scheduled",
        "data": exam.dict()
    }

# Get all exams
@app.get("/exams")
def get_exams():
    return {
        "status": "Success",
        "total_exams": len(exams_db),
        "exams": exams_db
    }

# Submit result
@app.post("/results")
def submit_result(result: Result):
    percentage = (result.marks_obtained / result.total_marks) * 100

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    result_data = result.dict()
    result_data["percentage"] = round(percentage, 2)
    result_data["grade"] = grade

    results_db.append(result_data)

    return {
        "status": "Success",
        "message": "Result submitted",
        "data": result_data
    }

# Get all results
@app.get("/results")
def get_results():
    return {
        "status": "Success",
        "total_results": len(results_db),
        "results": results_db
    }

# Get result statistics
@app.get("/results/statistics")
def get_statistics():
    if not results_db:
        return {
            "status": "Failed",
            "message": "No results available"
        }

    marks_list = [r["marks_obtained"] for r in results_db]

    return {
        "status": "Success",
        "statistics": {
            "total_results": len(results_db),
            "highest_marks": max(marks_list),
            "lowest_marks": min(marks_list),
            "average_marks": round(statistics.mean(marks_list), 2),
            "median_marks": statistics.median(marks_list)
        }
    }

# Get result by student ID
@app.get("/results/{student_id}")
def get_student_result(student_id: str):
    student_results = [
        r for r in results_db
        if r["student_id"] == student_id
    ]
    if student_results:
        return {
            "status": "Success",
            "data": student_results
        }
    return {
        "status": "Failed",
        "message": "No results found for this student"
    }
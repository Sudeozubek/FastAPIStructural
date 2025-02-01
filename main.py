from fastapi import FastAPI, Body ,Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Course:
    id: int
    title: str
    instructor: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, instructor: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.instructor = instructor
        self.rating = rating
        self.published_date = published_date

course_db = [
    Course(id= 1, title= "Python", instructor="Sude", rating=5, published_date=2029),
    Course(id= 2, title= "Kotlin", instructor= "Halil", rating= 5, published_date= 2030),
    Course(id= 3, title= "Jenkins", instructor= "Ahmet", rating= 5, published_date= 2025),
    Course(id= 4, title= "Kubernetes", instructor= "Ali", rating= 2, published_date= 2026),
    Course(id= 5, title= "Machine Learning", instructor= "Mehmet", rating= 3, published_date= 2036),
    Course(id= 6, title= "Deep Learning", instructor= "Ayşe", rating= 1, published_date= 2034)
]


@app.get(path="/courses", status_code=status.HTTP_200_OK)
async def get_all_courses():
    return course_db

@app.get(path="/courses/{course_id}", status_code=status.HTTP_200_OK)
async def get_course(course_id:int = Path(gt=0)):
    for course in course_db:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

@app.get("/courses/", status_code=status.HTTP_200_OK)
async def get_courses_by_rating(course_rating: int = Query(gt=0, lt=6)):
    courses_to_return = []
    for course in course_db:
        if course.rating == course_rating:
            courses_to_return.append(course)

    return courses_to_return
@app.get("/courses/publish/", status_code=status.HTTP_200_OK)
async def get_courses_by_publish_date(publish_date: int = Query(gt=2005, lt=2036)):
    courses_to_return = []
    for course in course_db:
        if course.published_date == publish_date:
            courses_to_return.append(course)

    return courses_to_return

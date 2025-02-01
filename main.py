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

class CourseRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not required', default=None)
    title: str = Field(min_length=3)
    instructor: str = Field(min_length=3)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "course title",
                "instructor": "atil samancioglu",
                "rating": 5,
                'published_date': 2027
            }
        }
    }

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

@app.post("/create-course", status_code=status.HTTP_201_CREATED)
async def create_course(course_request: CourseRequest):
    new_course = Course(**course_request.model_dump())
    courses_db.append(find_course_id(new_course))


def find_course_id(course: Course):
    course.id = 1 if len(courses_db) == 0 else courses_db[-1].id + 1
    return course


@app.put("/courses/update_course", status_code=status.HTTP_204_NO_CONTENT)
async def update_course(course: CourseRequest):
    course_changed = False
    for i in range(len(courses_db)):
        if courses_db[i].id == course.id:
            courses_db[i] = course
            course_changed = True
    if not course_changed:
        raise HTTPException(status_code=404, detail='Course not found')


@app.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int = Path(gt=0)):
    course_changed = False
    for i in range(len(courses_db)):
        if courses_db[i].id == course_id:
            courses_db.pop(i)
            course_changed = True
            break
    if not course_changed:
        raise HTTPException(status_code=404, detail='Item not found')

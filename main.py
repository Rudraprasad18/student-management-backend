from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.students import router as students_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL is working!"}


app.include_router(students_router)
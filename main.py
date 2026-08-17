from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI is working!"}


@app.get("/hello")
def hello():
    return {"message": "Hello Rudra!"}
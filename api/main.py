from fastapi import FastAPI
from routers import hotels

app = FastAPI()

app.include_router(hotels.router)
# @app.get("/")
# def root():
#     return "Hello World"
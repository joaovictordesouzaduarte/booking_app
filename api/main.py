from fastapi import FastAPI
from routers import hotels, auth, users, rooms
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(hotels.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rooms.router)

# @app.get("/")
# def root():
#     return "Hello World"
origins = [
    'http://localhost:3000/',
    'http://localhost:3000'
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*']
)
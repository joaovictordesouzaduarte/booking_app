from dotenv import load_dotenv, find_dotenv
import os
from pymongo import mongo_client

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://joaoduarte:{password}@cluster0.fkigflz.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = mongo_client.MongoClient(connection_string)

conn = None
try:
    conn = client.server_info()
    print('Connected to MongoDB')
except Exception:
    print('Unable to connect to the MongoDB Server')

hotels_collection = client.booking.hotels
user_collection = client.booking.user
room_collection = client.booking.room

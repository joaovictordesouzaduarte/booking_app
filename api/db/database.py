from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://joaoduarte:{password}@cluster0.fkigflz.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_string)
print('Connected to MongoDB')

hotels_collection = client.booking.hotels
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize as None
client = None
db = None
collection = None

# Constants
MONGODB_URI = "mongodb://localhost:27017/"
DATABASE_NAME = 'github_monitor'
COLLECTION_NAME = 'events'

def init_db():
    """Initialize MongoDB connection"""
    global client, db, collection
    
    if collection is None:
        mongo_uri = MONGODB_URI
        if not mongo_uri:
            raise ValueError("MONGO_URI not found in environment variables")
        
        client = MongoClient(mongo_uri)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        print(f"✅ MongoDB connected: {DATABASE_NAME}.{COLLECTION_NAME}")
    
    return collection

def get_collection():
    """Get the MongoDB collection, initializing if necessary"""
    global collection
    
    if collection is None:
        return init_db()
    
    return collection

def get_client():
    """Get the MongoDB client, initializing if necessary"""
    global client
    
    if client is None:
        init_db()
    
    return client
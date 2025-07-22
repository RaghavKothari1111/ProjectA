from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio
import sys
from bson import ObjectId

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()

client = AsyncIOMotorClient(MONGO_URI)
db = client['projectA_db']
users_collection = db['users']

@app.get('/')
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.on_event('startup')
async def startup_db_client():
    print("Connecting to the database...")

    async def ping_connection():
        await client.admin.command('ping')

    try:
        await asyncio.wait_for(ping_connection(), timeout=5)
        print("Database connection successful!")
    except asyncio.TimeoutError:
        print("Database connection timed out after 5 seconds.")
        sys.exit(1)
    except Exception as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)

@app.get('/users')
async def get_users():
    users_cursor = users_collection.find()
    users = []
    async for u in users_cursor:
        u['_id'] = str(u['_id'])
        users.append(u)
    return {"users": users}

@app.put('/users/{user_id}')
async def update_user(user_id: str, user_data: dict):
    update_data = {k: v for k, v in user_data.dict().items() if v is not None}

    if not update_data:
        return {'message': 'No fields to update.'}
    
    result= await users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': update_data}
    )
    if result.matched_count == 0:
        return {'message': 'No user found with the given ID or no changes made.'}
    
    return {'message': 'User updated successfully.'}



@app.on_event('shutdown')
async def shutdown_db_client():
    print("Closing database connection...")
    client.close()
    print("Database connection closed.")

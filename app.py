from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio
import sys
from bson import ObjectId
from pydantic import BaseModel
from typing import Optional

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

@app.get('/users')
async def get_users():
    users_cursor = users_collection.find()
    users = []
    async for u in users_cursor:
        u['_id'] = str(u['_id'])
        users.append(u)
    return {"users": users}

@app.put('/users/{user_id}')
async def update_user(user_id: str, user_data: UserUpdate):
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


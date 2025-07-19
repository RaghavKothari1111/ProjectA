from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

app=FastAPI()

client=AsyncIOMotorClient('mongodb+srv://raghav192003:<db_password>@cluster0.wttshhu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db=client['projectA_db']

users_collection=db['users']










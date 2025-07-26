from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from config import settings
import sys

client = AsyncIOMotorClient(mongo_uri)
db = client['projectA_db']

async def connect_to_db(mongo_uri: str):
    try:
        
        print("Trying to connect to db")

        await asyncio.wait_for(client.admin.command('ping'), timeout=5)
        print("Database connection successful!")
    
    except asyncio.TimeoutError:
        print("Database connection timed out after 5 seconds.")
        sys.exit(1)
    except Exception as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)

async def shutdown_db_client():
    print("Closing database connection...")
    client.close()
    print("Database connection closed.")
        



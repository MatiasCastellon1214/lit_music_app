from fastapi import APIRouter, HTTPException, status
from typing import List
from models.UserModel import User
from schema.UserSchema import users_schema
from services.UserService import search_user, create_user, update_user, delete_user
from db.config.db import db_client
from bson import ObjectId


router = APIRouter(prefix="/users", 
                   tags=["users"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})


# GET - All Users
@router.get("/", tags=["users"], 
            response_model=List[User])
async def get_users():
    return users_schema(db_client.users.find())


# GET - Calling a user by id - Path
@router.get('/{id}')
async def user(id: str):
    return search_user('_id', ObjectId(id))

'''# GET - Calling a user by id - Query
@router.get("/search")
async def user(id: str):
    return search_user("_id", ObjectId(id))

'''


# POST
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: User):
    return create_user(user)


# PUT
@router.put('/{id}', tags=["users"], 
            response_model=User)
async def update_existing_user(id: str, user: User):
    return update_user(id, user)


# DELETE
@router.delete("/{id}", tags=["users"],
               response_model=User)
async def remove_user(id: str):
    return delete_user(id)
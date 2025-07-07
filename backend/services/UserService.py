from bson import ObjectId
from fastapi import HTTPException, status
from db.config.db import db_client
from schema.UserSchema import user_schema
from models.UserModel import User
from utils.encryption import encrypt_password, f


# Search User
def search_user(field: str, key):
    '''Search for an user by a given field (e.g. "email")'''
    try:
        user = db_client.users.find_one({field: key})
        print(user)
        return User(**user_schema(user))
    except:
        return {'error': 'User not found'}


# Create User
def create_user(user: User):

    """Create a new user if the email does not already exist."""
    if type(search_user('email', user.email)) == User:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail= 'User already exists'
        )
    
    user_dict = user.model_dump()
    user_dict['password'] = f.encrypt(user.password.encode('utf-8')).decode('utf-8')
    user_dict.pop('id', None)

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({'_id': id}))

    return User(**new_user)


# Update User
def update_user(id: str, user: User):

    
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user id'
        )
    
    # Check if the user exists before updating
    existing_user = db_client.users.find_one({"_id": ObjectId(id)})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    # Convert Id to ObjectId
    user_dict = user.model_dump(exclude='id') # Exclude 'Id' from body
    user_dict['password'] = f.encrypt(user.password.encode('utf-8')).decode('utf-8')
    

    try:

        result =db_client.users.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': user_dict},
            return_document=True)

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= 'User not found'
            )
        
        return User(**user_schema(result))

    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An error occurred: {e}'
        )


# Delete User
def delete_user(id: str):

    # Validate if the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail='Invalid user Id'
        )

    user_found = db_client.users.find_one({'_id': ObjectId(id)})

    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Delete User after obtaining it
    db_client.users.delete_one({'_id': ObjectId(id)})

    return user_found
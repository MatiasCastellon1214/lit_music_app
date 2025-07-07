'''from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from db.config.db import db_client
from db.model.UserModel import User
from db.schema.UserSchema import users_schema, user_schema
from bson import ObjectId
from cryptography.fernet import Fernet

router = APIRouter(prefix="/users--", 
                   tags=["users--"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})
'''
# Generate a key and create a Fernet object
'''key = Fernet.generate_key()
f = Fernet(key)
'''
'''def search_user(field: str, key):
#   #Search for an user by a given field (e.g. "email")
    try:
        user = db_client.users.find_one({field: key})
        print(user)
        return User(**user_schema(user))
    except:
        return {'error': 'User not found'}

'''
'''
# GET
@router.get("/", response_model=List[User],
            tags=["users"])
async def get_users():
    #users = db_client.User.find()
    return users_schema(db_client.users.find())
'''


'''# POST
@router.post("/", response_model= User, 
             status_code=status.HTTP_201_CREATED,
             tags=["users"])
async def create_user(user: User):

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
'''

'''# PUT
@router.put('/{id}', tags=["users"],
            response_model=User)
async def update_user(id: str, user: User):

    # Validate if the ID is a valid ObjectId
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid user id'
        )

    # Convert Id to ObjectId
    user_dict = user.model_dump(exclude='id') # Exclude 'Id' from body
    user_dict['password'] = f.encrypt(user.password.encode('utf-8')).decode('utf-8')
    user_dict.pop('id', None)

    try:

        result =db_client.users.find_one_and_replace(
            {'_id': ObjectId(id)},
            user_dict,
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
        )'''
'''

# DELETE
@router.delete('/{id}', tags=['users'],
              #status_code=status.HTTP_204_NO_CONTENT,
              response_model=User
              )
async def delete_user(id: str):

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
'''
'''
user = APIRouter()

key = Fernet.generate_key()
f = Fernet(key)

@user.get("/users", response_model=List[User], tags=["users"])
async def get_users():
    result = conn.execute(users.select()).fetchall()
    return [dict(row._mapping) for row in result]
    
@user.get("/users/{id}", response_model=User, tags=["users"])
async def get_user(id: str):
    result = conn.execute(users.select().where(users.c.id == id)).first()
    return dict(result._mapping) if result else {"error": "User not found"}


# POST

@user.post("/users", response_model=User, tags=["users"])
async def create_user(user: User):
    
    try:
    
        new_user = {
            "name": user.name,
            "email": user.email,
            "password": f.encrypt(user.password.encode("utf-8"))
        }
        result = conn.execute(users.insert().values(new_user))
        conn.commit()

        # Obetener el ID del usuario insertado
        last_inserted_id = result.inserted_primary_key[0]

        # Consultar el usuario recién insertado y convertirlo a un diccionario
        inserted_user = conn.execute(users.select().where(users.c.id == last_inserted_id)).first()

        # Convertir el resultado a un diccionario antes de devolverlo
        inserted_user_id = dict(inserted_user._mapping) if inserted_user else {"error": "User not found"}
        print("Received: User created correctly")
        return inserted_user_id

    except SQLAlchemyError as e:
        print(str(e))
        return {"error": str(e)}    


@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: str):
    result = conn.execute(users.delete().where(users.c.id == id))
    #conn.commit()
    return Response(status_code=HTTP_204_NO_CONTENT) if result.rowcount else {"error": "User not found"}  
        

@user.put("/users/{id}", response_model=User, tags=["users"])
async def update_user(id: str, user: User):
    try:
        conn.execute(users.update().values(
            name=user.name, 
            email=user.email, 
            password=f.encrypt(user.password.encode('utf-8'))
        ).where(users.c.id == id))
        conn.commit()
        updated_user = conn.execute(users.select().where(users.c.id == id)).first()
        return dict(updated_user._mapping) if updated_user else {"error": "User not found"}
    except SQLAlchemyError as e:
        print(str(e))
        return {"error": str(e)}'''
from datetime import date
from typing import List

import databases
import sqlalchemy
from sqlalchemy import create_engine
import uvicorn
from fastapi import FastAPI
from hw6.model_user import User, UserWithId

DATABASE_URL = "sqlite:///hwbase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users",
                         metadata,
                         sqlalchemy.Column("user_id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("first_name", sqlalchemy.String(32)),
                         sqlalchemy.Column("last_name", sqlalchemy.String(32)),
                         sqlalchemy.Column("birthdate", sqlalchemy.Date()),
                         sqlalchemy.Column("email", sqlalchemy.String(50)),
                         sqlalchemy.Column("address", sqlalchemy.String(100))
                         )

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/users/', response_model=List[UserWithId])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}', response_model=UserWithId)
async def get_user(user_id: int):
    query = users.select().where(users.c.user_id == user_id)
    return await database.fetch_one(query)


@app.post("/users/", response_model=UserWithId)
async def create_user(user: User):
    query = users.insert().values(first_name=user.first_name, last_name=user.last_name, birthdate=user.birthdate,
                                  email=user.email, address=user.address)
    last_record_id = await database.execute(query)

    return {**user.model_dump(), "user_id": last_record_id}


@app.put("/users/{user_id}", response_model=UserWithId)
async def update_user(user_id: int, new_user: User):
    query = users.update().where(users.c.user_id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "user_id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.user_id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}

if __name__ == "__main__":
    uvicorn.run("z2:app")

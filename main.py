from fastapi import FastAPI, HTTPException
from database import get_database_connection
from pydantic import BaseModel

app= FastAPI();

class User(BaseModel):
    name:str
    email:str

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/users")
async def get_user():
    connection = get_database_connection()
    cursor =connection.cursor()
    query= "SELECT*FROM users"
    cursor.execute(query)
    users= cursor.fetchall()
    connection.close()
    return users


@app.post("/users")
async def create_user(user: User):
     connection= get_database_connection()
     cursor = connection.cursor()
     query= "INSERT INTO users (name, email) values ( %s, %s)"
     values= (user.name, user.email)
     cursor.execute(query, values)
     connection.commit()
     connection.close()
     return {"message":  "User Created sucessfully"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "DELETE FROM users where id= %s"
    cursor.execute(query, (user_id,))
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail= "User not found")
    return {"message": "User Delete Successfully"}

@app.put("/users/{user_id}")
async def update_user(user_id: int, user:User):
    connection= get_database_connection()
    cursor= connection.cursor()
    query = "UPDATE users SET name = %s, email = %s WHERE id= %s"
    cursor.execute(query, (user.name, user.email, user_id))
    connection.commit()
    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User UpDated Successfully"}





    
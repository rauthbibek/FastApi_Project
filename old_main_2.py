from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    
app = FastAPI()

while True:
    try:
        connection = psycopg2.connect(host='127.0.0.1', database='fastapi', user='postgres',
        password='root', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection established")
        break
    except Exception as e:
        print("Failed to connect to database")
        print("Error: ", e)
        time.sleep(3)


# my_posts = [{"title": "title 1", "content": "content 1", "id":1},
# {"title": "title 2", "content": "content 2", "id":2}]

@app.get("/") # root "/" path wit hhtp get method
def root():
    # fastapi automatically converts the python dictionary to json
    return {"message": "Hello, world!"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data":posts}

# @app.post("/posts")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"message": "This is a post request"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostModel):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    connection.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if post is not None:
        return {"data": post}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "id is invalid")

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, (str(id),))
    delete_post = cursor.fetchone()
    connection.commit()
    if delete_post:
            return Response(status_code= status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "id does not exist")

@app.put("/posts/{id}")
def update_post(id: int, post: PostModel):
    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    connection.commit()
    if updated_post:
        return {"data": updated_post}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "id does not exist")


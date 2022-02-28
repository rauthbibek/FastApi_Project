from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi.params import Body
# from pydantic import BaseModel
import psycopg2
from typing import List
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from . database import engine, get_db

# it will create all the tables from Base.metadata
models.Base.metadata.create_all(bind=engine)


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

@app.get("/") # root "/" path wit hhtp get method
def root():
    # fastapi automatically converts the python dictionary to json
    return {"message": "Hello, world!"}

@app.get("/posts", response_model=List[schemas.PostResponses])
def get_posts(db: Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponses)
def create_post(post: schemas.PostCreate, db: Session=Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # connection.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}", response_model=schemas.PostResponses)
def get_post(id: int,  db: Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is not None:
        return post
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "id is invalid")

@app.delete("/posts/{id}")
def delete_post(id: int,  db: Session=Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, (str(id),))
    # delete_post = cursor.fetchone()
    # connection.commit()
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    if delete_query.first() is not None:
        delete_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code= status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "id does not exist")

@app.put("/posts/{id}", response_model=schemas.PostResponses)
def update_post(id: int, post: schemas.PostUpdate, db: Session=Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    # (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)
    if update_query.first() is not None:
        update_query.update(post.dict(), synchronize_session=False)
        db.commit()
        return update_query.first()
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "id does not exist")


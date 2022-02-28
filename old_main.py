from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True
    
app = FastAPI()

my_posts = [{"title": "title 1", "content": "content 1", "id":1},
{"title": "title 2", "content": "content 2", "id":2}]

@app.get("/") # root "/" path wit hhtp get method
def root():
    # fastapi automatically converts the python dictionary to json
    return {"message": "Hello, world!"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

# @app.post("/posts")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"message": "This is a post request"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostModel):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, resp: Response):
    for post in my_posts:
        if post["id"]==id:
            return {"data":post}
    # resp.status_code = status.HTTP_404_NOT_FOUND
    # return {"msg":"id is invalid"}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "id is invalid")

@app.delete("/posts/{id}")
def delete_post(id: int):
    for i, post in enumerate(my_posts):
        if post["id"]==id:
            my_posts.pop(i)
            return Response(status_code= status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "id does not exist")

@app.put("/posts/{id}")
def update_post(id: int, req: PostModel):
    for i, post in enumerate(my_posts):
        if post["id"]==id:
            post_dict = req.dict()
            post_dict["id"]=id
            my_posts[i]=post_dict
            return {"data": post_dict}
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "id does not exist")


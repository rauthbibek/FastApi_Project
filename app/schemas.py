from pydantic import BaseModel
import datetime
    
class PostBase(BaseModel):
    pass


class PostCreate(PostBase):
    title: str
    content: str
    published: bool = True

class PostUpdate(PostBase):
    content: str
    published: bool

class PostResponses(PostBase):
    title: str
    content: str
    published: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True
        
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr

class SelectedCourseDelete(BaseModel):
    course_id: str

class SelectedCourseBase(BaseModel):
    course_id: str
    semester: int
    count_towards: str

    class Config:
        orm_mode = True

class SelectedCourseGet(SelectedCourseBase):
    credits: int

    class Config:
        orm_mode = True

class SelectedCourseCreate(SelectedCourseBase):
    user_id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    program_major: str
    program_minor: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    program_major: str
    program_minor: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr

class CourseGet(BaseModel):
    id: int
    course_id: str
    course_name: str
    course_credits: str
    sem_offered: str
    is_bs: bool
    is_hs: bool

    class Config:
        orm_mode = True

class ProgramGet(BaseModel):
    id: int
    major_code: str
    core_creds: int
    ext_core_creds: int
    bs_creds: int
    hs_creds: int
    open_creds: int

    class Config:
        orm_mode = True

class MinorGet(BaseModel):
    id: int
    minor_code: str

    class Config:
        orm_mode = True

class CoreRelGet(BaseModel):
    id: int
    course_id: int
    major_id: int

    class Config:
        orm_mode = True

class ExtCoreRelGet(BaseModel):
    id: int
    course_id: int
    major_id: int

    class Config:
        orm_mode = True

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
from fastapi import Response, status, HTTPException, Depends, APIRouter

from app.database import get_db
from .. import models, schemas, oauth2
from typing import Optional, List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/advisory',
    tags=['Advisory']
)

@router.get('/courses', response_model = List[schemas.CourseGet])
async def get_courses(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    courses = db.query(models.Course).all()
    return courses

@router.get('/programs', response_model = List[schemas.ProgramGet])
async def get_programs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    programs = db.query(models.ProgramMajor).all()
    return programs

@router.get('/minors', response_model = List[schemas.MinorGet])
async def get_minors(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    minors = db.query(models.ProgramMinor).all()
    return minors

@router.get('/corerel', response_model = List[schemas.CoreRelGet])
async def get_corerel(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    corerels = db.query(models.CoreRel).all()
    return corerels

@router.get('/extcorerel', response_model = List[schemas.ExtCoreRelGet])
async def get_corerel(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    extcorerels = db.query(models.ExtCoreRel).all()
    return extcorerels

@router.get('/coursetypes', response_model = List[schemas.CourseTypeGet])
async def get_coursetypes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    coursetypes = db.query(models.CourseTypes).all()
    return coursetypes
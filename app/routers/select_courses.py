from fastapi import Response, status, HTTPException, Depends, APIRouter

from app.database import get_db
from .. import models, schemas, oauth2
from typing import Optional, List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/planner',
    tags=['Planner']
)

@router.get('/', response_model=List[schemas.SelectedCourseGet])
async def get_selected_courses(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    courses = db.query(models.SelectedCourse).filter(models.SelectedCourse.user_id == current_user.id).all()
    ret = list()
    for c in courses:
        cid = c.course_id
        creds = db.query(models.Course).filter(models.Course.course_id == cid).first().course_credits
        tmp = schemas.SelectedCourseGet(user_id = c.user_id, course_id = c.course_id, semester = c.semester, count_towards = c.count_towards, credits = creds)
        ret.append(tmp)
    return ret

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.SelectedCourseGet])
async def create_selected_course(selected_course: schemas.SelectedCourseCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_selected_course = models.SelectedCourse(**selected_course.dict())
    new_selected_course.user_id = current_user.id

    check_already = db.query(models.SelectedCourse).filter(models.SelectedCourse.user_id == new_selected_course.user_id).filter(models.SelectedCourse.course_id == new_selected_course.course_id).all()
    if(len(check_already) > 0):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=f"Course Already Selected")

    ccid = new_selected_course.course_id
    cc = db.query(models.Course).filter(models.Course.course_id == ccid)
    major_code = current_user.program_major
    if cc.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
        detail=f"Course {ccid} does not exist")
    
    # check if selected course can be counted towards whatever is entered
    # Validation Not written yet
    if new_selected_course.count_towards == "BS":
        fetched_course = cc.first()
        if fetched_course.is_bs == False:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
            detail="Course cannot count towards BS")
    if new_selected_course.count_towards == "HS":
        fetched_course = cc.first()
        if fetched_course.is_hs == False:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
            detail="Course cannot count towards HS")
    if new_selected_course.count_towards == "Core":
        cc_new = db.query(models.CoreRel).filter(models.CoreRel.major_id == major_code).filter(models.CoreRel.course_id == ccid)
        if cc_new.first() == None:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
            detail="Course cannot count towards Core")
    if new_selected_course.count_towards == "Ext Core":
        cc_new = db.query(models.ExtCoreRel).filter(models.ExtCoreRel.major_id == major_code).filter(models.ExtCoreRel.course_id == ccid)
        if cc_new.first() == None:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
            detail="Course cannot count towards Ext Core")

    try:
        db.add(new_selected_course)
        db.commit()
        db.refresh(new_selected_course)
        courses = db.query(models.SelectedCourse).filter(models.SelectedCourse.user_id == current_user.id).all()
        ret = list()
        for c in courses:
            cid = c.course_id
            creds = db.query(models.Course).filter(models.Course.course_id == cid).first().course_credits
            tmp = schemas.SelectedCourseGet(user_id = c.user_id, course_id = c.course_id, semester = c.semester, count_towards = c.count_towards, credits = creds)
            ret.append(tmp)
        return ret
    
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid Request")

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_selected_course(selected_course: schemas.SelectedCourseDelete, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    sc = db.query(models.SelectedCourse).filter(models.SelectedCourse.user_id == current_user.id).filter(models.SelectedCourse.course_id == selected_course.course_id)

    if sc.first()==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
         detail=f"Course Entry Not Found")

    sc.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

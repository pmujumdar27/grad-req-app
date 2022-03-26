from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from typing import Optional, List
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    # print(posts)
    return posts

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # dont use f string coz it is vulnerable to SQLinjection attacks
    # cursor.execute(""" INSERT INTO posts (title, content, published) values (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # created_post = cursor.fetchone()
    # conn.commit()

    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=schemas.Post)
async def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts where id = %s """, (id,))
    # post = cursor.fetchone()

    qry = db.query(models.Post).filter(models.Post.id == id)
    post = qry.first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
         detail=f"Post for id: {id} was not found")
    
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first()==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
         detail=f"Post for id: {id} was not found")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()

    qry = db.query(models.Post).filter(models.Post.id==id)

    updated_post = qry.first()

    if not updated_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
         detail=f"Post for id: {id} was not found")
    
    qry.update(post.dict(), synchronize_session=False)
    db.commit()
    return qry.first()
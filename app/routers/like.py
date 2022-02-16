# NOTE: this is the like router file to handle all the likes routes operations

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, database, oauth2


# creates the router for the likes endpoints
router = APIRouter(
    prefix="/like",
    tags=["Likes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(like: schemas.Like, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()

    if not post:  # check if the post exists
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {like.post_id} does not exist')
    like_query = db.query(models.Like).filter(
        models.Like.user_id == current_user.id, models.Like.post_id == like.post_id)

    like_found = like_query.first()

    # if like is 1, then we want to check if the user has already liked the post
    if (like.dir == 1):
        if like_found:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'User with id:{current_user.id} already liked post with id:{like.post_id}')
        # if the user has not liked the post, then we can add the like
        new_like = models.Like(user_id=current_user.id, post_id=like.post_id)
        db.add(new_like)
        db.commit()
        return{"message": "Post liked"}

    # if like is 0, then we want to check if the user has already unliked the post
    elif (like.dir == 0):
        if not like_found:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'User with id:{current_user.id} has not liked post with id:{like.post_id}')
        # if the user has already liked the post, then we can remove the like
        like_query.delete(synchronize_session=False)
        db.commit()
        return{"message": "Post unliked"}

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Invalid like direction it should be 1 or 0')

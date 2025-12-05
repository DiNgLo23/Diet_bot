from fastapi import APIRouter
from app.db.crud import add_new_user, user_exists
from app.api.schemas import User


router = APIRouter(prefix="/users", tags=["users"])



@router.get("/{user_id}")
def user_exists_end(user_id:int):
    if user_exists(user_id):
        return {"message":True}
    return {"message":False}


@router.post("/")
def add_new_user_end(user:User):
    add_new_user(user.id,user.lang)
    return {"message":200}


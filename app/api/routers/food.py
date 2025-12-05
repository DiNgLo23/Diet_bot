from fastapi import APIRouter
from app.db.crud import add_food, get_food, log_food, get_day_log_food, add_search_log, search_log_exists, search_food
from pydantic import BaseModel
from app.api.schemas import Food, LogFood, SearchLog



router = APIRouter(prefix="/food", tags=["food"])



@router.get("/get_food/{id_food}")
def get_food_end(id_food:str):
    food = get_food(id_food)
    return {"message":food}


@router.get("/search_food")
def search_food_end(name: str):
    return {"message": search_food(name)}


@router.post("/add_food")
def add_food_end(food:Food):
    add_food(food)
    return {"message":200}


@router.get("/day_log_food/{user_id}/{date}")
def day_log_food_end(user_id,date):
    foods = get_day_log_food(user_id,date)
    if len(foods)>0:
        res = foods[0][4:]
        foods.pop(0)
        for i in foods:
            i = i[4:]
            res[0] += i[0]
            res[1] += i[1]
            res[2] += i[2]
            res[3] += i[3]
            res[4] += i[4]
        name = ["Ккал - ","Жиры - ","Углеводы - ","Белки - ", "Масса - "]
        res = "".join([name[i]+str(int(res[i]))+"\n" for i in range(len(res))])
        return {"message":res}
    return {"message":0}


@router.post("/log_food")
def log_food_end(food:LogFood):
    log_food(food)
    return {"message": 201}

@router.post("/add_search_log")
def add_search_log_end(search_log:SearchLog):
    add_search_log(search_log)
    return {"message":200}


@router.get("/search_log_exist/{mess}")
def search_log_exist(mess:str):
    return search_log_exists(mess)
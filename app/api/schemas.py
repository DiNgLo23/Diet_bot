from pydantic import BaseModel

class Food(BaseModel):
    id:str
    name:str
    energy:int
    fat:int
    carbohydrate:int
    protein:int


class User(BaseModel):
    id:int
    lang:str


class LogFood(BaseModel):
    id:str
    user_id:int
    date:int
    name:str
    energy:float
    fat:float
    carbohydrate:float
    protein:float
    mass:int


class SearchLog(BaseModel):
    user_id:int
    date:int
    mess:str
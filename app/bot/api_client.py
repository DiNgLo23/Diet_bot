import aiohttp
from typing import Optional, Dict, Any


class FoodBotApi:
    def __init__(self,base_url:str = "http://127.0.0.1:8000/"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None


    async def connect(self):
        self.session = aiohttp.ClientSession()


    async def disconnect(self):
        if self.session:
            await self.session.close()


    async def _request(self,method:str,endpoint:str, **kwargs) -> Dict[str,Any]:
        url = f"{self.base_url}{endpoint}"

        try:
            async with self.session.request(method, url, **kwargs) as response:
                if response.status==200:
                    return await response.json()
                else:
                    return {"error":f"Ошибка - {response.status}"}
        except Exception as e:
            return {"error":f"Ошибка подключения - {str(e)}"}

    ##################
    ### ПОЛЬЗОВАТЕЛИ
    ##################
    async def user_exist(self,user_id):
        return await self._request("GET",f"users/{user_id}")


    async def add_user(self, user:dict):
        return await self._request("POST",f"users",json=user)

    #########
    ### ЕДА
    #########
    async def get_food(self, food_id):
        return await self._request("GET",f"food/get_food/{food_id}")


    async def search_food(self, name):
        return await self._request("GET",f"food/search_food",params={"name":name})


    async def get_day_log_food(self,user_id,date):
        return await self._request("GET",f"food/day_log_food/{user_id}/{date}")

    async def log_food_ent(self, food:dict):
        return await self._request("POST",f"food/log_food",json=food)


    async def add_search_log(self,search_log:dict):
        return await self._request("POST",f"food/add_search_food",json=search_log)


    async def search_log_exist(self,mess:str):
        return await self._request("GET",f"food/search_log_exist/{mess}")



import requests
from bs4 import BeautifulSoup
#from main import lang

def get_foods(name: str):
    url = f"https://www.tablicakalorijnosti.ru/foodstuff/filter-list?format=json&page=0&limit=10000&query={name}&type=0&brand=&min=0&max=3800&sliderType=1"
    response = requests.get(url)
    data_en = dict(response.json())["data"]
    data_ru = [{} for i in range(len(data_en))]
    return data_en


# if lang == "ru":
#     for i in range(len(data_en)):
#         data_ru[i]["Название"] = data_en[i]["title"]
#         data_ru[i]["Энергия"] = data_en[i]["energy"]
#         data_ru[i]["Белок"] = data_en[i]["protein"]
#         data_ru[i]["protein"] = data_en[i]["protein"]
#         print(data_en[i])
#
#





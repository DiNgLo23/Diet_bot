import requests


def get_foods(name: str):
    url = f"https://www.tablicakalorijnosti.ru/foodstuff/filter-list?format=json&page=0&limit=10000&query={name}&type=0&brand=&min=0&max=3800&sliderType=1"
    response = requests.get(url)
    data_en = dict(response.json())["data"]
    return data_en







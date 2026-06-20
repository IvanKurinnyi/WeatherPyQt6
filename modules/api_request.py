import requests
import os
import json


def read_json(name_file: str) -> dict:
    with open(file=f"instances/{name_file}", mode="r", encoding='utf-8', errors='replace') as file:
        return json.load(file)

def create_json(data: dict, name_file:str):
    with open(file=f"instances/{name_file}", mode="w") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))

API_KEY = "d562486e64d8cd8b97cb68e1b245c4b4"#os.getenv("API_KEY") 


settings = read_json("settings.json")

lang = settings["language"]

def api_request(city:str, API_KEY:str, lang:str):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang={lang}"
        response = requests.get(url)
        response_dict = response.json()
        return response_dict
    except Exception as e:
        print("error")
        return []

def forecast_request(city:str, API_KEY:str, lang:str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang={lang}"
    response = requests.get(url)
    response_dict = response.json()
    return response_dict


#def country_request():
#    url = "https://countriesnow.space/api/v0.1/countries/positions"
#    response = requests.get(url)
#    response_dict = response.json()
#    return response_dict
#create_json(country_request(), "countries.json")


def get_coordinates(city:str):

    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"

    res = requests.get(url, headers={"User-Agent": "my-app"})
    data = res.json()

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    all_coordinates = f"{lat},{lon}"

    return all_coordinates

import requests
import os
import json


def create_json(data: dict, name_file:str):
    with open(file=f"{name_file}", mode="w") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))

API_KEY = os.getenv("API_KEY") 

def api_request(city:str, API_KEY:str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ua"
    response = requests.get(url)
    response_dict = response.json()
    return response_dict

def forecast_request(city:str, API_KEY:str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ua"
    response = requests.get(url)
    response_dict = response.json()
    return response_dict


def country_request():
    url = "https://countriesnow.space/api/v0.1/countries/positions"
    response = requests.get(url)
    response_dict = response.json()
    return response_dict

create_json(country_request(), "countries.json")


def get_coordinates(city:str):

    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"

    res = requests.get(url, headers={"User-Agent": "my-app"})
    data = res.json()

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    all_coordinates = f"{lat},{lon}"

    return all_coordinates

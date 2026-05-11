from .api import API_KEY
import requests


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
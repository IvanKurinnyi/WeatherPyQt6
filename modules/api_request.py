import requests
import os
import json

from .translations import LANG, api_lang_code


def read_json(name_file: str) -> dict:
    with open(file=f"instances/{name_file}", mode="r", encoding='utf-8', errors='replace') as file:
        return json.load(file)

def create_json(data: dict, name_file:str):
    with open(file=f"instances/{name_file}", mode="w") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))

try:
    CITIES = read_json("cities.json")
except Exception:
    CITIES = None

def _build_city_map(cities):
    m = {}
    if not cities:
        return m
    if isinstance(cities, list):
        for item in cities:
            if not isinstance(item, dict):
                continue
            name = (item.get("name") or "").strip()
            native = (item.get("native") or "").strip()
            if name:
                m[name.casefold()] = name
            if native:
                m[native.casefold()] = name
            trans = item.get("translations") or {}
            if isinstance(trans, dict):
                for v in trans.values():
                    if isinstance(v, str) and v.strip():
                        m[v.strip().casefold()] = name
    elif isinstance(cities, dict):
        for k, v in cities.items():
            if isinstance(k, str):
                m[k.strip().casefold()] = k
            if isinstance(v, str):
                m[v.strip().casefold()] = k
            if isinstance(v, dict):
                for vv in v.values():
                    if isinstance(vv, str):
                        m[vv.strip().casefold()] = k
    return m

CITY_MAP = _build_city_map(CITIES)

API_KEY = os.getenv("API_KEY")

settings = read_json("settings.json")




def get_city_display_name(city_obj: dict) -> str:
    
    if not isinstance(city_obj, dict):
        return ""
    if LANG.current == "en":
        return city_obj.get("name", "")
    translations = city_obj.get("translations")
    if isinstance(translations, dict):
        uk = translations.get("uk")
        if uk:
            return uk
    return city_obj.get("name", "")


def find_city_obj(city_name: str):
    if not city_name or not CITIES:
        return None
    target = city_name.strip().casefold()
    for c in CITIES:
        if not isinstance(c, dict):
            continue
        name = (c.get("name") or "").strip().casefold()
        if name == target:
            return c
        trans = c.get("translations") or {}
        if isinstance(trans, dict):
            uk = (trans.get("uk") or "").strip().casefold()
            if uk == target:
                return c
    return None


def display_name_for_any(city_name: str) -> str:
    city_obj = find_city_obj(city_name)
    if city_obj:
        return get_city_display_name(city_obj)
    return city_name


def get_api_city_name(display_city: str) -> str:
    if not display_city:
        return display_city
    key = display_city.strip().casefold()
    return CITY_MAP.get(key, display_city)

def _map_lang_for_api(lang_code: str) -> str:
    return api_lang_code(lang_code)

def api_request(city: str, API_KEY: str, lang: str = None):
    try:
        effective_lang = lang if lang is not None else LANG.current
        api_lang = _map_lang_for_api(effective_lang)
        city_for_api = get_api_city_name(city)
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_for_api}&appid={API_KEY}&units=metric&lang={api_lang}"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if isinstance(data, dict) and "main" in data:
            return data
        try:
            coords = get_coordinates(city_for_api)
        except Exception:
            try:
                coords = get_coordinates(city)
            except Exception:
                coords = None
        if coords:
            lat, lon = coords.split(",")
            url2 = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang={api_lang}"
            resp2 = requests.get(url2, timeout=5)
            return resp2.json()
        return data
    except Exception:
        return {}

def forecast_request(city: str, API_KEY: str, lang: str = None):
    effective_lang = lang if lang is not None else LANG.current
    api_lang = _map_lang_for_api(effective_lang)
    city_for_api = get_api_city_name(city)
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_for_api}&appid={API_KEY}&units=metric&lang={api_lang}"
    resp = requests.get(url)
    data = resp.json()
    if isinstance(data, dict) and "list" in data:
        return data
    try:
        coords = get_coordinates(city_for_api)
    except Exception:
        coords = None
    if coords:
        lat, lon = coords.split(",")
        url2 = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang={api_lang}"
        resp2 = requests.get(url2)
        return resp2.json()
    return data


def get_coordinates(city:str):

    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"

    res = requests.get(url, headers={"User-Agent": "my-app"})
    data = res.json()

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    all_coordinates = f"{lat},{lon}"

    return all_coordinates
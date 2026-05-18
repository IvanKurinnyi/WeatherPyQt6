import requests
import json

def search_api():
    url = "https://countriesnow.space/api/v0.1/countries/population/cities"
    response = requests.get(url)
    response_dict = response.json()
    with open(file="cites.json",mode="w") as file:
        file.write(json.dumps(obj=response_dict,indent=4))
search_api()
    

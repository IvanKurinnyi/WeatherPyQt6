def find_cities_by_prefix(cities: list, prefix: str, limit: int = 10) -> list:
    prefix_lower = prefix.lower()
    result = []
    
    for city_obj in cities:
        if 'name' not in city_obj:
            continue
            
        city_name = city_obj['name']
        if city_name.lower().startswith(prefix_lower):
            result.append(city_name.capitalize())
            
            if len(result) >= limit:
                break
    
    return result

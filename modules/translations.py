
from .read_write_json import read_json, create_json


TRANSLATIONS = {
    "en": {
        # --- общие ---
        "today": "Today",
        "search": "Search",
        "settings": "Settings",
        "add": "Add",
        "save": "Save",
        "max_min": "Max.: {max}°, min.: {min}°",
        "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"],

        # --- right_city_card.py ---
        "current_position": "Сurrent position",

        # --- forecast_time.py / forecast_graphic.py ---
        "now": "Now",
        "forecast_near_future": "Forecast for the near future",

        # --- top_search_bar.py: settings panel ---
        "results_of_search": "Results of the search",
        "menu_city_search": "Search of the city",
        "menu_resolution": "Window size",
        "menu_language": "Language",
        "menu_style": "Style",
        "city_search_title": "Search of the city",
        "country": "Country",
        "city": "City",
        "coordinates": "Coordinates",
        "choose_a_city": "Choose a city",
        "no_cities": "No cities",
        "added_cities": "Added cities",
        "choose_resolution": "Choose a size of the Application",
        "choose_language": "Choose a language",
        "language_label": "Language",
        "list_of_images": "List of the images",
        "images_list_n": "Images list №{n}",
    },
    "ua": {
        # --- общие ---
        "today": "Сьогоднi",
        "search": "Пошук",
        "settings": "Налаштування",
        "add": "Додати",
        "save": "Зберегти",
        "max_min": "Макс.: {max}°, мін.: {min}°",
        "weekdays": ["Понеділок", "Вівторок", "Середа", "Четвер",
                     "П'ятниця", "Субота", "Неділя"],

        # --- right_city_card.py ---
        "current_position": "Поточна позiцiя",

        # --- forecast_time.py / forecast_graphic.py ---
        "now": "Зараз",
        "forecast_near_future": "Прогноз на найближчий час",

        # --- top_search_bar.py: settings panel ---
        "results_of_search": "Результати пошуку",
        "menu_city_search": "Пошук міста",
        "menu_resolution": "Розмір Додатку",
        "menu_language": "Мова додатку",
        "menu_style": "Список зображень",
        "city_search_title": "Пошук міста",
        "country": "Країна",
        "city": "Місто",
        "coordinates": "Координати",
        "choose_a_city": "Виберіть місто",
        "no_cities": "Немає міст",
        "added_cities": "Додані міста",
        "choose_resolution": "Оберіть розмір додатку",
        "choose_language": "Оберіть мову додатку",
        "language_label": "Mовa додатку",
        "list_of_images": "Списки зображень",
        "images_list_n": "Cписок зображень {n}",
    },
}


def api_lang_code(lang_code: str) -> str:
    if not lang_code:
        return "en"
    if lang_code == "ua":
        return "uk"
    return lang_code


class LangState:
    

    def __init__(self, initial_lang: str):
        self.current = initial_lang
        self._listeners = []  

    def subscribe(self, callback):
        
        self._listeners.append(callback)

    def unsubscribe(self, callback):
        
        if callback in self._listeners:
            self._listeners.remove(callback)

    def set(self, new_lang: str, persist: bool = True):
        
        if new_lang == self.current:
            return

        self.current = new_lang

        if persist:
            try:
                settings = read_json("settings.json")
                settings["language"] = new_lang
                create_json(settings, "settings.json")
            except Exception as e:
                print(f"Не удалось сохранить язык в settings.json: {e}")

        
        for callback in list(self._listeners):
            try:
                callback()
            except RuntimeError:
                
                pass


def t(key: str) -> str:
    try:
        lang_dict = TRANSLATIONS.get(LANG.current, {})
        value = lang_dict.get(key)
        if value is None:
            value = TRANSLATIONS.get("en", {}).get(key)
        if value is None:
            return key
        return value
    except Exception:
        return key


def weekday_name(index: int) -> str:
    return TRANSLATIONS[LANG.current]["weekdays"][index]



try:
    _settings = read_json("settings.json")
    _initial_lang = _settings.get("language", "en")
except Exception:
    _initial_lang = "en"

LANG = LangState(_initial_lang)
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .title_bar import TitleBar
from .app import app
from .city_card import Card
from .toggle_switch_button import ToggleSwitch
import os
from .right_time_card import RightTimeCard
from .right_city_card import RightCityCard
from .top_search_bar import SearchBar
from .forecast_time import ForeCastTime
from .forecast_graphic import ForeCastGraph
import requests
from .read_write_json import read_json, create_json

class MainWindow(widget.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Weather App")
        font_path = os.path.join(os.path.dirname(__file__), "..", "media", "fonts", "Roboto-VariableFont_wdth,wght.ttf")
        font_id = gui.QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("Шрифт не найден")
            font_family = "Arial"
        else:
            font_family = gui.QFontDatabase.applicationFontFamilies(font_id)[0]
            

        self.roboto_font = gui.QFont(font_family, 16, 900)

        json_res = read_json(name_file="settings.json")

        self.WIDTH = int(json_res["currentResolution"][0])
        self.HEIGHT = int(json_res["currentResolution"][1])
        self.X = (app.primaryScreen().size().width() - self.WIDTH) // 2
        self.Y = (app.primaryScreen().size().height() - self.HEIGHT) // 2
        self.setGeometry(self.X, self.Y, self.WIDTH, self.HEIGHT)

        self.CENTRAL_WIDGET = widget.QWidget()
        
        self.GRADIENT = gui.QLinearGradient(1200, 0, 0, 830)
        self.GRADIENT.setColorAt(0.0, gui.QColor("#FFDF56"))
        self.GRADIENT.setColorAt(1.0, gui.QColor("#87CEFA"))
        
        self.PALETTE = gui.QPalette()
        self.PALETTE.setBrush(gui.QPalette.ColorRole.Window, gui.QBrush(self.GRADIENT))
        self.CENTRAL_WIDGET.setPalette(self.PALETTE)
        self.CENTRAL_WIDGET.setAutoFillBackground(True)

        self.setCentralWidget(self.CENTRAL_WIDGET)
        
        self.LAYOUT = widget.QVBoxLayout(self.CENTRAL_WIDGET)
        self.LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.LAYOUT.setSpacing(0)
        self.CENTRAL_WIDGET.setLayout(self.LAYOUT)

        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        
        self.CENTRAL_FRAME = widget.QFrame(self.CENTRAL_WIDGET)
        self.LAYOUT.addWidget(self.CENTRAL_FRAME)
        
        self.TITLE_BAR = TitleBar(self)
        self.TITLE_BAR.setGeometry(0, 0, self.WIDTH, 20)
        
        self.TITLE_BAR.raise_() 
        self.CENTRAL_LAYOUT = widget.QHBoxLayout(self.CENTRAL_FRAME)
        self.CENTRAL_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CENTRAL_LAYOUT.setSpacing(0)
        self.CENTRAL_FRAME.setLayout(self.CENTRAL_LAYOUT)

        self.LEFT_FRAME = widget.QFrame(self.CENTRAL_FRAME)
        self.LEFT_FRAME.setStyleSheet("background-color: rgba(0,0,0,0.4)")
        self.LEFT_FRAME.setFixedWidth(370)
        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT_FRAME)
        self.LEFT_LAYOUT.setContentsMargins(20, 37, 20, 20)
        self.LEFT_LAYOUT.setSpacing(20)
        self.LEFT_FRAME.setLayout(self.LEFT_LAYOUT)


        self.RIGHT_FRAME = widget.QFrame(self.CENTRAL_FRAME)
        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT_FRAME)
        self.RIGHT_FRAME.setLayout(self.RIGHT_LAYOUT)
        self.RIGHT_LAYOUT.setContentsMargins(20,30,20,0)
        self.RIGHT_LAYOUT.setSpacing(0)

        self.CENTRAL_LAYOUT.addWidget(self.LEFT_FRAME)
        self.CENTRAL_LAYOUT.addWidget(self.RIGHT_FRAME, stretch=1)


        self.TOGGLE_SWITCH = ToggleSwitch(self.LEFT_FRAME)
        self.LEFT_LAYOUT.addWidget(self.TOGGLE_SWITCH, alignment=core.Qt.AlignmentFlag.AlignRight)

        self.RIGHT_CARDS_FRAME = widget.QFrame(self.RIGHT_FRAME)
        # self.RIGHT_CARDS_FRAME.setMinimumSize(core.QSize(788, 733)) 
        self.RIGHT_LAYOUT.addWidget(self.RIGHT_CARDS_FRAME, stretch=1)
        
        self.RIGHT_CARDS_LAYOUT = widget.QVBoxLayout(self.RIGHT_CARDS_FRAME)
        self.RIGHT_CARDS_FRAME.setLayout(self.RIGHT_CARDS_LAYOUT)
        self.RIGHT_CARDS_LAYOUT.setContentsMargins(0,20,0,37)
        self.RIGHT_CARDS_LAYOUT.setSpacing(10)

        self.SEARCH_BAR = SearchBar(parent = self.RIGHT_CARDS_FRAME)
        self.RIGHT_CARDS_LAYOUT.addWidget(self.SEARCH_BAR)
        self.RIGHT_CARDS_LAYOUT.addSpacing(10)

        self.SEARCH_BAR.city_selected.connect(self.show_city_weather)
        self.SEARCH_BAR.city_added.connect(self.on_city_added)
        self.SEARCH_BAR.resolution_changed.connect(self.update_window_resolution)
        
        
        
        self.RIGHT_INFO_FRAME = widget.QFrame(self.RIGHT_CARDS_FRAME)
        # self.RIGHT_INFO_FRAME.setMinimumSize(core.QSize(788, 303))
        self.RIGHT_CARDS_LAYOUT.addWidget(self.RIGHT_INFO_FRAME)


        self.RIGHT_INFO_LAYOUT = widget.QHBoxLayout(self.RIGHT_INFO_FRAME)
        self.RIGHT_INFO_LAYOUT.setContentsMargins(0,0,0,0)

        
        self.RIGHT_CITY_CARD = RightCityCard(self.RIGHT_CARDS_FRAME)
        self.RIGHT_CITY_CARD.setFont(self.roboto_font)
        self.RIGHT_INFO_LAYOUT.addWidget(self.RIGHT_CITY_CARD, stretch=1)
        
        self.CITY_TIME_CARD = RightTimeCard(self.RIGHT_CARDS_FRAME)
        self.CITY_TIME_CARD.setFont(self.roboto_font)
        self.RIGHT_INFO_LAYOUT.addWidget(self.CITY_TIME_CARD, stretch=1)

        
        self.FORECAST_TIME = ForeCastTime(city_name = "Paris")
        self.RIGHT_CARDS_LAYOUT.addWidget(self.FORECAST_TIME)


        self.FORECAST_GRAPH = ForeCastGraph(city_name=None)
        self.RIGHT_CARDS_LAYOUT.addWidget(self.FORECAST_GRAPH, stretch=1)



        self.SCROLL_AREA = widget.QScrollArea(parent=self)
        self.SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL_AREA.setStyleSheet("background-color: rgba(0,0,0,0); border: none")
        self.LEFT_LAYOUT.addWidget(self.SCROLL_AREA)
        self.SCROLL_AREA.setWidgetResizable(True)
        
        self.SCROLL_FRAME = widget.QFrame(parent=self.SCROLL_AREA)
        self.SCROLL_LAYOUT = widget.QVBoxLayout()
        self.SCROLL_LAYOUT.setContentsMargins(0,0,0,0)
        self.SCROLL_LAYOUT.setSpacing(5)
        self.SCROLL_FRAME.setLayout(self.SCROLL_LAYOUT)
        self.SCROLL_AREA.setWidget(self.SCROLL_FRAME)
        
        self.cards = []
        self.selected_card = None
        current_city = self.city_request()
        
        # create_json(data=["Dnipro","Kyiv","Odessa"] ,name_file="city.json")
        city = read_json(name_file="city.json")

        
        city_list = [current_city]
        
        for i in city:
            city_list.append(i)

        for city in city_list:
            card = Card(parent = self.SCROLL_FRAME, city_name=city, scroll_frame=self.SCROLL_FRAME)
            card.setFont(self.roboto_font)
            self.cards.append(card)
            card.selected.connect(lambda c=card: self._on_card_selected(c))
            self.SCROLL_LAYOUT.addWidget(card, alignment=core.Qt.AlignmentFlag.AlignCenter)
            card.line(scroll_layout=self.SCROLL_LAYOUT)
            
        self.SCROLL_LAYOUT.addStretch(1)
        
    
    def show_city_weather(self, city_name):
        self.current_preview_city = city_name 

        self.RIGHT_CITY_CARD.update_city_data(city_name)
        self.CITY_TIME_CARD.minute_update(city_name)
        self.FORECAST_TIME.update_city_time(city_name)
        self.FORECAST_GRAPH.update_forecast(city_name)


        for card in self.cards:
            if card.city_name.lower() == city_name.lower():
                if self.selected_card and self.selected_card != card:
                    self.selected_card.deselect()
                self.selected_card = card
                return

        if self.selected_card:
            self.selected_card.deselect()
            self.selected_card = None
        
    def _on_card_selected(self, card):
        if self.selected_card is not None and self.selected_card != card:
            self.selected_card.deselect()
        self.selected_card = card
        city_name = card.city_name
        self.RIGHT_CITY_CARD.update_city_data(city_name)
        self.CITY_TIME_CARD.minute_update(city_name)
        self.FORECAST_TIME.update_city_time(city_name)
        self.FORECAST_GRAPH.update_forecast(city_name)

    def on_city_added(self, city_name):
        card = Card(parent=self.SCROLL_FRAME, city_name=city_name, scroll_frame=self.SCROLL_FRAME)
        card.setFont(self.roboto_font)
        self.cards.append(card)
        card.selected.connect(lambda c=card: self._on_card_selected(c))
        
        self.SCROLL_LAYOUT.insertWidget(self.SCROLL_LAYOUT.count() - 1, card)
        card.line(scroll_layout=self.SCROLL_LAYOUT)
        
        self.show_city_weather(city_name)

    def update_window_resolution(self, width, height):
        
        self.WIDTH = width
        self.HEIGHT = height
        
     
        self.X = (app.primaryScreen().size().width() - self.WIDTH) // 2
        self.Y = (app.primaryScreen().size().height() - self.HEIGHT) // 2
        
        
        self.setGeometry(self.X, self.Y, self.WIDTH, self.HEIGHT)
        
        
        self.TITLE_BAR.setGeometry(0, 0, self.WIDTH, 20)

    def city_request(self):
        try:
            response = requests.get("https://ipinfo.io/json", timeout=5)
            data_dict = response.json()
            return data_dict.get("city", "Dnipro")
        except Exception:
            return "Dnipro"

window = MainWindow()
        
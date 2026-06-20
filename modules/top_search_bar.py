import PyQt6.QtWidgets as widget
import PyQt6.QtWebEngineWidgets as web_engine
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtSvgWidgets import QSvgWidget
import folium, io
from .find_town import find_cities_by_prefix
from .read_write_json import create_json, read_json
from .combobox import ComboBox
from .api_request import get_coordinates, lang
import requests
import csv

class SearchBar(widget.QFrame):
    city_selected = core.pyqtSignal(str, str)
    city_added = core.pyqtSignal(str)
    city_removed = core.pyqtSignal(str) 
    resolution_changed = core.pyqtSignal(int, int)  
    language_changed = core.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.CITIES_DATA = read_json("cities.json")
        self._blur_label = None
        self.DYNAMIC_LABELS = []

        self.CITY_NAMES = [
            c.get("name", "").lower() 
            for c in self.CITIES_DATA 
            if isinstance(c, dict) and c.get("name") is not None
        ]

        self.UA_CITIES = [
            c.get("translations", {}).get("uk", "").lower() 
            for c in self.CITIES_DATA 
            if isinstance(c, dict) and isinstance(c.get("translations"), dict) and c.get("translations").get("uk") is not None
        ]

        self.setFixedHeight(36)
        self.setMinimumWidth(788)
        self.setStyleSheet("background-color:none")
        
        self.LAYOUT = widget.QHBoxLayout(self)
        self.LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.LAYOUT.setSpacing(10)
        
        self.SETTINGS_FRAME = widget.QFrame(self)
        self.LAYOUT.addWidget(self.SETTINGS_FRAME)

        self.S_LAYOUT = widget.QHBoxLayout(self.SETTINGS_FRAME)
        self.S_LAYOUT.setContentsMargins(0, 0, 0, 0)
        
        self.SETTINGS = widget.QPushButton(self.SETTINGS_FRAME)
        self.SETTINGS.setFixedSize(core.QSize(32,32))
        self.SETTINGS.setStyleSheet("background-color: rgba(0,0,0,0.2)")
        self.SETTINGS_LAYOUT = widget.QVBoxLayout(self.SETTINGS)
        self.SETTINGS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.SETTINGS_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.SETTINGS_LAYOUT.setSpacing(0)
        self.S_LAYOUT.addWidget(self.SETTINGS)

        self.SETTINGS_ICON = QSvgWidget("media/right_frame/settings.svg", self.SETTINGS)
        self.SETTINGS_ICON.setStyleSheet("background-color:none;")
        self.SETTINGS_ICON.setFixedSize(core.QSize(16,16))
        self.SETTINGS_LAYOUT.addWidget(self.SETTINGS_ICON)
        
        self.SETTINGS_label = widget.QLabel("Налаштування", self.SETTINGS_FRAME)
        self.SETTINGS_label.setStyleSheet("font-size:14px; font-weight:500;")
        self.S_LAYOUT.addWidget(self.SETTINGS_label)

        self.LAYOUT.addStretch(1) 
       
        self.ADD_BUTTON = widget.QPushButton(self)    
        self.ADD_BUTTON.setFixedSize(core.QSize(97, 36))
        self.ADD_BUTTON.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        self.ADD_LAYOUT = widget.QHBoxLayout(self.ADD_BUTTON)
        self.ADD_LAYOUT.setContentsMargins(10, 0, 10, 0)
        self.ADD_LAYOUT.setSpacing(6)
        self.ADD_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.ADD_ICON = QSvgWidget("media/search_bar/plus.svg", self.ADD_BUTTON)
        self.ADD_ICON.setFixedSize(core.QSize(16, 16))
        
        if lang == "en":
            self.ADD_TEXT = widget.QLabel("Add", self.ADD_BUTTON)
        else: 
            self.ADD_TEXT = widget.QLabel("Додати", self.ADD_BUTTON)
        self.ADD_TEXT.setStyleSheet("color: white; font-size: 14px; font-weight: 500; background: none;")
        
        self.ADD_LAYOUT.addWidget(self.ADD_ICON)
        self.ADD_LAYOUT.addWidget(self.ADD_TEXT)
        self.LAYOUT.addWidget(self.ADD_BUTTON)
        self.ADD_BUTTON.hide()
        self.ADD_BUTTON.clicked.connect(self.add_city)

        self.SEARCH = widget.QFrame(self)
        self.SEARCH.setFixedSize(core.QSize(261,36))
        self.SEARCH.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 4px;")
        self.LAYOUT.addWidget(self.SEARCH)
        
        self.SEARCH_LAYOUT = widget.QHBoxLayout(self.SEARCH)
        self.SEARCH_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.IMG = widget.QLabel(self.SEARCH)
        self.IMG.setFixedSize(core.QSize(22,22))
        self.IMG.setStyleSheet("background-color: none; margin-top: -3px;")
        self.PIXMAP = gui.QPixmap("media/right_frame/Search.svg")
        self.IMG.setPixmap(self.PIXMAP)
        self.SEARCH_LAYOUT.addWidget(self.IMG)
        
        self.SEARCH_LINE = widget.QLineEdit(self.SEARCH)
        self.SEARCH_LINE.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
            }
        """)
        if lang == "en":
            self.SEARCH_LINE.setPlaceholderText("Search")
        else:
            self.SEARCH_LINE.setPlaceholderText("Пошук")
        self.SEARCH_LAYOUT.addWidget(self.SEARCH_LINE)

        self.CLEAR = widget.QPushButton(self.SEARCH)
        self.CLEAR.setFixedSize(core.QSize(22,22))
        self.CLEAR.setStyleSheet("""
            QPushButton {
                background-color: none; 
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 3px;
            }
        """)
        self.CLEAR.setIcon(gui.QIcon("media/search_bar/Clear.svg"))
        self.CLEAR.setIconSize(core.QSize(22, 22))
        self.SEARCH_LAYOUT.addWidget(self.CLEAR, alignment=core.Qt.AlignmentFlag.AlignRight)
        self.CLEAR.hide()
        self.CLEAR.clicked.connect(self.clear_search_line)

        self.POPUP = widget.QWidget(self) 
        self.POPUP.setObjectName("PopupMain")
        
        self.POPUP.setWindowFlags(
            core.Qt.WindowType.Window | 
            core.Qt.WindowType.FramelessWindowHint |
            core.Qt.WindowType.WindowStaysOnTopHint |
            core.Qt.WindowType.WindowDoesNotAcceptFocus |
            core.Qt.WindowType.NoDropShadowWindowHint
        )
        self.POPUP.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.POPUP.setStyleSheet("""
            #PopupMain { 
                background: transparent; 
                border: none; 
            }
        """)
        self.POPUP.setMinimumWidth(261)
        
        self.POPUP_MAIN_LAYOUT = widget.QVBoxLayout(self.POPUP)
        self.POPUP_MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)

        self.POPUP_FRAME = widget.QFrame(self.POPUP)
        self.POPUP_FRAME.setObjectName("PopupFrame")
        self.POPUP_FRAME.setFrameShape(widget.QFrame.Shape.NoFrame)
        
        self.POPUP_FRAME.setStyleSheet("""
            #PopupFrame {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 10px; 
                border: none; 
            }
        """)
        self.POPUP_FRAME.setMinimumWidth(261)

        self.POPUP_MAIN_LAYOUT.addWidget(self.POPUP_FRAME)

        self.POPUP_LAYOUT = widget.QVBoxLayout(self.POPUP_FRAME)
        self.POPUP_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        if lang == "en":
            self.RESULTS = widget.QLabel("Results of the search", self.POPUP_FRAME)
        else:
            self.RESULTS = widget.QLabel("Результати пошуку", self.POPUP_FRAME)
        self.RESULTS.setStyleSheet("background-color: none; color: white; padding-left: 5px; border: none;")
        self.POPUP_LAYOUT.addWidget(self.RESULTS)
        self.POPUP.hide()
        
        self.SEARCH_LINE.textChanged.connect(self.on_text_changed)
        widget.QApplication.instance().installEventFilter(self)
        
        self.SETTINGS_POPUP = widget.QFrame()
        self.SETTINGS_POPUP.setFixedSize(core.QSize(790, 688))
        self.SETTINGS_POPUP.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.SETTINGS_POPUP.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.SETTINGS_POPUP.setStyleSheet("background-color: none; border-radius: 10px; border: none;")
        self.SETTINGS_POPUP.raise_()
        self.SETTINGS_POPUP_FRAME = widget.QFrame(self.SETTINGS_POPUP)
        self.SETTINGS_POPUP_FRAME.setStyleSheet("background-color: rgba(0, 0, 0, 0.8); border-radius: 10px; border: none;")
        
        self.SETTINGS_POPUP_LAYOUT = widget.QVBoxLayout(self.SETTINGS_POPUP_FRAME)
        self.SETTINGS_POPUP_LAYOUT.setContentsMargins(24,24,24,24)
        self.SETTINGS_POPUP_LAYOUT.setSpacing(34)
        self.TITLE_SETT = widget.QFrame()
        self.TITLE_SETT.setStyleSheet("background-color: none")
        self.TITLE_SETT.setFixedSize(core.QSize(742, 28))
        self.SETTINGS_POPUP_LAYOUT.addWidget(self.TITLE_SETT, alignment=core.Qt.AlignmentFlag.AlignCenter)
        
        self.T_LAYOUT = widget.QHBoxLayout(self.TITLE_SETT)
        self.T_LAYOUT.setContentsMargins(0,0,0,0)

        if lang == "en":
            self.TITLE_LABEL = widget.QLabel("Settings")
        else:
            self.TITLE_LABEL = widget.QLabel("Налаштування")
            
        self.TITLE_LABEL.setStyleSheet("font-size:24px; font-weight:500")
        self.T_LAYOUT.addWidget(self.TITLE_LABEL)
        
        self.CLOSE_BUTTON = widget.QPushButton()
        self.CLOSE_BUTTON.setIcon(gui.QIcon("media/search_bar/close.svg"))
        self.CLOSE_BUTTON.setIconSize(core.QSize(16, 16))
        self.T_LAYOUT.addWidget(self.CLOSE_BUTTON, alignment=core.Qt.AlignmentFlag.AlignRight)

        self.CENTRAL_FRAME = widget.QFrame()
        self.CENTRAL_FRAME.setStyleSheet("background-color:none")
        self.CENTRAL_FRAME.setFixedSize(core.QSize(742, 578))
        self.SETTINGS_POPUP_LAYOUT.addWidget(self.CENTRAL_FRAME, alignment=core.Qt.AlignmentFlag.AlignCenter)

        self.CENTRAL_LAYOUT = widget.QHBoxLayout(self.CENTRAL_FRAME)
        self.CENTRAL_LAYOUT.setContentsMargins(0,0,0,0)
        self.CENTRAL_LAYOUT.setSpacing(24)

        self.LEFT_SETTINGS_FRAME = widget.QFrame()
        self.LEFT_SETTINGS_FRAME.setStyleSheet("background-color: none; border-radius: 0px; border-right: 1px solid rgba(255, 255, 255, 0.2)")
        self.LEFT_SETTINGS_FRAME.setFixedSize(core.QSize(174, 578))
        self.LEFT_SETTINGS_LAYOUT = widget.QVBoxLayout(self.LEFT_SETTINGS_FRAME)
        self.LEFT_SETTINGS_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.LEFT_SETTINGS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.LEFT_SETTINGS_LAYOUT.setSpacing(0)
        self.CENTRAL_LAYOUT.addWidget(self.LEFT_SETTINGS_FRAME)
        
        if lang == "en":
            self.CITY_SEARCH = widget.QPushButton("Search of the city")
            self.RESOLUTION = widget.QPushButton("Window size")
            self.LANGUAGE = widget.QPushButton("Language")
            self.IMG_LIST = widget.QPushButton("Style")
        else:
            self.CITY_SEARCH = widget.QPushButton("Пошук міста")
            self.RESOLUTION = widget.QPushButton("Розмір Додатку")
            self.LANGUAGE = widget.QPushButton("Мова додатку")
            self.IMG_LIST = widget.QPushButton("Список зображень")
        
        self.CITY_SEARCH.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:0px; text-align: left; padding-left: 8px;")
        self.CITY_SEARCH.setFixedSize(core.QSize(158, 35))
        
        self.RESOLUTION.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:0px; text-align: left; padding-left: 8px;")
        self.RESOLUTION.setFixedSize(core.QSize(158, 35))

        self.LANGUAGE.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:0px; text-align: left; padding-left: 8px;")
        self.LANGUAGE.setFixedSize(core.QSize(158, 35))
        
        self.IMG_LIST.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:0px; text-align: left; padding-left: 8px;")
        self.IMG_LIST.setFixedSize(core.QSize(158, 35))

        self.LEFT_SETTINGS_LAYOUT.addWidget(self.CITY_SEARCH)
        self.LEFT_SETTINGS_LAYOUT.addWidget(self.RESOLUTION)
        self.LEFT_SETTINGS_LAYOUT.addWidget(self.LANGUAGE)
        self.LEFT_SETTINGS_LAYOUT.addWidget(self.IMG_LIST)
        
        self.RIGHT_FRAME = widget.QFrame()
        self.RIGHT_FRAME.setStyleSheet("background-color:none")
        self.RIGHT_FRAME.setFixedSize(core.QSize(544, 578))
        self.CENTRAL_LAYOUT.addWidget(self.RIGHT_FRAME)
        
        self.CITY_SEARCH_FRAME = widget.QFrame(self.RIGHT_FRAME)
        self.CITY_SEARCH_LAYOUT = widget.QVBoxLayout(self.CITY_SEARCH_FRAME)
        self.CITY_SEARCH_LAYOUT.setContentsMargins(0,0,0,0)
        
        if lang == "en":
            self.CITY_SEARCH_LABEL = widget.QLabel("Search of the city", self.CITY_SEARCH_FRAME)
        else:
            self.CITY_SEARCH_LABEL = widget.QLabel("Пошук міста", self.CITY_SEARCH_FRAME)
        self.CITY_SEARCH_LABEL.setStyleSheet("background-color: none; color: white; font-size: 18px; font-weight: 400;")
        self.CITY_SEARCH_LAYOUT.addWidget(self.CITY_SEARCH_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.MAP_FRAME = widget.QFrame()
        self.MAP_FRAME.setFixedSize(core.QSize(544, 256))
        self.CITY_SEARCH_LAYOUT.addWidget(self.MAP_FRAME)

        self.MAP_LAYOUT = widget.QHBoxLayout(self.MAP_FRAME)
        self.MAP_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAP_LAYOUT.setSpacing(16)

        self.COUNTRY_FRAME = widget.QLabel()
        self.COUNTRY_FRAME.setFixedSize(core.QSize(239, 256))
        self.MAP_LAYOUT.addWidget(self.COUNTRY_FRAME)

        self.WEB_VIEW = web_engine.QWebEngineView()
        self.WEB_VIEW.setFixedSize(core.QSize(289, 256))
        self.MAP_LAYOUT.addWidget(self.WEB_VIEW)

        self.WEBMAP = folium.Map(location=(80, 60))
        data = io.BytesIO()
        self.WEBMAP.save(data, close_file=False)
        self.WEB_VIEW.setHtml(data.getvalue().decode())

        self.COUNTRY_LAYOUT = widget.QVBoxLayout(self.COUNTRY_FRAME)
        self.COUNTRY_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.COUNTRY_LAYOUT.setSpacing(8)

        self.COUNTRY_GROUP_FRAME = widget.QFrame()
        self.COUNTRY_GROUP_LAYOUT = widget.QVBoxLayout(self.COUNTRY_GROUP_FRAME)
        self.COUNTRY_GROUP_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.COUNTRY_GROUP_LAYOUT.setSpacing(4)
        self.COUNTRY_LAYOUT.addWidget(self.COUNTRY_GROUP_FRAME)

        countrys_json = read_json("countries.json")
        settings = read_json("settings.json")

        # countries.json теперь хранит список стран с готовыми полями:
        # id, name_en, name_ua, iso2, latitude, longitude.
        # Строим список для комбобокса и словарь "отображаемое имя -> id",
        # чтобы потом находить города по country_id, а не по сравнению строк.
        self.COUNTRY_NAME_TO_ID = {}
        countries = []

        for country in countrys_json:
            if not isinstance(country, dict):
                continue

            if settings["language"] == "ua":
                display_name = country.get("name_ua") or country.get("name_en", "")
            else:
                display_name = country.get("name_en", "")

            if not display_name:
                continue

            countries.append(display_name)
            self.COUNTRY_NAME_TO_ID[display_name] = country.get("id")



        if lang == "en":
            self.COUNTRY_LABEL = widget.QLabel("Country")
        else:
            self.COUNTRY_LABEL = widget.QLabel("Країна")
            
        self.COUNTRY_LABEL.setStyleSheet("color:white; font-weight:500;font-size:14px;text-align: left;")
        self.COUNTRY_LABEL.setFixedSize(core.QSize(249, 14))
        self.COUNTRY_GROUP_LAYOUT.addWidget(self.COUNTRY_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.COUNTRY_COMBOBOX = ComboBox(layout=self.COUNTRY_GROUP_LAYOUT, items=countries)

        self.CITY_GROUP_FRAME = widget.QFrame()
        self.CITY_GROUP_LAYOUT = widget.QVBoxLayout(self.CITY_GROUP_FRAME)
        self.CITY_GROUP_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CITY_GROUP_LAYOUT.setSpacing(4)
        self.COUNTRY_LAYOUT.addWidget(self.CITY_GROUP_FRAME)

        if lang == "en":
            self.CITY_LABEL = widget.QLabel("City")
        else:
            self.CITY_LABEL = widget.QLabel("Місто")
            
        self.CITY_LABEL.setStyleSheet("color:white; font-weight:500;font-size:14px;text-align: left;")
        self.CITY_LABEL.setFixedSize(core.QSize(249, 14))
        self.CITY_GROUP_LAYOUT.addWidget(self.CITY_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)
        
        if lang == "en":
            self.CITY_COMBOBOX = ComboBox(layout=self.CITY_GROUP_LAYOUT, items=["Choose a city"])
        else:
            self.CITY_COMBOBOX = ComboBox(layout=self.CITY_GROUP_LAYOUT, items=["Виберіть місто"])
            
        self.COUNTRY_COMBOBOX.currentTextChanged.connect(self.update_cities_by_country)

        if self.COUNTRY_COMBOBOX.count() > 0:
            self.update_cities_by_country(self.COUNTRY_COMBOBOX.currentText())

        self.COORDS_GROUP_FRAME = widget.QFrame()
        self.COORDS_GROUP_LAYOUT = widget.QVBoxLayout(self.COORDS_GROUP_FRAME)
        self.COORDS_GROUP_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.COORDS_GROUP_LAYOUT.setSpacing(4)
        self.COUNTRY_LAYOUT.addWidget(self.COORDS_GROUP_FRAME)

        if lang == "en":
            self.COORDS_LABEL = widget.QLabel("Coordinates")
        else:
            self.COORDS_LABEL = widget.QLabel("Координати")
            
        self.COORDS_LABEL.setStyleSheet("color:white; font-weight:500;font-size:14px;text-align: left;")
        self.COORDS_LABEL.setFixedSize(core.QSize(249, 14))
        self.COORDS_GROUP_LAYOUT.addWidget(self.COORDS_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.COORDS_QLINEEDIT = widget.QLineEdit()
        self.COORDS_QLINEEDIT.setFixedSize(core.QSize(239, 32))
        self.COORDS_QLINEEDIT.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                border: none;
                border-radius: 4px;
                color: rgba(113, 113, 122, 1);
            }
        """)
        self.COORDS_GROUP_LAYOUT.addWidget(self.COORDS_QLINEEDIT)
        
        self.CITY_COMBOBOX.currentTextChanged.connect(self.update_coordinates_display)
        self.CITY_COMBOBOX.currentTextChanged.connect(self.update_city_map)

        if lang == "en":
            self.SAVE_MAP_BUTTON = widget.QPushButton("Save", self.COUNTRY_FRAME)
        else:
            self.SAVE_MAP_BUTTON = widget.QPushButton("Зберегти", self.COUNTRY_FRAME)
            
        self.SAVE_MAP_BUTTON.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 4px;
                border: none;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.SAVE_MAP_BUTTON.setFixedSize(core.QSize(105, 38))
        self.SAVE_MAP_BUTTON.clicked.connect(self.save_selected_city)
        self.COUNTRY_LAYOUT.addWidget(self.SAVE_MAP_BUTTON, alignment=core.Qt.AlignmentFlag.AlignLeft)
        
        if lang == "en":
            self.ADDED_CITIES_LABEL = widget.QLabel("Added cities")
        else:
            self.ADDED_CITIES_LABEL = widget.QLabel("Додані міста")
            
        self.ADDED_CITIES_LABEL.setStyleSheet("color:white; font-weight:400;font-size:18px;text-align: left;")
        self.CITY_SEARCH_LAYOUT.addWidget(self.ADDED_CITIES_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.SCROLL_AREA = widget.QScrollArea(parent=self)
        self.SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL_AREA.setWidgetResizable(True)

        self.SCROLL_AREA.setFixedSize(core.QSize(544, 160))

        self.SCROLL_AREA.setStyleSheet("""
            QScrollArea { background-color: rgba(0, 0, 0, 0.2); border: none; }
            QScrollArea > QWidget > QWidget { background: transparent; }
        """)

        self.CITY_SEARCH_LAYOUT.addWidget(self.SCROLL_AREA, alignment=core.Qt.AlignmentFlag.AlignLeft)


        self.ADDED_CITIES_FRAME = widget.QFrame()
        self.ADDED_CITIES_FRAME.setStyleSheet("background: transparent;")

        self.ADDED_CITIES_LAYOUT = widget.QVBoxLayout(self.ADDED_CITIES_FRAME)
        self.ADDED_CITIES_LAYOUT.setContentsMargins(16, 16, 16, 16)
        self.ADDED_CITIES_LAYOUT.setSpacing(0)

        self.ADDED_CITIES_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        self.SCROLL_AREA.setWidget(self.ADDED_CITIES_FRAME)

        
        try:
            cities = read_json(f"city_{lang}.json")
        except:
            cities = []
        
        self.CITIES_LIST = cities
        self.added_city_frames = {}
        
        for city in self.CITIES_LIST:
            self.update_added_cities(city)
            
        self.CITY_SEARCH_FRAME.hide()

        self.RESOLUTION_FRAME = widget.QFrame(self.RIGHT_FRAME)
        self.RESOLUTION_LAYOUT = widget.QVBoxLayout(self.RESOLUTION_FRAME)
        self.RESOLUTION_LAYOUT.setContentsMargins(0,0,0,0)
        
        if lang == "en":
            self.RESOLUTION_LABEL = widget.QLabel("Choose a size of the Application", self.RESOLUTION_FRAME)
        else:
            self.RESOLUTION_LABEL = widget.QLabel("Оберіть розмір додатку", self.RESOLUTION_FRAME)
        
        self.RESOLUTION_LABEL.setStyleSheet("background-color: none; color: white; font-size: 18px; font-weight: 400;")
        self.RESOLUTION_LAYOUT.addWidget(self.RESOLUTION_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.FRAME_CENTRAL = widget.QFrame()
        self.FRAME_CENTRAL.setFixedSize(core.QSize(544, 174))
        self.RESOLUTION_LAYOUT.addWidget(self.FRAME_CENTRAL)
        self.FRAME_CENTRAL_LAYOUT = widget.QVBoxLayout(self.FRAME_CENTRAL)
        self.FRAME_CENTRAL_LAYOUT.setContentsMargins(0,0,0,0)
        self.FRAME_CENTRAL_LAYOUT.setSpacing(24)
        
        self.RADIO_BUTTONS_FRAME = widget.QFrame(self.FRAME_CENTRAL)
        self.RADIO_BUTTONS_FRAME.setFixedSize(core.QSize(544, 122))
        self.FRAME_CENTRAL_LAYOUT.addWidget(self.RADIO_BUTTONS_FRAME)

        self.FRAME_RADIOBUTTONS_LAYOUT = widget.QVBoxLayout(self.RADIO_BUTTONS_FRAME)
        self.FRAME_RADIOBUTTONS_LAYOUT.setContentsMargins(0,0,0,0)
        self.FRAME_RADIOBUTTONS_LAYOUT.setSpacing(8)

        self.RADIO_1 = widget.QRadioButton("1200x800", self.RADIO_BUTTONS_FRAME)
        self.RADIO_2 = widget.QRadioButton("1440x1024", self.RADIO_BUTTONS_FRAME)
        self.RADIO_3 = widget.QRadioButton("1512x982", self.RADIO_BUTTONS_FRAME)
        self.RADIO_4 = widget.QRadioButton("1728x1117", self.RADIO_BUTTONS_FRAME)

        radio_buttons = [self.RADIO_1, self.RADIO_2, self.RADIO_3, self.RADIO_4]

        self.RAIDO_BUTTONS_GROUP = widget.QButtonGroup(self.RADIO_BUTTONS_FRAME)
        for rb in radio_buttons:
            self.FRAME_RADIOBUTTONS_LAYOUT.addWidget(rb, alignment=core.Qt.AlignmentFlag.AlignLeft)
            self.RAIDO_BUTTONS_GROUP.addButton(rb)
        
        if lang == "en":
            self.SAVE_SIZE_BUTTON = widget.QPushButton("Save", self.FRAME_CENTRAL)
        else:
            self.SAVE_SIZE_BUTTON = widget.QPushButton("Зберегти", self.FRAME_CENTRAL)   
        
        self.SAVE_SIZE_BUTTON.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 4px;
                border: none;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.SAVE_SIZE_BUTTON.setFixedSize(core.QSize(105, 38))
        self.SAVE_SIZE_BUTTON.clicked.connect(self.save_resolution)
        self.FRAME_CENTRAL_LAYOUT.addWidget(self.SAVE_SIZE_BUTTON, alignment=core.Qt.AlignmentFlag.AlignLeft)
        
        self.RESOLUTION_FRAME.hide()

        self.LANGUAGE_FRAME = widget.QFrame(self.RIGHT_FRAME)
        self.LANGUAGE_LAYOUT = widget.QVBoxLayout(self.LANGUAGE_FRAME)
        self.LANGUAGE_LAYOUT.setContentsMargins(0,0,0,0)
        self.LANGUAGE_LAYOUT.setSpacing(24)
        
        if lang == "en":
            self.LANGUAGE_LABEL = widget.QLabel("Choose a language", self.LANGUAGE_FRAME)
        else:
            self.LANGUAGE_LABEL = widget.QLabel("Оберіть мову додатку", self.LANGUAGE_FRAME)
        
        self.LANGUAGE_LABEL.setStyleSheet("background-color: none; color: white; font-size: 18px; font-weight: 400;")
        self.LANGUAGE_LAYOUT.addWidget(self.LANGUAGE_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)
        
        self.COMBOBOX_FRAME = widget.QFrame(self.LANGUAGE_FRAME)
        self.COMBOBOX_FRAME.setFixedSize(core.QSize(544,54))
        self.LANGUAGE_CENTRAL_LAYOUT = widget.QVBoxLayout(self.COMBOBOX_FRAME)
        self.LANGUAGE_CENTRAL_LAYOUT.setContentsMargins(0,0,0,0)
        self.LANGUAGE_CENTRAL_LAYOUT.setSpacing(0)
        
        if lang == "en":
            self.LANGUAGE_LABEL = widget.QLabel("Language", self.COMBOBOX_FRAME)
        else:
            self.LANGUAGE_LABEL = widget.QLabel("Mовa додатку", self.COMBOBOX_FRAME)
        
        self.LANGUAGE_LABEL.setStyleSheet("background-color: none; color: white; font-size: 14px; font-weight: 500;")
        self.LANGUAGE_CENTRAL_LAYOUT.addWidget(self.LANGUAGE_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)

        if lang == "en":
            self.COMBOBOX_LANGUAGE = ComboBox(layout=self.LANGUAGE_CENTRAL_LAYOUT, items=["English", "Українська"])
        else:
            self.COMBOBOX_LANGUAGE = ComboBox(layout=self.LANGUAGE_CENTRAL_LAYOUT, items=["Українська", "English"])
        
        self.BUTTON_FRAME = widget.QFrame(self.LANGUAGE_FRAME)
        self.BUTTON_FRAME.setFixedSize(core.QSize(544,38))
        
        self.BUTTON_LAYOUT = widget.QHBoxLayout(self.BUTTON_FRAME)
        self.BUTTON_LAYOUT.setContentsMargins(0,0,0,0)
        self.BUTTON_LAYOUT.setSpacing(0)
        
        if lang == "en":
            self.SAVE_LANGUAGE_BUTTON = widget.QPushButton("Save", self.BUTTON_FRAME)
        else: 
            self.SAVE_LANGUAGE_BUTTON = widget.QPushButton("Зберегти", self.BUTTON_FRAME)
            
        self.SAVE_LANGUAGE_BUTTON.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 4px;
                border: none;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.SAVE_LANGUAGE_BUTTON.setFixedSize(core.QSize(105, 38))
        self.BUTTON_LAYOUT.addWidget(self.SAVE_LANGUAGE_BUTTON, alignment=core.Qt.AlignmentFlag.AlignLeft)
        
        self.LANGUAGE_LAYOUT.addWidget(self.COMBOBOX_FRAME)
        self.LANGUAGE_LAYOUT.addWidget(self.BUTTON_FRAME)
        
        self.LANGUAGE_FRAME.hide()

        self.IMG_LIST_FRAME = widget.QFrame(self.RIGHT_FRAME)
        self.IMG_LIST_LAYOUT = widget.QVBoxLayout(self.IMG_LIST_FRAME)
        self.IMG_LIST_LAYOUT.setContentsMargins(0,0,0,0)
        self.IMG_LIST_LAYOUT.setSpacing(24)
        
        
        
        self.ADD_STYLE_BUTTON = widget.QPushButton()
        self.ADD_STYLE_BUTTON.setFixedSize(core.QSize(97, 36))
        self.ADD_STYLE_BUTTON.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        self.STYLE_BUTTON_LAYOUT = widget.QHBoxLayout(self.ADD_STYLE_BUTTON)
        self.STYLE_BUTTON_LAYOUT.setContentsMargins(10, 0, 10, 0)
        self.STYLE_BUTTON_LAYOUT.setSpacing(6)
        self.STYLE_BUTTON_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        
        if lang == "en":
            self.IMG_LIST_LABEL = widget.QLabel("List of the images", self.IMG_LIST_FRAME)
        else:
            self.IMG_LIST_LABEL = widget.QLabel("Списки зображень", self.IMG_LIST_FRAME)
            
        self.IMG_LIST_LABEL.setStyleSheet("background-color: none; color: white; font-size: 18px; font-weight: 400;")
        self.IMG_LIST_LAYOUT.addWidget(self.IMG_LIST_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)
        
        self.ADD_ICON_BUTTON = QSvgWidget("media/search_bar/plus.svg", self.ADD_STYLE_BUTTON)
        self.ADD_ICON_BUTTON.setFixedSize(core.QSize(16, 16))
        
        if lang == "en":
            self.ADD_TEXT_BUTTON = widget.QLabel("Add", self.ADD_STYLE_BUTTON)
        else: 
            self.ADD_TEXT_BUTTON = widget.QLabel("Додати", self.ADD_STYLE_BUTTON)
        self.ADD_TEXT_BUTTON.setStyleSheet("color: white; font-size: 14px; font-weight: 500; background: none;")
        
        self.STYLE_BUTTON_LAYOUT.addWidget(self.ADD_ICON_BUTTON)
        self.STYLE_BUTTON_LAYOUT.addWidget(self.ADD_TEXT_BUTTON)
        self.IMG_LIST_LAYOUT.addWidget(self.ADD_STYLE_BUTTON)
        # self.ADD_STYLE_BUTTON.clicked.connect(self.add_styles)
            
            
        self.STYLES_FRAME = widget.QFrame()  
        self.STYLES_FRAME.setFixedSize(core.QSize(490,282))
        self.STYLES_FRAME_LAYOUT = widget.QVBoxLayout(self.STYLES_FRAME)
        self.STYLES_FRAME_LAYOUT.setContentsMargins(0,0,0,0)
        self.STYLE_BUTTON_LAYOUT.setSpacing(10)
        
        ### сделать json с путями папок изображений
        all_images = read_json("img_list.json")
        
        for i in all_images:
            style_list = widget.QFrame(self.STYLES_FRAME)
            style_list.setFixedSize(core.QSize(490,136))
            style_list.setStyleSheet("background-color: none; border-radius: 4px")
            style_list_layout = widget.QVBoxLayout(style_list)
            style_list_layout.setContentsMargins(16,16,16,16)
            style_list_layout.setSpacing(16)
            
            if lang == "en":
                number_img = widget.QLabel(f"Images list №{i}", style_list)
            else:
                number_img = widget.QLabel(f"Cписок зображень №{i}", style_list)
            number_img.setFixedSize(core.QSize(300,14))
            number_img.setStyleSheet("font-weight:500; font-size:14px; background-color: none")
            style_list_layout.addWidget(number_img)
            
            style_img_frame = widget.QFrame(style_list)
            style_img_frame.setStyleSheet("background-color: none")
            style_img_frame.setFixedSize(core.QSize(458, 74))
            style_list_layout.addWidget(style_img_frame)
            
            style_img_layout = widget.QHBoxLayout(style_img_frame)
            style_img_layout.setContentsMargins(0, 0, 0, 0)
            style_img_layout.setSpacing(16)
            
            for img in range(5):
                img_frame = widget.QFrame()
                img_frame.setFixedSize(core.QSize(74,74))
                img_frame.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border-radius: 10px")
                style_img_layout.addWidget(img_frame, alignment=core.Qt.AlignmentFlag.AlignCenter)
            
            
            self.STYLES_FRAME_LAYOUT.addWidget(style_list)
            
        self.IMG_LIST_LAYOUT.addWidget(self.STYLES_FRAME)   
        
        
        
        if lang == "en":
            self.SAVE_STYLE_BUTTON = widget.QPushButton("Save", self.COUNTRY_FRAME)
        else:
            self.SAVE_STYLE_BUTTON = widget.QPushButton("Зберегти", self.COUNTRY_FRAME)
            
        self.SAVE_STYLE_BUTTON.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 4px;
                border: none;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        self.SAVE_STYLE_BUTTON.setFixedSize(core.QSize(105, 38))
        self.SAVE_STYLE_BUTTON.clicked.connect(self.save_selected_city)
        self.IMG_LIST_LAYOUT.addWidget(self.SAVE_STYLE_BUTTON)
        
        self.IMG_LIST_FRAME.hide()

        self.SETTINGS.clicked.connect(self.show_settings)
        self.CLOSE_BUTTON.clicked.connect(self.close_settings)
        self.CITY_SEARCH.clicked.connect(self.city_search)
        self.RESOLUTION.clicked.connect(self.resolution_settings)
        self.LANGUAGE.clicked.connect(self.language_settings)
        self.IMG_LIST.clicked.connect(self.image_list)    
        self.COUNTRY_COMBOBOX.currentTextChanged.connect(self.update_country_map)
        self.SAVE_LANGUAGE_BUTTON.clicked.connect(self.language_save_json)
        

    def clear_old_results(self):
        for lbl in self.DYNAMIC_LABELS:
            lbl.hide()
            self.POPUP_LAYOUT.removeWidget(lbl)
            lbl.deleteLater()
        self.DYNAMIC_LABELS.clear()
        
        while self.POPUP_LAYOUT.count() > 1: 
            item = self.POPUP_LAYOUT.takeAt(1)
            if item.widget():
                item.widget().hide() 
                item.widget().deleteLater()

    def on_text_changed(self, text):
        self.clear_old_results()
        
        if text.strip():
            self.CLEAR.show()
            text_lower = text.strip().lower()
            
            city_exists = (text_lower in self.CITY_NAMES) or (text_lower in self.UA_CITIES)
            
            if city_exists:
                self.ADD_BUTTON.show()
            else:
                self.ADD_BUTTON.hide()
            
            found_cities = []
            limit = 5
            
            for c in self.CITIES_DATA:
                if len(found_cities) >= limit:
                    break
                    
                if not isinstance(c, dict):
                    continue
                
                name_en = c.get("name", "")
                translations = c.get("translations")
                name_ua = translations.get("uk", "") if isinstance(translations, dict) else ""
                
                if lang == "ua":
                    
                    if (name_ua and name_ua.lower().startswith(text_lower)) or name_en.lower().startswith(text_lower):
                        
                        display_name = name_ua if name_ua else name_en
                        if display_name not in found_cities:
                            found_cities.append(display_name)
                else:
                    
                    if name_en.lower().startswith(text_lower):
                        if name_en not in found_cities:
                            found_cities.append(name_en)
           
            
            if found_cities:
                for display_name in found_cities:
                    btn = widget.QPushButton(display_name, self.POPUP_FRAME)
                    btn.setFixedHeight(36)
                    btn.setStyleSheet("""
                        QPushButton {
                            text-align: left; 
                            background-color: transparent; 
                            color: white; 
                            padding: 6px 10px;
                            border: none;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            background-color: rgba(255, 255, 255, 0.2);
                            border-radius: 4px;
                        }
                    """)
                   
                    btn.clicked.connect(lambda checked, c=display_name: self._on_city_clicked(c))
                    
                    self.POPUP_LAYOUT.addWidget(btn)
                    self.DYNAMIC_LABELS.append(btn)

                if not self.POPUP.isVisible():
                    self.POPUP.show()
                
                self.POPUP_LAYOUT.activate()
                self.POPUP.resize(1, 1) 
                self.POPUP.adjustSize()
                
                pos = self.SEARCH.mapToGlobal(core.QPoint(0, self.SEARCH.height()))
                self.POPUP.move(pos)
        else:
            self.CLEAR.hide()
            self.ADD_BUTTON.hide()
            
    def _on_city_clicked(self, city_name):
        self.SEARCH_LINE.blockSignals(True)
        self.SEARCH_LINE.setText(city_name)
        self.SEARCH_LINE.blockSignals(False)
        self.CLEAR.show()
        self.ADD_BUTTON.show()
        
        self.POPUP.hide()
        self.update_city_map(city_name)
        
        try:
            coordinates = get_coordinates(city_name)
        except Exception as e:
            print(f"Error getting coordinates for {city_name}: {e}")
            coordinates = "0,0"
        
        self.city_selected.emit(city_name, coordinates)
            
    def eventFilter(self, obj, event):
        if event.type() == core.QEvent.Type.MouseButtonPress:
            if self.POPUP.isVisible():
                global_pos = event.globalPosition().toPoint()
                if not self.SEARCH.geometry().contains(self.SEARCH.mapFromGlobal(global_pos)) and \
                   not self.POPUP.geometry().contains(self.POPUP.mapFromGlobal(global_pos)):
                    self.POPUP.hide()
                    
        return super().eventFilter(obj, event)

    def clear_search_line(self):
        self.SEARCH_LINE.blockSignals(True)
        self.SEARCH_LINE.setText("")
        self.SEARCH_LINE.blockSignals(False)
        self.CLEAR.hide()
        self.ADD_BUTTON.hide()
        self.POPUP.hide()

    def add_city(self):
        city_name = self.SEARCH_LINE.text().strip()
        if not city_name:
            return

        city_obj = self.find_city(city_name)
        if not city_obj:
            return

        city_en = city_obj.get("name")
        translations = city_obj.get("translations")
        city_ua = translations.get("uk", city_en) if isinstance(translations, dict) else city_en

        
        self.save_city_everywhere(city_en, city_ua)
        
      
        target_name = city_ua if lang == "ua" else city_en
        
      
        self.update_added_cities(target_name)

        self.clear_search_line()
        
        
        self.city_added.emit(target_name)
        
    def show_settings(self):
        parent_frame = self.parent()
        if parent_frame is None:
            print("Помилка: батьківський фрейм не знайдено!")
            return
        
        frame_center = parent_frame.rect().center() 
        global_center = parent_frame.mapToGlobal(frame_center)

        popup_width = self.SETTINGS_POPUP.width()
        popup_height = self.SETTINGS_POPUP.height()
        
        final_x = global_center.x() - (popup_width // 2)
        final_y = global_center.y() - (popup_height // 2)

        try:
            parent_window = parent_frame.window()

            popup_size = self.SETTINGS_POPUP.size()
            global_top_left = core.QPoint(final_x, final_y)
            local_top_left = parent_window.mapFromGlobal(global_top_left)

            grab_rect = core.QRect(local_top_left, popup_size)

            parent_rect = parent_window.rect()
            grab_rect = grab_rect.intersected(parent_rect)

            if not grab_rect.isEmpty():
                grabbed = parent_window.grab(grab_rect)
            else:
                grabbed = parent_window.grab()

            blurred = self.blur_pixmap(grabbed, radius=8)

            if self._blur_label is None:
                self._blur_label = widget.QLabel(self.SETTINGS_POPUP)
                self._blur_label.setObjectName("_blurLabel")
                self._blur_label.setScaledContents(True)

            if blurred.size() != self.SETTINGS_POPUP.size():
                blurred = blurred.scaled(self.SETTINGS_POPUP.size(), core.Qt.AspectRatioMode.IgnoreAspectRatio, core.Qt.TransformationMode.SmoothTransformation)

            self._blur_label.setPixmap(blurred)
            self._blur_label.setFixedSize(self.SETTINGS_POPUP.size())
            self._blur_label.move(0, 0)
            self._blur_label.lower()
            self._blur_label.show()
        except Exception as e:
            print(f"Блюр выдал ошибку: {e}")

        self.SETTINGS_POPUP.move(final_x, final_y)
        self.SETTINGS_POPUP.show()
        self.SETTINGS_POPUP.raise_()
        
    def close_settings(self):
        self.SETTINGS_POPUP.hide()

    def clear(self):
        self.CITY_SEARCH.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:none; text-align: left; padding-left: 8px;")
        self.RESOLUTION.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:none; text-align: left; padding-left: 8px;")
        self.LANGUAGE.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:none; text-align: left; padding-left: 8px;")
        self.IMG_LIST.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:none; text-align: left; padding-left: 8px;")

        self.CITY_SEARCH_FRAME.hide()
        self.RESOLUTION_FRAME.hide()
        self.LANGUAGE_FRAME.hide()
        self.IMG_LIST_FRAME.hide()

    def city_search(self):
        self.clear()
        self.CITY_SEARCH.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 0px; font-size:16px; font-weight:400; border:none; text-align: left; padding-left: 8px;")
        self.CITY_SEARCH_FRAME.show()
    
    def resolution_settings(self):
        self.clear()
        self.RESOLUTION.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 0px; font-size:16px; font-weight:400; border:none; text-align: left; padding-left: 8px;")
        self.RESOLUTION_FRAME.show()

    def on_resolution_changed(self, button):
        resolution = read_json("settings.json")
        current_res = button.text().split("x")
        resolution["currentResolution"] = current_res  
        create_json(resolution, "settings.json")

    def language_settings(self):
        self.clear()
        self.LANGUAGE.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 0px; font-size:16px; font-weight:400; border:none; text-align: left; padding-left: 8px;")
        self.LANGUAGE_FRAME.show()

    def image_list(self):
        self.clear()
        self.IMG_LIST.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 0px; font-size:16px; font-weight:400; border:none; text-align: left; padding-left: 8px;")
        self.IMG_LIST_FRAME.show()

    def save_resolution(self):
        checked_button = self.RAIDO_BUTTONS_GROUP.checkedButton()
        if checked_button:
            res_str = checked_button.text()
            width, height = map(int, res_str.split("x"))
            
            resolution = read_json("settings.json")
            resolution["currentResolution"] = [str(width), str(height)]
            create_json(resolution, "settings.json")
            
            self.resolution_changed.emit(width, height)
            self.close_settings()

    def update_coordinates_display(self, city_name):
        if lang == "en":
            if not city_name or city_name in ["Choose a city", "No cities"]:
                self.COORDS_QLINEEDIT.clear()
                return
        else:
            if not city_name or city_name in ["Виберіть місто", "Немає міст"]:
                self.COORDS_QLINEEDIT.clear()
                return

        coords = self.get_coords(city_name)
        if not coords:
            if lang == "en":
                self.COORDS_QLINEEDIT.setText("Not found")
            else:
                self.COORDS_QLINEEDIT.setText("Не знайдено")
            return

        lat, lon = coords
        self.COORDS_QLINEEDIT.setText(f"{lat}, {lon}")

    def save_selected_city(self):
      
        city_name = self.CITY_COMBOBOX.currentText().strip()
    
        if not city_name or city_name in ["Виберіть місто", "Немає міст", "Choose a city", "No cities"]:
            return
    
        city_obj = self.find_city(city_name)
        if not city_obj:
            return
    
        city_en = city_obj.get("name")
        translations = city_obj.get("translations")
        city_ua = translations.get("uk", city_en) if isinstance(translations, dict) else city_en
    
        self.save_city_everywhere(city_en, city_ua)
        
        target_name = city_ua if lang == "ua" else city_en
        
        
        self.update_added_cities(target_name)
        
        self.city_added.emit(target_name)

    def delete_city(self, city_name):
        city_name = city_name.strip()
        
        for file_name in ["city.json", "city_en.json", "city_ua.json"]:
            try:
                cities = read_json(file_name)
                cities = [c for c in cities if c.lower() != city_name.lower()]
                create_json(cities, file_name)
            except:
                pass

        frame = self.added_city_frames.get(city_name.lower())
        if frame:
            self.ADDED_CITIES_LAYOUT.removeWidget(frame)
            frame.setParent(None)
            frame.deleteLater()
            try:
                del self.added_city_frames[city_name.lower()]
            except KeyError:
                pass

        self.CITIES_LIST = [c for c in self.CITIES_LIST if c.lower() != city_name.lower()]
        self.city_removed.emit(city_name)

    def update_added_cities(self, city_name):
        if city_name.lower() in self.added_city_frames:
            return

        frame = widget.QFrame()
        frame.setStyleSheet("background-color: none;")
        frame.setFixedSize(core.QSize(512,32))
        self.ADDED_CITIES_LAYOUT.addWidget(frame)

        row_layout = widget.QHBoxLayout(frame) 
        label = widget.QLabel(city_name)
        label.setStyleSheet("color: white; font-size: 14px; margin-top:-5px")

        trash_btn = widget.QPushButton()
        trash_btn.setFixedSize(core.QSize(16,16))
        trash_btn.setStyleSheet("QPushButton { background-color: none; border: none; }")
        trash_btn.clicked.connect(lambda checked=False, c=city_name: self.delete_city(c))
        QSvgWidget("media/search_bar/trash.svg", trash_btn)

        row_layout.addWidget(label, alignment=core.Qt.AlignmentFlag.AlignLeft)
        row_layout.addWidget(trash_btn, alignment=core.Qt.AlignmentFlag.AlignRight)

        self.added_city_frames[city_name.lower()] = frame

    def _render_map(self, lat, lon, label=""):
        self.WEBMAP = folium.Map(
            location=[lat, lon],
            zoom_start=10,
            tiles="OpenStreetMap"
        )
        folium.Marker(
            [lat, lon],
            popup=label,
            tooltip=label
        ).add_to(self.WEBMAP)

        data = io.BytesIO()
        self.WEBMAP.save(data, close_file=False)
        self.WEB_VIEW.setHtml(data.getvalue().decode())

    def blur_pixmap(self, pixmap, radius=8):
        try:
            if pixmap is None or pixmap.isNull():
                return pixmap

            img = gui.QImage(pixmap.size(), gui.QImage.Format.Format_ARGB32)
            img.fill(0)

            painter = gui.QPainter(img)

            scene = widget.QGraphicsScene()
            item = scene.addPixmap(pixmap)

            blur = widget.QGraphicsBlurEffect()
            blur.setBlurRadius(radius)
            try:
                item.setGraphicsEffect(blur)
            except Exception:
                pass

            scene.render(painter)
            painter.end()

            return gui.QPixmap.fromImage(img)
        except Exception as e:
            print(f"[BLUR] Error while blurring pixmap: {e}")
            return pixmap

    def update_city_map(self, city_name):
        if lang == "en":
            if not city_name or city_name in ["Choose a city", "No cities"]:
                return
        else:
            if not city_name or city_name in ["Виберіть місто", "Немає міст"]:
                return

        coords = self.get_coords(city_name)
        if not coords:
            print("[MAP] City not found in JSON")
            return

        lat, lon = coords
        self._render_map(lat, lon, city_name)

    def update_country_map(self, country_name):
        country_id = self.COUNTRY_NAME_TO_ID.get(country_name)
        if country_id is None:
            return

        cities = [
            c for c in self.CITIES_DATA
            if isinstance(c, dict) and c.get("country_id") == country_id
        ]
        if not cities:
            return

        city = cities[0]
        lat = float(city["latitude"])
        lon = float(city["longitude"])
        self._render_map(lat, lon, country_name)

    def update_cities_by_country(self, country_name):
        self.CITY_COMBOBOX.clear()

        if lang == "en":
            self.CITY_COMBOBOX.addItem("Choose a city")
        else:
            self.CITY_COMBOBOX.addItem("Виберіть місто")

        if not country_name:
            return

        country_id = self.COUNTRY_NAME_TO_ID.get(country_name)

        cities = []

        if country_id is not None:
            for c in self.CITIES_DATA:
                if not isinstance(c, dict):
                    continue

                if c.get("country_id") == country_id:
                    display_name = self.get_city_display_name(c)

                    if display_name:
                        cities.append(display_name)

        if not cities:

            if lang == "en":
                self.CITY_COMBOBOX.addItem("No cities")
            else:
                self.CITY_COMBOBOX.addItem("Немає міст")

            return

        self.CITY_COMBOBOX.addItems(cities)

    def get_coords(self, city_name):
        city = self.find_city(city_name)
        if not city:
            return None
        return float(city["latitude"]), float(city["longitude"])
    
    def find_city(self, city_name):
        if not city_name:
            return None
            
        for c in self.CITIES_DATA:
            if not isinstance(c, dict):
                continue
            
            if lang == "en":
                if c.get("name", "").lower() == city_name.lower():
                    return c
            else:
            
                translations = c.get("translations")
                if isinstance(translations, dict):
                    uk = translations.get("uk", "")
                    if uk and uk.lower() == city_name.lower():
                        return c
              
                if c.get("name", "").lower() == city_name.lower():
                    return c
        return None
    
    def language_save_json(self):
        current_language = self.COMBOBOX_LANGUAGE.currentText()
        print(current_language)

        set_language = read_json("settings.json")
        if current_language == "Українська":
            set_language["language"] = "ua"
        elif current_language == "English":
            set_language["language"] = "en"

        create_json(set_language, "settings.json")
        
    def get_city_display_name(self, city_obj):
        if not isinstance(city_obj, dict):
            return ""
        if lang == "en":
            return city_obj.get("name", "")
            
        translations = city_obj.get("translations")
        if isinstance(translations, dict):
            return translations.get("uk", city_obj.get("name", ""))
        return city_obj.get("name", "")
    
    def save_city_everywhere(self, city_en: str, city_ua: str):
        try:
            cities_en = read_json("city_en.json")
        except:
            cities_en = []
    
        try:
            cities_ua = read_json("city_ua.json")
        except:
            cities_ua = []
    
        if city_en.lower() not in [c.lower() for c in cities_en]:
            cities_en.append(city_en)
    
        if city_ua.lower() not in [c.lower() for c in cities_ua]:
            cities_ua.append(city_ua)
    
        create_json(cities_en, "city_en.json")
        create_json(cities_ua, "city_ua.json")

    def remove_city_everywhere(self, city_name: str):
        try:
            cities_en = read_json("city_en.json")
        except:
            cities_en = []

        try:
            cities_ua = read_json("city_ua.json")
        except:
            cities_ua = []

        target_en = None
        target_ua = None

        for city_obj in self.CITIES_DATA:
            target_en = None
            target_ua = None

        for city_obj in self.CITIES_DATA:
            if not isinstance(city_obj, dict):
                continue
                
            name_en = city_obj.get("name", "")
            translations = city_obj.get("translations")
            name_ua = translations.get("uk", "") if isinstance(translations, dict) else ""

            if city_name.lower() in [name_en.lower(), name_ua.lower()]:
                target_en = name_en
                target_ua = name_ua
                break

        search_en = [target_en.lower()] if target_en else [city_name.lower()]
        search_ua = [target_ua.lower()] if target_ua else [city_name.lower()]

        new_cities_en = [c for c in cities_en if c.lower() not in search_en]
        new_cities_ua = [c for c in cities_ua if c.lower() not in search_ua]

       
        create_json(new_cities_en, "city_en.json")
        create_json(new_cities_ua, "city_ua.json")
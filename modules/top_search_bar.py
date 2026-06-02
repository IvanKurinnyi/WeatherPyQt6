import PyQt6.QtWidgets as widget
import PyQt6.QtWebEngineWidgets as web_engine
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtSvgWidgets import QSvgWidget
import folium, io
from .find_town import find_cities_by_prefix
from .read_write_json import create_json, read_json
from .combobox import ComboBox
from .api_request import get_coordinates
import requests
class SearchBar(widget.QFrame):
    city_selected = core.pyqtSignal(str)
    city_added = core.pyqtSignal(str)
    resolution_changed = core.pyqtSignal(int, int)  # ширина, висота
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.CITIES_DATA = read_json("cities.json").get("data", [])
        self.CITY_NAMES = [city_obj.get('city', '').lower() for city_obj in self.CITIES_DATA]
        self.DYNAMIC_LABELS = []

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
        
        self.SETTINGS_LABEL = widget.QLabel("Налаштування",self.SETTINGS_FRAME)
        self.SETTINGS_LABEL.setStyleSheet("font-size:14px; font-weight:500;")
        self.S_LAYOUT.addWidget(self.SETTINGS_LABEL)

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

        self.RESULTS = widget.QLabel("Результати пошуку", self.POPUP_FRAME)
        self.RESULTS.setStyleSheet("background-color: none; color: white; padding-left: 5px; border: none;")
        self.POPUP_LAYOUT.addWidget(self.RESULTS)
        self.POPUP.hide()
        
        self.SEARCH_LINE.textChanged.connect(self.on_text_changed)
        widget.QApplication.instance().installEventFilter(self)
        
        self.SETTINGS_POPUP = widget.QFrame()
        self.SETTINGS_POPUP.setFixedSize(core.QSize(790, 688))
        self.SETTINGS_POPUP.setWindowFlags(
            core.Qt.WindowType.Window | 
            core.Qt.WindowType.FramelessWindowHint |
            core.Qt.WindowType.WindowStaysOnTopHint |
            core.Qt.WindowType.WindowDoesNotAcceptFocus |
            core.Qt.WindowType.NoDropShadowWindowHint
        )
        self.SETTINGS_POPUP.setStyleSheet("background-color: none; border-radius: 10px; border: none;")
        self.SETTINGS_POPUP.raise_()
        self.SETTINGS_POPUP_FRAME = widget.QFrame(self.SETTINGS_POPUP)
        self.SETTINGS_POPUP_FRAME.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); border-radius: 10px; border: none;")
        
        self.SETTINGS_POPUP_LAYOUT = widget.QVBoxLayout(self.SETTINGS_POPUP_FRAME)
        self.SETTINGS_POPUP_LAYOUT.setContentsMargins(24,24,24,24)
        self.SETTINGS_POPUP_LAYOUT.setSpacing(34)
        self.TITLE_SETT = widget.QFrame()
        self.TITLE_SETT.setStyleSheet("background-color: none")
        self.TITLE_SETT.setFixedSize(core.QSize(742, 28))
        self.SETTINGS_POPUP_LAYOUT.addWidget(self.TITLE_SETT, alignment=core.Qt.AlignmentFlag.AlignCenter)
        
        self.T_LAYOUT = widget.QHBoxLayout(self.TITLE_SETT)
        self.T_LAYOUT.setContentsMargins(0,0,0,0)

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
        
        self.CITY_SEARCH = widget.QPushButton("Пошук міста")
        self.CITY_SEARCH.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:0px; text-align: left; padding-left: 8px;")
        self.CITY_SEARCH.setFixedSize(core.QSize(158, 35))
        
        self.RESOLUTION = widget.QPushButton("Розмір Додатку")
        self.RESOLUTION.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:0px; text-align: left; padding-left: 8px;")
        self.RESOLUTION.setFixedSize(core.QSize(158, 35))

        self.LANGUAGE = widget.QPushButton("Мова додатку")
        self.LANGUAGE.setStyleSheet("background-color: none; border-radius: 0px; font-size:16px; font-weight:400; border:0px; text-align: left; padding-left: 8px;")
        self.LANGUAGE.setFixedSize(core.QSize(158, 35))

        


        self.IMG_LIST = widget.QPushButton("Список зображень")
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

        self.WEBMAP = folium.Map(location=(50, 30))
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
        countries = [item["name"] for item in countrys_json["data"]]

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


        self.CITY_LABEL = widget.QLabel("Місто")
        self.CITY_LABEL.setStyleSheet("color:white; font-weight:500;font-size:14px;text-align: left;")
        self.CITY_LABEL.setFixedSize(core.QSize(249, 14))
        self.CITY_GROUP_LAYOUT.addWidget(self.CITY_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.CITY_COMBOBOX = ComboBox(layout=self.CITY_GROUP_LAYOUT, items=["Виберіть місто", "Dnipro", "Kharkiv", "Kyiv"])

        self.COUNTRY_COMBOBOX.currentTextChanged.connect(self.update_cities_by_country)

        if self.COUNTRY_COMBOBOX.count() > 0:
            self.update_cities_by_country(self.COUNTRY_COMBOBOX.currentText())

        self.COORDS_GROUP_FRAME = widget.QFrame()
        self.COORDS_GROUP_LAYOUT = widget.QVBoxLayout(self.COORDS_GROUP_FRAME)
        self.COORDS_GROUP_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.COORDS_GROUP_LAYOUT.setSpacing(4)
        self.COUNTRY_LAYOUT.addWidget(self.COORDS_GROUP_FRAME)

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
        self.COUNTRY_LAYOUT.addWidget(self.SAVE_MAP_BUTTON, alignment=core.Qt.AlignmentFlag.AlignLeft)
        
        self.ADDED_CITIES_LABEL = widget.QLabel("Додані міста")
        self.ADDED_CITIES_LABEL.setStyleSheet("color:white; font-weight:400;font-size:18px;text-align: left;")
        self.CITY_SEARCH_LAYOUT.addWidget(self.ADDED_CITIES_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)


        self.ADDED_CITIES_FRAME = widget.QFrame()
        self.ADDED_CITIES_FRAME.setStyleSheet("background-color: rgba(0, 0, 0, 0.2)")
        self.ADDED_CITIES_FRAME.setFixedSize(core.QSize(544,160))
        self.CITY_SEARCH_LAYOUT.addWidget(self.ADDED_CITIES_FRAME, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.ADDED_CITIES_LAYOUT = widget.QVBoxLayout(self.ADDED_CITIES_FRAME)
        self.ADDED_CITIES_LAYOUT.setContentsMargins(16,16,16,16)
        self.ADDED_CITIES_LAYOUT.setSpacing(0)
        
        cities_list = ["Kyiv", "Bratislava", "Dnipro", "Rome"]
        
        for city in cities_list:
            frame = widget.QFrame()
            frame.setStyleSheet("background-color: none;")
            frame.setFixedSize(core.QSize(512,32))
            self.ADDED_CITIES_LAYOUT.addWidget(frame)
            
            layout = widget.QHBoxLayout(frame)

            label = widget.QLabel(city)
            trash_icon = QSvgWidget("media/search_bar/trash.svg")
            layout.addWidget(label, alignment=core.Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(trash_icon, alignment=core.Qt.AlignmentFlag.AlignRight)
            
        self.CITY_SEARCH_FRAME.hide()

        self.RESOLUTION_FRAME = widget.QFrame(self.RIGHT_FRAME)
        self.RESOLUTION_LAYOUT = widget.QVBoxLayout(self.RESOLUTION_FRAME)
        self.RESOLUTION_LAYOUT.setContentsMargins(0,0,0,0)
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

        resolution = read_json("settings.json")
        

        self.RADIO_1 = widget.QRadioButton("1200x800", self.RADIO_BUTTONS_FRAME)
        self.RADIO_2 = widget.QRadioButton("1440x1024", self.RADIO_BUTTONS_FRAME)
        self.RADIO_3 = widget.QRadioButton("1512x982", self.RADIO_BUTTONS_FRAME)
        self.RADIO_4 = widget.QRadioButton("1728x1117", self.RADIO_BUTTONS_FRAME)

        radio_buttons = [self.RADIO_1, self.RADIO_2, self.RADIO_3, self.RADIO_4]

        self.RAIDO_BUTTONS_GROUP = widget.QButtonGroup(self.RADIO_BUTTONS_FRAME)
        for rb in radio_buttons:
            self.FRAME_RADIOBUTTONS_LAYOUT.addWidget(rb, alignment=core.Qt.AlignmentFlag.AlignLeft)
            self.RAIDO_BUTTONS_GROUP.addButton(rb)
        
        
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
        self.LANGUAGE_LABEL = widget.QLabel("Оберіть мову додатку", self.LANGUAGE_FRAME)
        self.LANGUAGE_LABEL.setStyleSheet("background-color: none; color: white; font-size: 18px; font-weight: 400;")
        self.LANGUAGE_LAYOUT.addWidget(self.LANGUAGE_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)
        
        self.COMBOBOX_FRAME = widget.QFrame(self.LANGUAGE_FRAME)
        self.COMBOBOX_FRAME.setFixedSize(core.QSize(544,54))
        self.LANGUAGE_CENTRAL_LAYOUT = widget.QVBoxLayout(self.COMBOBOX_FRAME)
        self.LANGUAGE_CENTRAL_LAYOUT.setContentsMargins(0,0,0,0)
        self.LANGUAGE_CENTRAL_LAYOUT.setSpacing(0)
        
        self.LANGUAGE_LABEL = widget.QLabel("Mовa додатку", self.COMBOBOX_FRAME)
        self.LANGUAGE_LABEL.setStyleSheet("background-color: none; color: white; font-size: 14px; font-weight: 500;")

        self.LANGUAGE_CENTRAL_LAYOUT.addWidget(self.LANGUAGE_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.COMBOBOX_LANGUAGE = ComboBox(layout=self.LANGUAGE_CENTRAL_LAYOUT, items=["Українська", "English"])
        
        self.BUTTON_FRAME = widget.QFrame(self.LANGUAGE_FRAME)
        self.BUTTON_FRAME.setFixedSize(core.QSize(544,38))
        
        self.BUTTON_LAYOUT = widget.QHBoxLayout(self.BUTTON_FRAME)
        self.BUTTON_LAYOUT.setContentsMargins(0,0,0,0)
        self.BUTTON_LAYOUT.setSpacing(0)
        
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
        self.IMG_LIST_LABEL = widget.QLabel("Список зображень", self.IMG_LIST_FRAME)
        self.IMG_LIST_LABEL.setStyleSheet("background-color: none; color: white; font-size: 18px; font-weight: 400;")
        self.IMG_LIST_LAYOUT.addWidget(self.IMG_LIST_LABEL, alignment=core.Qt.AlignmentFlag.AlignLeft)
        
        
        
        self.IMG_LIST_FRAME.hide()

        self.SETTINGS.clicked.connect(self.show_settings)
        self.CLOSE_BUTTON.clicked.connect(self.close_settings)
        self.CITY_SEARCH.clicked.connect(self.city_search)
        self.RESOLUTION.clicked.connect(self.resolution_settings)
        self.LANGUAGE.clicked.connect(self.language_settings)
        self.IMG_LIST.clicked.connect(self.image_list)    

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
            city_exists = text_lower in self.CITY_NAMES
            
            if city_exists:
                self.ADD_BUTTON.show()
            else:
                self.ADD_BUTTON.hide()
            
            # Show search results
            found_cities = find_cities_by_prefix(self.CITIES_DATA, text, limit=5)
            
            if found_cities:
                for city in found_cities:
                    btn = widget.QPushButton(city, self.POPUP_FRAME)
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
                    btn.clicked.connect(lambda checked, c=city: self._on_city_clicked(c))
                    
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
        self.city_selected.emit(city_name)
            
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

        try:
            cities = read_json("city.json")
        except:
            cities = []

        if any(c.lower() == city_name.lower() for c in cities):
            return
        
        cities.append(city_name)
        
        create_json(cities, "city.json")
        
        self.clear_search_line()
        
        self.city_added.emit(city_name)
        
    def show_settings(self):
        self.SETTINGS_POPUP.show()
        
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

    def update_cities_by_country(self, country_name):      
        if not country_name or country_name == "Виберіть країну":
           
            self.CITY_COMBOBOX.clear()
            self.CITY_COMBOBOX.addItem("Виберіть місто")
            return
        
    
        cities_data = self.CITIES_DATA
        
       
        cities_for_country = [
            city_obj.get('city', '').title() 
            for city_obj in cities_data 
            if city_obj.get('country', '').lower() == country_name.lower()
        ]
        
        
        self.CITY_COMBOBOX.clear()
        
        if cities_for_country:
            self.CITY_COMBOBOX.addItem("Виберіть місто")
            self.CITY_COMBOBOX.addItems(cities_for_country)  
        else:
            self.CITY_COMBOBOX.addItem("Немає міст")
    def update_coordinates_display(self, city_name):
        if not city_name or city_name in ["Виберіть місто", "Немає міст"]:
            self.COORDS_QLINEEDIT.clear()
            return
        
        try:
            
            url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
            res = requests.get(url, headers={"User-Agent": "my-app"}, timeout=5)
            
            if res.status_code == 200 and res.json():
                data = res.json()[0]  
                lat = data.get("lat", "")
                lon = data.get("lon", "")
                
               
                self.COORDS_QLINEEDIT.setText(f"{lat}, {lon}")
            else:
                self.COORDS_QLINEEDIT.setText("Координати не знайдені")
        except Exception as e:
            print(f"Помилка при отриманні координат: {e}")
            self.COORDS_QLINEEDIT.setText("Помилка при отриманні")
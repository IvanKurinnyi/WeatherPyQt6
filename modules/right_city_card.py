import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtSvgWidgets import QSvgWidget
from .api_request import api_request, API_KEY
import PyQt6.QtGui as gui
from PIL import Image
from PIL.ImageQt import ImageQt

class RightCityCard(widget.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WIDTH = 390
        self.HEIGHT = 303
        self.setFixedSize(core.QSize(self.WIDTH, self.HEIGHT))
        self.setStyleSheet("""
            RightCityCard {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 10px;
            }
        """)
       
        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(16, 16, 16, 16)
        self.LAYOUT.setSpacing(16)
        
        self.TOP_SECTION = widget.QWidget()
        self.TOP_SECTION_LAYOUT = widget.QVBoxLayout(self.TOP_SECTION)
        self.TOP_SECTION_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TOP_SECTION_LAYOUT.setSpacing(8)

        
        self.ICON_TEXT_CONTAINER = widget.QWidget()
        self.ICON_TEXT_LAYOUT = widget.QHBoxLayout(self.ICON_TEXT_CONTAINER)
        self.ICON_TEXT_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.ICON_TEXT_LAYOUT.setSpacing(8)

        
        #self.TOP_ICON = widget.QLabel()
        #self.TOP_PIXMAP = gui.QPixmap("media/city_card/navigation.svg")
        #self.TOP_ICON.setPixmap(self.TOP_PIXMAP.scaled(76,76))


        self.TOP_FRAME_ICON = QSvgWidget("media/city_card/navigation.svg")
        self.TOP_FRAME_ICON.setFixedSize(16, 16)
        
        self.TOP_TEXT = widget.QLabel("Поточна позiцiя")
        self.TOP_TEXT.setStyleSheet("color: white; font-size: 16px; font-family: 'Roboto'; font-weight: 500;")
        
        self.ICON_TEXT_LAYOUT.addWidget(self.TOP_FRAME_ICON)
        self.ICON_TEXT_LAYOUT.addWidget(self.TOP_TEXT)
        self.ICON_TEXT_LAYOUT.addStretch() 

        
        self.LINE = widget.QFrame()
        self.LINE.setFixedHeight(1)
        self.LINE.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")

        
        self.TOP_SECTION_LAYOUT.addWidget(self.ICON_TEXT_CONTAINER)
        self.TOP_SECTION_LAYOUT.addWidget(self.LINE)
        
        
        self.LAYOUT.addWidget(self.TOP_SECTION)
        

        self.LAYOUT.addStretch() 
        self.CITY_LABEL = widget.QLabel("")
        self.CITY_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.CITY_LABEL.setStyleSheet("font-size: 44px; font-weight: bold; font-family: 'Roboto'; color: white; background: none;")
        self.LAYOUT.addWidget(self.CITY_LABEL)
        
     
        self.DEGREE_FRAME = widget.QFrame()
        self.DEGREE_LAYOUT = widget.QHBoxLayout(self.DEGREE_FRAME)
        self.DEGREE_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        
        self.WEATHER_ICON = widget.QLabel()
        self.TOP_PIXMAP = gui.QPixmap("media/right_frame/Cloudy.svg")
        #self.WEATHER_ICON.setPixmap(self.TOP_PIXMAP.scaled(76,76))

        #self.WEATHER_ICON = QSvgWidget("media/right_frame/Cloudy.svg")
        #self.WEATHER_ICON.setFixedSize(60, 60)
        
        
        self.DEGREE = widget.QLabel("")
        self.DEGREE.setStyleSheet("font-size: 74px; color: white; font-family: 'Roboto';font-weight: 500; background: none;")
        
        self.DEGREE_LAYOUT.addWidget(self.WEATHER_ICON)
        self.DEGREE_LAYOUT.addWidget(self.DEGREE)
        
        self.LAYOUT.addWidget(self.DEGREE_FRAME)

        self.STAT_LABEL = widget.QLabel("")
        self.STAT_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.STAT_LABEL.setStyleSheet("font-size: 24px; font-weight: 500; white; font-family: 'Roboto';background: none;")
        self.LAYOUT.addWidget(self.STAT_LABEL)

        self.MINMAX_LABEL = widget.QLabel()
        self.MINMAX_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.MINMAX_LABEL.setStyleSheet("font-size: 16px; color: white; font-weight: 500;font-family: 'Roboto'; background: none")
        self.LAYOUT.addWidget(self.MINMAX_LABEL)


        self.LAYOUT.addStretch()

    def update_city_data(self, city_name):
        city_request = api_request(city=city_name, API_KEY=API_KEY)
        
        temp = str(round(city_request["main"]["temp"]))
        temp_max = str(city_request["main"]["temp_max"])
        temp_min = str(city_request["main"]["temp_min"])
        description:str = city_request["weather"][0]["description"]
        icon_path = f"media/right_frame/weather_icons/{city_request["weather"][0]["icon"]}.svg"
        self.CITY_LABEL.setText(city_name)
        self.DEGREE.setText(temp + "°")
        #self.WEATHER_ICON.load(icon_path)
        #self.WEATHER_ICON = widget.QLabel()
        self.TOP_PIXMAP = gui.QPixmap(icon_path)
        self.WEATHER_ICON.setPixmap(self.TOP_PIXMAP.scaled(76,76))
        self.STAT_LABEL.setText(description.capitalize())
        self.MINMAX_LABEL.setText(f"Макс.: {temp_max}°, мін.: {temp_min}°")
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtSvgWidgets import QSvgWidget
import PyQt6.QtGui as gui
from .api_request import forecast_request
from .api import API_KEY

class ForeCastTime(widget.QFrame):
    def __init__(self, city_name,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.WIDTH = 788
        self.HEIGHT = 157
        self.setFixedSize(core.QSize(self.WIDTH, self.HEIGHT))
        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(16,16,16,16)
        self.LAYOUT.setSpacing(16)
        
        self.setStyleSheet("background-color: rgba(0,0,0,0.2); border: none; border-radius: 10px")
        
        self.TOP_FRAME = widget.QFrame()
        self.TOP_FRAME.setStyleSheet("background-color: none")
        self.TOP_LAYOUT = widget.QVBoxLayout(self.TOP_FRAME)
        self.TOP_LAYOUT.setContentsMargins(0,0,0,0)
        self.TOP_LAYOUT.setSpacing(8)
        self.LAYOUT.addWidget(self.TOP_FRAME)
        
        
        self.TOP_TEXT = widget.QLabel("Хмарна погода до кінця дня")
        self.TOP_TEXT.setStyleSheet("font-size:16px; color:white")
        self.TOP_LAYOUT.addWidget(self.TOP_TEXT)
        
        self.LINE = widget.QFrame()
        self.LINE.setFixedHeight(1)
        self.LINE.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")
        self.TOP_LAYOUT.addWidget(self.LINE)
        
        self.DOWN_FRAME = widget.QFrame()
        self.DOWN_FRAME.setStyleSheet("background-color: none")
        self.DOWN_LAYOUT = widget.QHBoxLayout(self.DOWN_FRAME)
        self.DOWN_LAYOUT.setContentsMargins(0,0,0,0)
        self.LAYOUT.addWidget(self.DOWN_FRAME)

        self.LEFT_BUTTON = widget.QPushButton()
        self.LEFT_ARROW = gui.QIcon("media/right_frame/arrow_left.svg")
        self.LEFT_BUTTON.setIcon(self.LEFT_ARROW)
        self.LEFT_BUTTON.setFixedSize(core.QSize(16,16))
        self.DOWN_LAYOUT.addWidget(self.LEFT_BUTTON)
        

        self.CENTRAL = widget.QFrame()
        self.CENTRAL.setStyleSheet("background-color: blue") 
        self.CENTRAL.setFixedSize(core.QSize(676, 82))
        
        self.CENTRAL_LAYOUT = widget.QHBoxLayout(self.CENTRAL)
        self.CENTRAL_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CENTRAL_LAYOUT.setSpacing(17) 
        
        self.DOWN_LAYOUT.addWidget(self.CENTRAL, alignment=core.Qt.AlignmentFlag.AlignCenter)

        api_request = forecast_request(city = city_name, API_KEY = API_KEY)
        count = 0
        for item in api_request["list"][:10]:
            
            time = item["dt_txt"]
            temp = round(item["main"]["temp"])
            icon = item["weather"][0]["icon"]
            # desc = item["weather"][0]["description"]


            forecast = widget.QFrame()
            forecast.setFixedSize(core.QSize(45, 82))
            layout = widget.QVBoxLayout(forecast)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(4)
            layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            
            if count == 0:
                hour = widget.QLabel("Зараз")
            else:
                hour = widget.QLabel(time[10:13])
            hour.setStyleSheet("font-size:16px")
                
            wicon = QSvgWidget(f"media/right_frame/weather_icons/{icon}.svg")
            wicon.setFixedSize(24, 24)

            degree = widget.QLabel(f"{temp}°")
            degree.setStyleSheet("font-size:16px")
   
            
            layout.addWidget(hour)
            layout.addWidget(wicon)
            layout.addWidget(degree)
            
            self.CENTRAL_LAYOUT.addWidget(forecast)
            count += 1

            # print(f"{time} | {temp}°C | {desc}")
    
        self.RIGHT_BUTTON = widget.QPushButton()
        self.RIGHT_ARROW = gui.QIcon("media/right_frame/arrow_right.svg")
        self.RIGHT_BUTTON.setIcon(self.RIGHT_ARROW)
        self.RIGHT_BUTTON.setFixedSize(core.QSize(16,16))
        self.DOWN_LAYOUT.addWidget(self.RIGHT_BUTTON)
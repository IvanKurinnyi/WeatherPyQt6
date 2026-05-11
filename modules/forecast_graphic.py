import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtSvgWidgets import QSvgWidget
import PyQt6.QtGui as gui
from .api_request import forecast_request
from .api import API_KEY

class ForeCastGraph(widget.QFrame):
    def __init__(self, city_name,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.WIDTH = 788
        self.HEIGHT = 197
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
        
        self.TOP_TEXT = widget.QLabel("Прогноз на 12 годин")
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
    
        self.ICON_FORECAST = widget.QFrame()
        self.ICON_FORECAST.setFixedSize(core.QSize(728,24))
        self.ICON_FORECAST.setStyleSheet("background-color:blue")
        self.DOWN_LAYOUT.addWidget(self.ICON_FORECAST)


        self.GRAPH_FORECAST = widget.QFrame()
        self.GRAPH_FORECAST.setFixedSize(core.QSize(727,106))
        self.GRAPH_FORECAST.setStyleSheet("background-color:orange")
        self.DOWN_LAYOUT.addWidget(self.GRAPH_FORECAST)


        for temp in range(8):
            degree = 25
            minus_digree = 5 * temp
            self.TEMP_SCALE = widget.QLabel(str(degree - minus_digree))
            self.TEMP_SCALE.setFixedSize(core.QSize(22,15))
            self.TEMP_SCALE.setStyleSheet("background-color:orange")


        # api_request = forecast_request(city = city_name, API_KEY = API_KEY)
        
        # for item in api_request["list"][:10]:
        #     time = item["dt_txt"]
        #     temp = item["main"]["temp"]
        #     desc = item["weather"][0]["description"]
        
        #     print(f"{time} | {temp}°C | {desc}")
    
        

    
        
        
        
        
        
        
        
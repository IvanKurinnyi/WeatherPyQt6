import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtCore import pyqtSignal
import PyQt6.QtGui as gui
from PyQt6.QtSvgWidgets import QSvgWidget
from .api_request import api_request, API_KEY
from .time import find_time


class RightCityCard(widget.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WIDTH = 390
        self.HEIGHT = 303
        self.setMinimumSize(core.QSize(self.WIDTH, self.HEIGHT))

        self.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 10px; padding: 16px")
        
        
        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(16, 16, 16, 16)
        self.LAYOUT.setSpacing(16)
        self.LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        
        self.TOP_SECTION = widget.QFrame(self)
        self.TOP_SECTION.setStyleSheet("background-color: none")
        self.TOP_SECTION_LAYOUT = widget.QHBoxLayout(self.TOP_SECTION)
        self.TOP_SECTION.setLayout(self.TOP_SECTION_LAYOUT)
        self.TOP_SECTION_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TOP_SECTION_LAYOUT.setSpacing(0)
        self.LAYOUT.addWidget(self.TOP_SECTION)
        
        self.TOP_FRAME_ICON = QSvgWidget("media/city_card/navigation.svg", self.TOP_SECTION)
        self.TOP_FRAME_ICON.setStyleSheet("background-color: none")
        self.TOP_FRAME_ICON.setFixedSize(16, 16)
        self.TOP_SECTION_LAYOUT.addWidget(self.TOP_FRAME_ICON, alignment=core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)
        
        self.TOP_TEXT = widget.QLabel("Поточна позiцiя", self.TOP_SECTION)
        self.TOP_TEXT.setStyleSheet("background-color: none")
        self.TOP_TEXT.setStyleSheet("color: white; font-size: 16px; font-family: 'Roboto'; font-weight: 500;")
        self.TOP_SECTION_LAYOUT.addWidget(self.TOP_TEXT, alignment=core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)
        
        self.TOP_SECTION_LAYOUT.addStretch()
        
        self.LAYOUT.addLayout(self.TOP_SECTION_LAYOUT)
        
        self.LINE = widget.QFrame(self.TOP_SECTION)
        self.LINE.setFixedHeight(1)
        self.LINE.setStyleSheet("background-color: rgba(255,255,255,0.2);")
        self.LAYOUT.addWidget(self.LINE)
        
        self.CITY_LABEL = widget.QLabel("Днiпро", self)
        self.CITY_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.CITY_LABEL.setStyleSheet("background-color: none; font-size: 44px; font-weight: bold; color: white;")
        self.LAYOUT.addWidget(self.CITY_LABEL)
        

        
    
        # self.DEGREE_FRAME = widget.QFrame(self)
        # self.LAYOUT.addWidget(self.DEGREE_FRAME)
        # self.DEGREE_FRAME.setFixedSize(core.QSize(113,87))
        
        
        # self.DEGREE_LAYOUT = widget.QHBoxLayout(self.DEGREE_FRAME)
        # self.DEGREE_LAYOUT.setContentsMargins(0,0,0,0)
        
        
        # self.WEATHER_ICON = QSvgWidget("media/right_frame/Cloudy.svg", self.DEGREE_FRAME )
        # self.WEATHER_ICON.setStyleSheet("background-color: none")
        # self.WEATHER_ICON.setFixedSize(core.QSize(76, 76))
        # self.DEGREE_LAYOUT.addWidget(self.WEATHER_ICON, alignment=core.Qt.AlignmentFlag.AlignCenter)

        # self.DEGREE = widget.QLabel("11°",self.DEGREE_FRAME)
        # self.DEGREE.setStyleSheet("font-size:74px")
        # self.DEGREE_LAYOUT.addWidget(self.DEGREE)
        
        self.LAYOUT.addStretch()
        

        # self.WEATHER_ICON = QSvgWidget("media/weather_icon.svg")
        # self.WEATHER_ICON.setFixedSize(100, 100)
        # self.LAYOUT.addWidget(self.WEATHER_ICON, alignment=core.Qt.AlignmentFlag.AlignCenter)

        # self.TEMPERATURE_LABEL = widget.QLabel("17°")
        # self.TEMPERATURE_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        # self.TEMPERATURE_LABEL.setStyleSheet("font-size: 74px; color: white;")
        # self.LAYOUT.addWidget(self.TEMPERATURE_LABEL)


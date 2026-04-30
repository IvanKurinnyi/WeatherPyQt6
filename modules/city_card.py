import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtCore import pyqtSignal
import PyQt6.QtGui as gui
from PyQt6.QtSvgWidgets import QSvgWidget
from .api_request import api_request, API_KEY
from .time import find_time


class Card(widget.QFrame):
    selected = pyqtSignal()
    
    def __init__(self, city_name:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WIDTH = 330
        self.HEIGHT = 90

        self.IS_CHOSEN = False

        self.CHOSEN_STYLE = "background-color: rgba(0,0,0,0.2); border-radius: 8px"
        self.DESELECTED_STYLE = "background-color: rgba(0,0,0,0); border-radius: 8px"

        self.setMinimumSize(core.QSize(self.WIDTH, self.HEIGHT))
        self.city_name = city_name

        self.CARD_LAYOUT = widget.QHBoxLayout(self)
        self.CARD_LAYOUT.setContentsMargins(0,0,0,0)

        self.INFO_FRAME = widget.QFrame(self)
        self.INFO_FRAME.setFixedSize(core.QSize(330,90))
        self.INFO_LAYOUT = widget.QVBoxLayout(self.INFO_FRAME)
        self.INFO_FRAME.setContentsMargins(0,0,0,0)
        self.INFO_FRAME.setLayout(self.INFO_LAYOUT)
        self.CARD_LAYOUT.addWidget(self.INFO_FRAME)
    
        self.INFO_FRAME.setStyleSheet(self.DESELECTED_STYLE)

    
        self.UPPER_INFO = widget.QFrame(self.INFO_FRAME)
        self.UPPER_INFO.setFixedSize(core.QSize(314,48))
        self.UPPER_LAYOUT = widget.QHBoxLayout(self.UPPER_INFO)
        self.UPPER_LAYOUT.setContentsMargins(0,0,0,0)
        self.UPPER_LAYOUT.setSpacing(0)
        self.UPPER_INFO.setLayout(self.UPPER_LAYOUT)
        self.INFO_LAYOUT.addWidget(self.UPPER_INFO)

        self.UPPER_LEFT = widget.QFrame(self.UPPER_INFO)
        self.UPPER_LEFT.setFixedSize(core.QSize(247,50))
        self.UPPER_LAYOUT.addWidget(self.UPPER_LEFT)
        self.UPPER_LEFT_LAYOUT = widget.QVBoxLayout(self.UPPER_LEFT)
        self.UPPER_LEFT_LAYOUT.setContentsMargins(0,0,0,0)
        self.UPPER_LEFT.setLayout(self.UPPER_LEFT_LAYOUT)
        
        
        self.UPPER_UPPER = widget.QFrame(self.UPPER_LEFT)
        self.UPPER_UPPER.setFixedSize(core.QSize(247,26))
        self.UPPER_LEFT_LAYOUT.addWidget(self.UPPER_UPPER)

        self.UPPER_UPPER_LAYOUT = widget.QHBoxLayout(self.UPPER_UPPER)
        self.UPPER_UPPER_LAYOUT.setContentsMargins(0,0,0,0)
        self.UPPER_UPPER.setLayout(self.UPPER_UPPER_LAYOUT)

        if city_name == "Дніпро":
            self.ICON_FRAME = widget.QFrame(self.UPPER_UPPER)
            self.ICON_FRAME.setFixedSize(core.QSize(16,16))
            self.UPPER_UPPER_LAYOUT.addWidget(self.ICON_FRAME)
            self.ICON_LAYOUT = widget.QVBoxLayout(self.ICON_FRAME)
            self.ICON_LAYOUT.setContentsMargins(0,0,0,0)
            self.ICON_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
            self.POSITION_ICON = QSvgWidget("media/city_card/navigation.svg", self.ICON_FRAME)
            self.POSITION_ICON.setFixedSize(16, 16)
            self.ICON_LAYOUT.addWidget(self.POSITION_ICON, alignment=core.Qt.AlignmentFlag.AlignLeft)
            self.POSITION_PICTURE = gui.QPixmap("media/city_card/navigation.svg")
            
        self.CITY_NAME_FRAME = widget.QFrame(self.UPPER_UPPER)
        self.UPPER_UPPER_LAYOUT.addWidget(self.CITY_NAME_FRAME)

        self.UPPER_UPPER_LABEL = widget.QLabel(self.CITY_NAME_FRAME)
        self.UPPER_UPPER_LABEL.setContentsMargins(0,0,0,0)
        self.UPPER_UPPER_LABEL.setFixedSize(core.QSize(240,29))
        
        self.UPPER_UPPER_LABEL.setStyleSheet("font-size:28px;font-family: 'Roboto';font-weight:500;color:white; margin-top: -5px")
        
        self.UPPER_UPPER_LABEL.setText(city_name)
        

        self.UPPER_BOTTOM = widget.QFrame(self.UPPER_LEFT)
        self.UPPER_BOTTOM.setFixedSize(core.QSize(247,21))
        self.UPPER_BOTTOM_LAYOUT = widget.QHBoxLayout(self.UPPER_BOTTOM)
        self.UPPER_BOTTOM_LAYOUT.setContentsMargins(0,0,0,0)
        self.UPPER_BOTTOM.setLayout(self.UPPER_BOTTOM_LAYOUT)
        
        self.TIME_LABEL = widget.QLabel(self.UPPER_BOTTOM)
        self.TIME_LABEL.setContentsMargins(0,0,0,0)
        self.TIME_LABEL.setStyleSheet("font-size:14px;font-family: 'Roboto';font-weight:500;color:white")
        self.TIME_LABEL.setText("")
        self.UPPER_BOTTOM_LAYOUT.addWidget(self.TIME_LABEL)
        
        self.UPPER_LEFT_LAYOUT.addWidget(self.UPPER_BOTTOM)




        self.UPPER_RIGHT = widget.QFrame(self.UPPER_INFO)
        self.UPPER_RIGHT.setFixedSize(core.QSize(67,52))
        self.UPPER_LAYOUT.addWidget(self.UPPER_RIGHT)
        self.UPPER_RIGHT_LABEL = widget.QLabel(self.UPPER_RIGHT)
        self.UPPER_LAYOUT.addWidget(self.UPPER_RIGHT_LABEL)
        self.UPPER_RIGHT_LABEL.setContentsMargins(0,0,0,0)
        self.UPPER_RIGHT_LABEL.setFixedSize(core.QSize(70,52))
        self.UPPER_RIGHT_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignRight)
        self.UPPER_RIGHT_LABEL.setStyleSheet("font-size:44px;font-family: 'Roboto';font-weight:500;color:white; margin-top:-10px")
        self.UPPER_RIGHT_LABEL.setText("")


        self.BOTTOM_INFO = widget.QFrame(self.INFO_FRAME)
        self.BOTTOM_INFO.setFixedSize(core.QSize(314,14))
        self.INFO_LAYOUT.addWidget(self.BOTTOM_INFO)

        self.BOTTOM_LAYOUT = widget.QHBoxLayout(self.BOTTOM_INFO)
        self.BOTTOM_LAYOUT.setContentsMargins(0,0,0,0)
        
        self.BOTTOM_LEFT = widget.QLabel(self.BOTTOM_INFO)
        self.BOTTOM_LEFT.setFixedSize(core.QSize(150,14))
        self.BOTTOM_LEFT.setStyleSheet("font-size:12px;font-family: 'Roboto';font-weight:500;color:white;")
        self.BOTTOM_LEFT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.BOTTOM_LEFT.setText("")
        self.BOTTOM_LAYOUT.addWidget(self.BOTTOM_LEFT, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.BOTTOM_RIGHT = widget.QLabel(self.BOTTOM_INFO)
        self.BOTTOM_RIGHT.setFixedSize(core.QSize(150,14))
        self.BOTTOM_RIGHT.setStyleSheet("font-size:12px;font-family: 'Roboto';font-weight:500;color:white")
        self.BOTTOM_RIGHT.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        self.BOTTOM_RIGHT.setText("")
        self.BOTTOM_LAYOUT.addWidget(self.BOTTOM_RIGHT, alignment=core.Qt.AlignmentFlag.AlignRight)

        self.update_weather(city_name = city_name)
        self.TIMER = core.QTimer(self)
        self.TIMER.timeout.connect(lambda: self.update_weather(city_name = city_name))
        self.TIMER.start(300000)

        self.update_style()

    def update_style(self):
        if self.IS_CHOSEN:
            self.INFO_FRAME.setStyleSheet(self.CHOSEN_STYLE)
            self.UPPER_INFO.setStyleSheet(self.DESELECTED_STYLE)
            self.BOTTOM_INFO.setStyleSheet(self.DESELECTED_STYLE)
        else:
            self.INFO_FRAME.setStyleSheet(self.DESELECTED_STYLE)
            self.UPPER_INFO.setStyleSheet(self.DESELECTED_STYLE)
            self.BOTTOM_INFO.setStyleSheet(self.DESELECTED_STYLE)
    
    def deselect(self):
        """Убирает выбор с карточки"""
        self.IS_CHOSEN = False
        self.update_style()
        
    def mousePressEvent(self, event):
        """Обработчик клика по карточке"""
        self.IS_CHOSEN = True
        self.update_style()
        self.selected.emit()

    def update_weather(self, city_name):
            city_request = api_request(city=city_name, API_KEY=API_KEY)
        
            temp = str(round(city_request["main"]["temp"]))
            temp_max = str(city_request["main"]["temp_max"])
            temp_min = str(city_request["main"]["temp_min"])
            description:str = city_request["weather"][0]["description"]
            offset:int = int(city_request["timezone"])
            self.UPPER_RIGHT_LABEL.setText(temp + "°")
            self.BOTTOM_LEFT.setText(description.capitalize())
            self.BOTTOM_RIGHT.setText(f"Макс.: {temp_max}°, мін.: {temp_min}°")
            self.TIME_LABEL.setText(find_time(offset))
            print("Погода оновлена!!!!")









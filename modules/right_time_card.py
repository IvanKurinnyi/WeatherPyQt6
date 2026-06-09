import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtSvgWidgets import QSvgWidget

from datetime import datetime
import locale
from .time import find_time
from .api_request import api_request, API_KEY

class RightTimeCard(widget.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WIDTH = 390
        self.HEIGHT = 303
        self.setMinimumSize(core.QSize(self.WIDTH, self.HEIGHT))

        self.setStyleSheet("""
            RightTimeCard {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 10px;
            }
        """)
       
        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(16, 16, 16, 16)
        self.LAYOUT.setSpacing(8)
        
        locale.setlocale(locale.LC_TIME, "uk_UA.UTF-8")

        self.NOW = datetime.now()

        self.TOP_SECTION = widget.QWidget()
        self.TOP_SECTION_LAYOUT = widget.QVBoxLayout(self.TOP_SECTION)
        self.TOP_SECTION_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TOP_SECTION_LAYOUT.setSpacing(0)

        self.TOP_TEXT = widget.QLabel("Сьогоднi")
        self.TOP_TEXT.setStyleSheet("color: white; font-size: 16px; font-family: 'Roboto'; font-weight: 500;")
        self.LAYOUT.addWidget(self.TOP_TEXT, alignment=core.Qt.AlignmentFlag.AlignLeft)

        
        self.LINE = widget.QFrame()
        self.LINE.setFixedHeight(1)
        self.LINE.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")

        
        self.TOP_SECTION_LAYOUT.addWidget(self.LINE)
        
        
        self.LAYOUT.addWidget(self.TOP_SECTION)
        

        self.DATE_FRAME = widget.QFrame()
        self.DATE_LAYOUT = widget.QHBoxLayout(self.DATE_FRAME)
        
        self.WEEK_DAY = widget.QLabel(self.NOW.strftime("%A").capitalize(), self.DATE_FRAME)
        self.WEEK_DAY.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.WEEK_DAY.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Roboto'; color: white; background: none;")
        self.DATE_LAYOUT.addWidget(self.WEEK_DAY)

        self.DATE = widget.QLabel(self.NOW.strftime("%d.%m.%Y"), self.DATE_FRAME)
        self.DATE.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        self.DATE.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Roboto'; color: white; background: none;")
        self.DATE_LAYOUT.addWidget(self.DATE)

        self.LAYOUT.addWidget(self.DATE_FRAME)
        
        
        self.WATCH_FRAME = widget.QWidget()
        
        self.WATCH_FRAME.setSizePolicy(widget.QSizePolicy.Policy.Expanding, widget.QSizePolicy.Policy.Expanding)
        
        self.WATCH_LAYOUT = widget.QGridLayout(self.WATCH_FRAME)
        self.WATCH_LAYOUT.setContentsMargins(0, 0, 0, 0)

        self.WATCH = QSvgWidget("media/right_frame/watch.svg")
        self.WATCH.setSizePolicy(widget.QSizePolicy.Policy.Expanding, widget.QSizePolicy.Policy.Expanding)
        self.WATCH.setMinimumSize(168, 168)
        self.WATCH.renderer().setAspectRatioMode(core.Qt.AspectRatioMode.KeepAspectRatio)

        self.TIME = widget.QLabel("")
        self.TIME.setStyleSheet("font-size:29px; color: white; font-weight: 500; font-family: 'Roboto'; background: transparent;")
        self.TIME.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.WATCH_LAYOUT.addWidget(self.WATCH, 0, 0, core.Qt.AlignmentFlag.AlignCenter)
        self.WATCH_LAYOUT.addWidget(self.TIME, 0, 0, core.Qt.AlignmentFlag.AlignCenter)

        self.TIME.raise_() 
        
        self.LAYOUT.addStretch(1)
        
        self.LAYOUT.addWidget(self.WATCH_FRAME, 5) 
        
        self.LAYOUT.addStretch(1) 
 
    def minute_update(self, city_name):
        now = datetime.now()
        minutes = now.minute
        if self.TIME.text()[3:] != minutes:
            city_request = api_request(city=city_name, API_KEY=API_KEY)
            offset:int = int(city_request["timezone"])
            self.TIME.setText(find_time(offset))
        
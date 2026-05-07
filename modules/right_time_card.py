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
        self.setFixedSize(core.QSize(self.WIDTH, self.HEIGHT))

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
        
        self.WEEK_DAY = widget.QLabel(self.NOW.strftime("%A"), self.DATE_FRAME)
        self.WEEK_DAY.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.WEEK_DAY.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Roboto'; color: white; background: none;")
        self.DATE_LAYOUT.addWidget(self.WEEK_DAY)

        self.DATE = widget.QLabel(self.NOW.strftime("%d.%m.%Y"), self.DATE_FRAME)
        self.DATE.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        self.DATE.setStyleSheet("font-size: 24px; font-weight: bold; font-family: 'Roboto'; color: white; background: none;")
        self.DATE_LAYOUT.addWidget(self.DATE)

        self.LAYOUT.addWidget(self.DATE_FRAME)
        
        
        self.WATCH_FRAME = widget.QWidget()
        self.WATCH_LAYOUT = widget.QStackedLayout(self.WATCH_FRAME)
    
        self.WATCH_LAYOUT.setStackingMode(widget.QStackedLayout.StackingMode.StackAll)

       
        self.WATCH = QSvgWidget("media/right_frame/watch.svg")
        self.WATCH.setFixedSize(168, 168)

        
        self.TIME = widget.QLabel("")
        self.TIME.setStyleSheet("font-size:29px; color: white; font-weight: 500; font-family: 'Roboto';background: transparent;")
        self.TIME.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.WATCH_LAYOUT.addWidget(self.WATCH)
        self.WATCH_LAYOUT.addWidget(self.TIME)
        self.TIME.raise_()

        self.LAYOUT.addWidget(self.WATCH_FRAME, alignment=core.Qt.AlignmentFlag.AlignCenter)


        self.LAYOUT.addStretch()
 
    def minute_update(self, city_name):
        now = datetime.now()
        minutes = now.minute
        if self.TIME.text()[3:] != minutes:
            city_request = api_request(city=city_name, API_KEY=API_KEY)
            offset:int = int(city_request["timezone"])
            self.TIME.setText(find_time(offset))
        
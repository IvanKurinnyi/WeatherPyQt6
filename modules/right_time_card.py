import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtSvgWidgets import QSvgWidget
from .read_write_json import read_json, create_json

from datetime import datetime
import locale
from .time import find_time
from .api_request import api_request, API_KEY, LANG
from .translations import t, weekday_name


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

        
        self._current_city = None

        self.TOP_SECTION = widget.QWidget()
        self.TOP_SECTION_LAYOUT = widget.QVBoxLayout(self.TOP_SECTION)
        self.TOP_SECTION_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TOP_SECTION_LAYOUT.setSpacing(0)

        
        self.TOP_TEXT = widget.QLabel(t("today"))
        self.TOP_TEXT.setStyleSheet("color: white; font-size: 16px; font-family: 'Roboto'; font-weight: 500;")
        self.LAYOUT.addWidget(self.TOP_TEXT, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.LINE = widget.QFrame()
        self.LINE.setFixedHeight(1)
        self.LINE.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")

        self.TOP_SECTION_LAYOUT.addWidget(self.LINE)

        self.LAYOUT.addWidget(self.TOP_SECTION)

        self.DATE_FRAME = widget.QFrame()
        self.DATE_LAYOUT = widget.QHBoxLayout(self.DATE_FRAME)

        day_index = self.NOW.weekday()

        self.WEEK_DAY = widget.QLabel(weekday_name(day_index), self.DATE_FRAME)
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
        self.WATCH_FRAME.setMinimumSize(168, 168)

        self.WATCH_LAYOUT = widget.QGridLayout(self.WATCH_FRAME)
        self.WATCH_LAYOUT.setContentsMargins(0, 0, 0, 0)

        self.WATCH = QSvgWidget("media/right_frame/watch.svg")
        self.WATCH.setSizePolicy(widget.QSizePolicy.Policy.Expanding, widget.QSizePolicy.Policy.Expanding)
        self.WATCH.renderer().setAspectRatioMode(core.Qt.AspectRatioMode.KeepAspectRatio)

        self.TIME = widget.QLabel("")
        self.TIME.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.change_clock()

        self.WATCH_LAYOUT.addWidget(self.WATCH, 0, 0, core.Qt.AlignmentFlag.AlignCenter)
        self.WATCH_LAYOUT.addWidget(self.TIME, 0, 0, core.Qt.AlignmentFlag.AlignCenter)

        self.TIME.raise_()

        self.LAYOUT.addStretch(1)

        self.LAYOUT.addWidget(self.WATCH_FRAME, 5)

        self.LAYOUT.addStretch(1)

        
        LANG.subscribe(self.retranslate_ui)

    def minute_update(self, city_name):
        self._current_city = city_name
        now = datetime.now()
        minutes = now.minute
        if self.TIME.text()[3:] != minutes:
            city_request = api_request(city=city_name, API_KEY=API_KEY, lang=LANG.current)
            offset: int = int(city_request["timezone"])
            self.TIME.setText(find_time(offset))

    def retranslate_ui(self):
        
        self.TOP_TEXT.setText(t("today"))

        day_index = datetime.now().weekday()
        self.WEEK_DAY.setText(weekday_name(day_index))

        if self._current_city:
            self.minute_update(self._current_city)

    def closeEvent(self, event):
        
        LANG.unsubscribe(self.retranslate_ui)
        super().closeEvent(event)

    def change_clock(self):

        settings = read_json("settings.json")

        print(settings.get("currentResolution"))

        if settings.get("currentResolution") == ["1200", "800"]:
            self.WATCH.setMinimumSize(168, 168)
            self.TIME.setStyleSheet("font-size:29px; color: white; font-weight: 500; font-family: 'Roboto'; background: transparent;")

        elif settings.get("currentResolution") == ["1440", "1024"]:
            self.WATCH.setMinimumSize(260, 260)
            self.TIME.setStyleSheet("font-size:36px; color: white; font-weight: 500; font-family: 'Roboto'; background: transparent;")

        elif settings.get("currentResolution") == ["1512", "982"]:
            self.WATCH.setMinimumSize(255, 255)
            self.TIME.setStyleSheet("font-size:36px; color: white; font-weight: 500; font-family: 'Roboto'; background: transparent;")

        elif settings.get("currentResolution") == ["1728", "1117"]:
            self.WATCH.setMinimumSize(350, 350)
            self.TIME.setStyleSheet("font-size:44px; color: white; font-weight: 500; font-family: 'Roboto'; background: transparent;")
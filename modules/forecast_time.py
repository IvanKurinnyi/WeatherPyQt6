import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .read_write_json import read_json, create_json
from .api_request import forecast_request, API_KEY, LANG
from .translations import t


class ForeCastTime(widget.QFrame):
    def __init__(self, city_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WIDTH = 788
        self.HEIGHT = 157
        self.setFixedHeight(self.HEIGHT)
        self.setMinimumWidth(self.WIDTH)

        self.ALL_FORECAST_DATA = []
        self.MAX_CARDS = 30

        
        self._current_city = city_name

        self.setStyleSheet("background-color: rgba(0,0,0,0.2); border: none; border-radius: 10px")


        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(16, 16, 16, 16)
        self.LAYOUT.setSpacing(16)


        self.TOP_FRAME = widget.QFrame()
        self.TOP_FRAME.setStyleSheet("background-color: none")
        self.TOP_LAYOUT = widget.QVBoxLayout(self.TOP_FRAME)
        self.TOP_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TOP_TEXT = widget.QLabel("")
        self.TOP_TEXT.setStyleSheet("font-size:16px; color:white")
        self.TOP_LAYOUT.addWidget(self.TOP_TEXT)

        self.LINE = widget.QFrame()
        self.LINE.setFixedHeight(1)
        self.LINE.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")
        self.TOP_LAYOUT.addWidget(self.LINE)
        self.LAYOUT.addWidget(self.TOP_FRAME)


        self.DOWN_FRAME = widget.QFrame()
        self.DOWN_FRAME.setStyleSheet("background-color: none")
        self.DOWN_LAYOUT = widget.QHBoxLayout(self.DOWN_FRAME)
        self.DOWN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.LAYOUT.addWidget(self.DOWN_FRAME)


        self.LEFT_BUTTON = widget.QPushButton()
        self.LEFT_BUTTON.setIcon(gui.QIcon("media/right_frame/arrow_left.svg"))
        self.LEFT_BUTTON.setFixedSize(16, 16)
        self.LEFT_BUTTON.clicked.connect(self.scroll_left)
        self.DOWN_LAYOUT.addWidget(self.LEFT_BUTTON)

        self.SCROLL_AREA = widget.QScrollArea()
        self.SCROLL_AREA.setFixedHeight(85)
        self.SCROLL_AREA.setMinimumWidth(675)
        self.SCROLL_AREA.setWidgetResizable(True)


        self.SCROLL_AREA.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.SCROLL_AREA.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:horizontal { height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; }
            QScrollBar::handle:horizontal { background: rgba(255,255,255,0.4); border-radius: 2px; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
        """)

        self.SCROLL_AREA.wheelEvent = self.scroll_area_wheel_event

        self.CENTRAL = widget.QWidget()
        self.CENTRAL.setStyleSheet("background: transparent;")
        self.CENTRAL_LAYOUT = widget.QHBoxLayout(self.CENTRAL)
        self.CENTRAL_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CENTRAL_LAYOUT.setSpacing(10)

        self.CENTRAL_LAYOUT.setSizeConstraint(widget.QLayout.SizeConstraint.SetMinAndMaxSize)

        self.SCROLL_AREA.setWidget(self.CENTRAL)
        self.DOWN_LAYOUT.addWidget(self.SCROLL_AREA, stretch = 1)


        self.RIGHT_BUTTON = widget.QPushButton()
        self.RIGHT_BUTTON.setIcon(gui.QIcon("media/right_frame/arrow_right.svg"))
        self.RIGHT_BUTTON.setFixedSize(16, 16)
        self.RIGHT_BUTTON.clicked.connect(self.scroll_right)
        self.DOWN_LAYOUT.addWidget(self.RIGHT_BUTTON)

        
        LANG.subscribe(self.retranslate_ui)

    def scroll_area_wheel_event(self, event):

        angle = event.angleDelta().y()
        if angle == 0:
            angle = event.angleDelta().x()

        current = self.SCROLL_AREA.horizontalScrollBar().value()

        self.SCROLL_AREA.horizontalScrollBar().setValue(current - angle)
        event.accept()

    def update_city_time(self, city_name):
        self._current_city = city_name
        response = forecast_request(city=city_name, API_KEY=API_KEY)
        if response and "list" in response:
            description = response["list"][0]["weather"][0]["description"]
            self.TOP_TEXT.setText(f"{description.capitalize()}")

            self.ALL_FORECAST_DATA = response["list"]
            self.render_forecast()

    def retranslate_ui(self):
        if self._current_city:
            self.update_city_time(self._current_city)

    def closeEvent(self, event):
        LANG.unsubscribe(self.retranslate_ui)
        super().closeEvent(event)

    def render_forecast(self):

        while self.CENTRAL_LAYOUT.count():
            item = self.CENTRAL_LAYOUT.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()


        self.SCROLL_AREA.horizontalScrollBar().setValue(0)


        display_data = self.ALL_FORECAST_DATA[:self.MAX_CARDS]

        for i, item in enumerate(display_data):
            time_str = item["dt_txt"]
            temp = round(item["main"]["temp"])
            icon_code = item["weather"][0]["icon"]

            card = widget.QFrame()
            card.setFixedSize(65, 85)
            card_layout = widget.QVBoxLayout(card)
            card_layout.setContentsMargins(0, 0, 0, 0)
            card_layout.setSpacing(4)

            is_now = (i == 0)
            label_time = widget.QLabel(t("now") if is_now else time_str[11:16])

            label_time.setStyleSheet("color: white; font-size: 13px")
            label_time.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

            icon_label = widget.QLabel()
            pix = gui.QPixmap(f"media/right_frame/weather_icons_white/{icon_code}.svg")
            icon_label.setPixmap(pix.scaled(24, 24, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
            icon_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

            label_temp = widget.QLabel(f"{temp}°")
            label_temp.setStyleSheet("color: white; font-size: 15px; font-weight: bold")
            label_temp.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

            card_layout.addWidget(label_time)
            card_layout.addWidget(icon_label)
            card_layout.addWidget(label_temp)

            self.CENTRAL_LAYOUT.addWidget(card)

    def scroll_left(self):

        current = self.SCROLL_AREA.horizontalScrollBar().value()
        self.SCROLL_AREA.horizontalScrollBar().setValue(current - 75)

    def scroll_right(self):

        current = self.SCROLL_AREA.horizontalScrollBar().value()
        self.SCROLL_AREA.horizontalScrollBar().setValue(current + 75)
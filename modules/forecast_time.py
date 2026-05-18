import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .api_request import forecast_request
from .api import API_KEY

class ForeCastTime(widget.QFrame):
    def __init__(self, city_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WIDTH = 788
        self.HEIGHT = 157
        self.setFixedSize(core.QSize(self.WIDTH, self.HEIGHT))
        
        
        self.ALL_FORECAST_DATA = [] 
        self.CURRENT_INDEX = 0      
        self.ITEMS_TO_SHOW = 7

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
        self.LEFT_BUTTON.clicked.connect(self.show_previous)
        self.DOWN_LAYOUT.addWidget(self.LEFT_BUTTON)

        
        self.CENTRAL = widget.QFrame()
        self.CENTRAL.setFixedSize(676, 85)
        self.CENTRAL_LAYOUT = widget.QHBoxLayout(self.CENTRAL)
        self.CENTRAL_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CENTRAL_LAYOUT.setSpacing(10) 
        self.DOWN_LAYOUT.addWidget(self.CENTRAL, alignment=core.Qt.AlignmentFlag.AlignCenter)

        
        self.RIGHT_BUTTON = widget.QPushButton()
        self.RIGHT_BUTTON.setIcon(gui.QIcon("media/right_frame/arrow_right.svg"))
        self.RIGHT_BUTTON.setFixedSize(16, 16)
        self.RIGHT_BUTTON.clicked.connect(self.show_next)
        self.DOWN_LAYOUT.addWidget(self.RIGHT_BUTTON)

    def update_city_time(self, city_name):

        response = forecast_request(city=city_name, API_KEY=API_KEY)
        description:str = response["list"][0]["weather"][0]["description"]
        self.TOP_TEXT.setText(f"{description.capitalize()}")
        if response and "list" in response:
            self.ALL_FORECAST_DATA = response["list"]
            self.CURRENT_INDEX = 0
            self.render_forecast()


    def render_forecast(self):
        """Очистка и отрисовка текущего среза данных"""

        while self.CENTRAL_LAYOUT.count():
            item = self.CENTRAL_LAYOUT.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        
        display_data = self.ALL_FORECAST_DATA[self.CURRENT_INDEX : self.CURRENT_INDEX + self.ITEMS_TO_SHOW]
        
        for i, item in enumerate(display_data):
            time_str = item["dt_txt"]
            temp = round(item["main"]["temp"])
            icon_code = item["weather"][0]["icon"]

            card = widget.QFrame()
            card.setFixedSize(65, 85)
            card_layout = widget.QVBoxLayout(card)
            card_layout.setContentsMargins(0, 0, 0, 0)
            card_layout.setSpacing(4)
            
            is_now = (self.CURRENT_INDEX == 0 and i == 0)
            label_time = widget.QLabel("Зараз" if is_now else time_str[11:16])
            label_time.setStyleSheet("color: white; font-size: 13px")
            label_time.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            
            icon_label = widget.QLabel()
            pix = gui.QPixmap(f"media/right_frame/weather_icons_white/{icon_code}.svg")
            icon_label.setPixmap(pix.scaled(30, 30, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
            icon_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            

            label_temp = widget.QLabel(f"{temp}°")
            label_temp.setStyleSheet("color: white; font-size: 15px; font-weight: bold")
            label_temp.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            
            card_layout.addWidget(label_time)
            card_layout.addWidget(icon_label)
            card_layout.addWidget(label_temp)
            
            self.CENTRAL_LAYOUT.addWidget(card)

    def show_next(self):

        if self.CURRENT_INDEX + self.ITEMS_TO_SHOW < len(self.ALL_FORECAST_DATA):
            self.CURRENT_INDEX += 1
            self.render_forecast()

    def show_previous(self):

        if self.CURRENT_INDEX > 0:
            self.CURRENT_INDEX -= 1
            self.render_forecast()
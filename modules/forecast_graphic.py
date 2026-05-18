import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .api_request import forecast_request
from .api import API_KEY

class ForeCastGraph(widget.QFrame):
    def __init__(self, city_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WIDTH = 788
        self.HEIGHT = 197
        self.setFixedSize(core.QSize(self.WIDTH, self.HEIGHT))
        
        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(16, 16, 16, 16)
        self.LAYOUT.setSpacing(16)
        self.setStyleSheet("background-color: rgba(0,0,0,0.2); border: none; border-radius: 10px")

        self.TOP_FRAME = widget.QFrame()
        self.TOP_FRAME.setStyleSheet("background-color: none")
        self.TOP_LAYOUT = widget.QVBoxLayout(self.TOP_FRAME)
        self.TOP_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TOP_LAYOUT.setSpacing(8)
        self.LAYOUT.addWidget(self.TOP_FRAME)

        self.TOP_TEXT = widget.QLabel("Прогноз на найближчий час")
        self.TOP_TEXT.setStyleSheet("font-size:16px; color:white")
        self.TOP_LAYOUT.addWidget(self.TOP_TEXT)

        self.LINE = widget.QFrame()
        self.LINE.setFixedHeight(1)
        self.LINE.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")
        self.TOP_LAYOUT.addWidget(self.LINE)

        self.DOWN_FRAME = widget.QFrame()
        self.DOWN_FRAME.setStyleSheet("background-color: none")
        self.DOWN_LAYOUT = widget.QVBoxLayout(self.DOWN_FRAME)
        self.DOWN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.DOWN_LAYOUT.setSpacing(0)
        self.LAYOUT.addWidget(self.DOWN_FRAME)

        self.ICON_FORECAST = widget.QFrame()
        self.ICON_FORECAST.setFixedSize(core.QSize(728, 24))
        self.ICON_LAYOUT = widget.QHBoxLayout(self.ICON_FORECAST)
        self.ICON_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.ICON_LAYOUT.setSpacing(0)
        self.DOWN_LAYOUT.addWidget(self.ICON_FORECAST, alignment=core.Qt.AlignmentFlag.AlignLeft)


        self.GRAPHIC = widget.QFrame()
        self.GRAPHIC_LAYOUT = widget.QHBoxLayout(self.GRAPHIC)
        self.GRAPHIC_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.GRAPHIC_LAYOUT.setSpacing(6)
        self.DOWN_LAYOUT.addWidget(self.GRAPHIC)

        self.GRAPHIC_FRAME = widget.QFrame()
        self.GRAPHIC_FRAME.setFixedSize(core.QSize(726, 95))
        self.COLUMN_LAYOUT = widget.QHBoxLayout(self.GRAPHIC_FRAME)
        self.COLUMN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.COLUMN_LAYOUT.setSpacing(0)
        self.GRAPHIC_LAYOUT.addWidget(self.GRAPHIC_FRAME)
        
        self.NUMBERS_FRAME = widget.QFrame()
        self.NUMBERS_FRAME.setFixedSize(core.QSize(22, 95))
        self.TEMP_LAYOUT = widget.QVBoxLayout(self.NUMBERS_FRAME)
        self.TEMP_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TEMP_LAYOUT.setSpacing(1)
        self.GRAPHIC_LAYOUT.addWidget(self.NUMBERS_FRAME)

        for temp in range(7):
            degree = 25 - (5 * temp)
            label = widget.QLabel(str(degree))
            label.setFixedSize(core.QSize(22, 15))
            label.setStyleSheet("font-size: 10px; color: rgba(255,255,255,0.6);")
            self.TEMP_LAYOUT.addWidget(label, alignment=core.Qt.AlignmentFlag.AlignCenter)

        self.update_forecast(city_name)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            child_widget = item.widget()
            if child_widget is not None:
                child_widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())

    def update_forecast(self, city_name):
        try:
            api_data = forecast_request(city=city_name, API_KEY=API_KEY)
            raw_data = api_data["list"][:16]
        except Exception as e:
            print(f"Помилка оновлення графіка: {e}")
            return

        self.clear_layout(self.ICON_LAYOUT)
        self.clear_layout(self.COLUMN_LAYOUT)


        interpolated_data = []
        for i in range(len(raw_data) - 1):
            t1 = float(raw_data[i]["main"]["temp"])
            t2 = float(raw_data[i+1]["main"]["temp"])
            icon = raw_data[i]["weather"][0]["icon"]
            interpolated_data.append({"temp": t1, "icon": icon, "is_main": True})
            interpolated_data.append({"temp": t1 + (t2 - t1) * (1/3), "icon": None, "is_main": False})
            interpolated_data.append({"temp": t1 + (t2 - t1) * (2/3), "icon": None, "is_main": False})

        last_item = raw_data[-1]
        interpolated_data.append({"temp": float(last_item["main"]["temp"]), "icon": last_item["weather"][0]["icon"], "is_main": True})

   
        min_temp = -5
        temp_range = 30
        max_height = 95
        total_points = len(interpolated_data)
        block_width = int(726 / total_points)
        bar_width = max(2, int(block_width * 0.75))

        for item in interpolated_data:

            icon_container = widget.QFrame()
            icon_container.setFixedSize(core.QSize(block_width, 24))
            if item["is_main"] and item["icon"]:
                icon_label = widget.QLabel(icon_container)
                pix = gui.QPixmap(f"media/right_frame/weather_icons_white/{item['icon']}.svg")
                icon_label.setPixmap(pix.scaled(16, 16, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
                icon_label.setGeometry(int((block_width - 16) / 2), 2, 16, 16)
            self.ICON_LAYOUT.addWidget(icon_container)

            col_container = widget.QFrame()
            col_container.setFixedSize(core.QSize(block_width, max_height))
            col_box = widget.QVBoxLayout(col_container)
            col_box.setContentsMargins(0, 0, 0, 0)
            
            column = widget.QFrame()
            calc_h = int(((item["temp"] - min_temp) / temp_range) * max_height)
            column.setFixedSize(core.QSize(bar_width, max(1, calc_h)))
            column.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FDD835, stop:1 #4FC3F7);
                border-radius: 2px;
            """)
            col_box.addWidget(column, alignment=core.Qt.AlignmentFlag.AlignBottom | core.Qt.AlignmentFlag.AlignHCenter)
            self.COLUMN_LAYOUT.addWidget(col_container)
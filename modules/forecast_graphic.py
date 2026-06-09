import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .api_request import forecast_request, API_KEY

class ForeCastGraph(widget.QFrame):
    def __init__(self, city_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.HEIGHT = 197
        self.setFixedHeight(self.HEIGHT)
        
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

        # --- Создаем структуру для Иконок (зеркальную структуре графика) ---
        self.ICON_FORECAST = widget.QFrame()
        self.ICON_FORECAST.setFixedHeight(24)
        self.ICON_LAYOUT = widget.QHBoxLayout(self.ICON_FORECAST)
        self.ICON_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.ICON_LAYOUT.setSpacing(6) # Такой же отступ, как у графика ниже
        self.DOWN_LAYOUT.addWidget(self.ICON_FORECAST)

        # Контейнер, куда будут сыпаться сами иконки
        self.ICON_BARS_FRAME = widget.QFrame()
        self.ICON_BARS_LAYOUT = widget.QHBoxLayout(self.ICON_BARS_FRAME)
        self.ICON_BARS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.ICON_BARS_LAYOUT.setSpacing(0)
        self.ICON_LAYOUT.addWidget(self.ICON_BARS_FRAME)

        # Невидимая заглушка справа, чтобы сдвинуть иконки влево от цифр градусов
        self.ICON_SPACER = widget.QFrame()
        self.ICON_SPACER.setFixedWidth(22) # Ровно по ширине NUMBERS_FRAME
        self.ICON_LAYOUT.addWidget(self.ICON_SPACER)

        # --- Структура для Столбиков Графика ---
        self.GRAPHIC = widget.QFrame()
        self.GRAPHIC_LAYOUT = widget.QHBoxLayout(self.GRAPHIC)
        self.GRAPHIC_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.GRAPHIC_LAYOUT.setSpacing(6)
        self.DOWN_LAYOUT.addWidget(self.GRAPHIC)

        self.GRAPHIC_FRAME = widget.QFrame()
        self.GRAPHIC_FRAME.setFixedHeight(95)
        self.COLUMN_LAYOUT = widget.QHBoxLayout(self.GRAPHIC_FRAME)
        self.COLUMN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.COLUMN_LAYOUT.setSpacing(0)
        self.GRAPHIC_LAYOUT.addWidget(self.GRAPHIC_FRAME)
        
        self.NUMBERS_FRAME = widget.QFrame()
        self.NUMBERS_FRAME.setFixedHeight(95)
        self.NUMBERS_FRAME.setFixedWidth(22) # Зафиксировали ширину для точного выравнивания
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

        self.interpolated_data = []
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

        self.interpolated_data = []
        for i in range(len(raw_data) - 1):
            t1 = float(raw_data[i]["main"]["temp"])
            t2 = float(raw_data[i+1]["main"]["temp"])
            icon = raw_data[i]["weather"][0]["icon"]
            self.interpolated_data.append({"temp": t1, "icon": icon, "is_main": True})
            self.interpolated_data.append({"temp": t1 + (t2 - t1) * (1/3), "icon": None, "is_main": False})
            self.interpolated_data.append({"temp": t1 + (t2 - t1) * (2/3), "icon": None, "is_main": False})

        last_item = raw_data[-1]
        self.interpolated_data.append({"temp": float(last_item["main"]["temp"]), "icon": last_item["weather"][0]["icon"], "is_main": True})

        self.draw_graph()

    def draw_graph(self):
        self.clear_layout(self.ICON_BARS_LAYOUT) # Очищаем только контейнер с иконками
        self.clear_layout(self.COLUMN_LAYOUT)

        min_temp = -5
        temp_range = 30
        max_height = 95
        
        if not self.interpolated_data:
            return

        for item in self.interpolated_data:
            # --- 1. Контейнер для Иконки ---
            icon_container = widget.QFrame()
            icon_container.setFixedHeight(24)
            icon_container.setSizePolicy(widget.QSizePolicy.Policy.Expanding, widget.QSizePolicy.Policy.Fixed)
            
            icon_box = widget.QHBoxLayout(icon_container)
            icon_box.setContentsMargins(0, 0, 0, 0)
            icon_box.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
            
            if item["is_main"] and item["icon"]:
                icon_label = widget.QLabel()
                pix = gui.QPixmap(f"media/right_frame/weather_icons_white/{item['icon']}.svg")
                if not pix.isNull():
                    icon_label.setPixmap(pix.scaled(16, 16, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
                icon_box.addWidget(icon_label)
                    
            self.ICON_BARS_LAYOUT.addWidget(icon_container, stretch=1)

            # --- 2. Контейнер для Столбика ---
            col_container = widget.QFrame()
            col_container.setFixedHeight(max_height)
            col_container.setSizePolicy(widget.QSizePolicy.Policy.Expanding, widget.QSizePolicy.Policy.Fixed)
            
            col_box = widget.QVBoxLayout(col_container)
            col_box.setContentsMargins(0, 0, 0, 0) 
            
            column = widget.QFrame()
            calc_h = int(((item["temp"] - min_temp) / temp_range) * max_height)
            
            column.setFixedHeight(max(1, calc_h))
            column.setFixedWidth(10)
            
            column.setStyleSheet("""
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 223, 86, 1), stop:1 rgba(135, 206, 250, 1));
                border-radius: 2px;
            """)
            
            col_box.addWidget(column, alignment=core.Qt.AlignmentFlag.AlignBottom | core.Qt.AlignmentFlag.AlignHCenter)
            self.COLUMN_LAYOUT.addWidget(col_container, stretch=1)
        
        self.update()
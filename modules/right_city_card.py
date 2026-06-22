import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtSvgWidgets import QSvgWidget
from .api_request import api_request, API_KEY, LANG, display_name_for_any
import PyQt6.QtGui as gui
from .read_write_json import read_json
from .translations import t
from .icon_finder import get_icon_path, svg_to_pixmap


class RightCityCard(widget.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.WIDTH = 390
        self.HEIGHT = 303
        self.setMinimumSize(core.QSize(self.WIDTH, self.HEIGHT))
        self.setStyleSheet("""
            RightCityCard {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 10px;
            }
        """)

        
        self._current_city = None

        self.LAYOUT = widget.QVBoxLayout(self)
        self.LAYOUT.setContentsMargins(16, 16, 16, 16)
        self.LAYOUT.setSpacing(16)

        self.TOP_SECTION = widget.QWidget()
        self.TOP_SECTION_LAYOUT = widget.QVBoxLayout(self.TOP_SECTION)
        self.TOP_SECTION_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TOP_SECTION_LAYOUT.setSpacing(8)


        self.ICON_TEXT_CONTAINER = widget.QWidget()
        self.ICON_TEXT_LAYOUT = widget.QHBoxLayout(self.ICON_TEXT_CONTAINER)
        self.ICON_TEXT_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.ICON_TEXT_LAYOUT.setSpacing(8)


        self.TOP_FRAME_ICON = QSvgWidget("media/city_card/navigation.svg")
        self.TOP_FRAME_ICON.setFixedSize(16, 16)

        self.TOP_TEXT = widget.QLabel(t("current_position"))
        self.TOP_TEXT.setStyleSheet("color: white; font-size: 16px; font-family: 'Roboto'; font-weight: 500;")

        self.ICON_TEXT_LAYOUT.addWidget(self.TOP_FRAME_ICON)
        self.ICON_TEXT_LAYOUT.addWidget(self.TOP_TEXT)
        self.ICON_TEXT_LAYOUT.addStretch()


        self.LINE = widget.QFrame()
        self.LINE.setFixedHeight(1)
        self.LINE.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")


        self.TOP_SECTION_LAYOUT.addWidget(self.ICON_TEXT_CONTAINER)
        self.TOP_SECTION_LAYOUT.addWidget(self.LINE)


        self.LAYOUT.addWidget(self.TOP_SECTION)


        self.LAYOUT.addStretch()
        self.CITY_LABEL = widget.QLabel("")
        self.CITY_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.LAYOUT.addWidget(self.CITY_LABEL)


        self.WEATHER_ICON = widget.QLabel(self)  # parent = сама карточка
        self.WEATHER_ICON.setAttribute(core.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.WEATHER_ICON.setStyleSheet("background: none;")

        self.DEGREE_FRAME = widget.QFrame()
        self.DEGREE_LAYOUT = widget.QHBoxLayout(self.DEGREE_FRAME)
        self.DEGREE_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.ICON_SPACER = widget.QLabel()
        self.ICON_SPACER.setStyleSheet("background: none;")

        self.DEGREE = widget.QLabel("")

        self.DEGREE_LAYOUT.addWidget(self.ICON_SPACER)
        self.DEGREE_LAYOUT.addWidget(self.DEGREE)

        self.LAYOUT.addWidget(self.DEGREE_FRAME)
        self.STAT_LABEL = widget.QLabel("")
        self.STAT_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.LAYOUT.addWidget(self.STAT_LABEL)

        self.MINMAX_LABEL = widget.QLabel()
        self.MINMAX_LABEL.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.LAYOUT.addWidget(self.MINMAX_LABEL)


        self.LAYOUT.addStretch()

        
        LANG.subscribe(self.retranslate_ui)

    def _load_svg_as_pixmap(self, path: str, size: int) -> gui.QPixmap:
        return svg_to_pixmap(path, size)
    
    def update_city_data(self, city_name):
        self._current_city = city_name
        city_request = api_request(city=city_name, API_KEY=API_KEY)

        temp = str(round(city_request["main"]["temp"]))
        temp_max = str(city_request["main"]["temp_max"])
        temp_min = str(city_request["main"]["temp_min"])
        description: str = city_request["weather"][0]["description"]
        icon_code = city_request["weather"][0]["icon"]

        self._icon_path = get_icon_path(icon_code)  # сохраняем путь

        self.CITY_LABEL.setText(display_name_for_any(city_name).capitalize())
        self.DEGREE.setText(temp + "°")
        self.STAT_LABEL.setText(description.capitalize())
        self.MINMAX_LABEL.setText(t("max_min").format(max=temp_max, min=temp_min))
        self.change_size()

    def retranslate_ui(self):
        
        self.TOP_TEXT.setText(t("current_position"))
        if self._current_city:
            self.update_city_data(self._current_city)

    def closeEvent(self, event):
        LANG.unsubscribe(self.retranslate_ui)
        super().closeEvent(event)

    def change_size(self):
        settings = read_json("settings.json")
        icon_path = getattr(self, "_icon_path", "media/right_frame/weather_icons/01d.svg")

        size_map = {
            ("1200", "800"):   (44,  74,  24, 16, 130),
            ("1440", "1024"):  (60,  85,  34, 25, 210),
            ("1512", "982"):   (60,  85,  34, 25, 190),
            ("1728", "1117"):  (70,  95,  40, 30, 240),
        }
        res = tuple(settings.get("currentResolution", ["1200", "800"]))
        city_fs, deg_fs, stat_fs, minmax_fs, icon_size = size_map.get(res, (44, 74, 24, 16, 130))

        self.CITY_LABEL.setStyleSheet(
            f"font-size: {city_fs}px; font-weight: bold; font-family: 'Roboto'; color: white; background: none;"
        )
        self.DEGREE.setStyleSheet(
            f"font-size: {deg_fs}px; color: white; font-family: 'Roboto'; font-weight: 500; background: none;"
        )
        self.STAT_LABEL.setStyleSheet(
            f"font-size: {stat_fs}px; font-weight: 500; color: white; font-family: 'Roboto'; background: none;"
        )
        self.MINMAX_LABEL.setStyleSheet(
            f"font-size: {minmax_fs}px; color: white; font-weight: 500; font-family: 'Roboto'; background: none"
        )

        pixmap = self._load_svg_as_pixmap(icon_path, icon_size)
        self.WEATHER_ICON.setPixmap(pixmap)
        self.WEATHER_ICON.setFixedSize(pixmap.size())
        self.ICON_SPACER.setFixedSize(pixmap.size())
        self.WEATHER_ICON.raise_()

        core.QTimer.singleShot(0, self._reposition_icon)
        core.QTimer.singleShot(0, self.WEATHER_ICON.raise_)

    def _reposition_icon(self):
        frame_pos = self.DEGREE_FRAME.mapTo(self, core.QPoint(0, 0))
        frame_h = self.DEGREE_FRAME.height()
        icon_h = self.WEATHER_ICON.height()
        icon_w = self.WEATHER_ICON.width()
        spacer_pos = self.ICON_SPACER.mapTo(self, core.QPoint(0, 0))
        x = spacer_pos.x()
        y = frame_pos.y() + (frame_h - icon_h) // 2
        self.WEATHER_ICON.move(x, y)
        
    def refresh_icon(self):
        if not hasattr(self, "_icon_path") or not self._current_city:
            return
        from .icon_finder import get_icon_path
        import os
        icon_code = os.path.splitext(os.path.basename(self._icon_path))[0]
        self._icon_path = get_icon_path(icon_code)
        self.change_size()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "WEATHER_ICON") and hasattr(self, "ICON_SPACER"):
            self._reposition_icon()
            self.WEATHER_ICON.raise_()
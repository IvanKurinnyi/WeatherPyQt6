import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .title_bar import TitleBar
from .app import app
from .city_card import Card
from .toggle_switch_button import ToggleSwitch
import os
from .right_city_card import RightCityCard


class MainWindow(widget.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Weather App")
        font_path = os.path.join(os.path.dirname(__file__), "..", "media", "fonts", "Roboto-VariableFont_wdth,wght.ttf")
        font_id = gui.QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("Шрифт не найден")
            font_family = "Arial"
        else:
            font_family = gui.QFontDatabase.applicationFontFamilies(font_id)[0]
            

        roboto_font = gui.QFont(font_family, 16, 900)

        self.WIDTH = 1200
        self.HEIGHT = 800
        self.X = (app.primaryScreen().size().width() - self.WIDTH) // 2
        self.Y = (app.primaryScreen().size().height() - self.HEIGHT) // 2
        self.setGeometry(self.X, self.Y, self.WIDTH, self.HEIGHT)

        self.CENTRAL_WIDGET = widget.QWidget()
        
        self.GRADIENT = gui.QLinearGradient(1200, 0, 0, 800)
        self.GRADIENT.setColorAt(0.0, gui.QColor("#FFDF56"))
        self.GRADIENT.setColorAt(1.0, gui.QColor("#87CEFA"))
        
        self.PALETTE = gui.QPalette()
        self.PALETTE.setBrush(gui.QPalette.ColorRole.Window, gui.QBrush(self.GRADIENT))
        self.CENTRAL_WIDGET.setPalette(self.PALETTE)
        self.CENTRAL_WIDGET.setAutoFillBackground(True)

        self.setCentralWidget(self.CENTRAL_WIDGET)
        
        self.LAYOUT = widget.QVBoxLayout(self.CENTRAL_WIDGET)
        self.LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.LAYOUT.setSpacing(0)
        self.CENTRAL_WIDGET.setLayout(self.LAYOUT)

        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        
        self.CENTRAL_FRAME = widget.QFrame(self.CENTRAL_WIDGET)
        self.LAYOUT.addWidget(self.CENTRAL_FRAME)
        
        # TitleBar добавляем после всех элементов, чтобы он был сверху
        self.TITLE_BAR = TitleBar(self)
        self.TITLE_BAR.setGeometry(0, 0, self.WIDTH, 20)
        self.TITLE_BAR.raise_()  # Поверх других элементов

        self.CENTRAL_LAYOUT = widget.QHBoxLayout(self.CENTRAL_FRAME)
        self.CENTRAL_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CENTRAL_FRAME.setLayout(self.CENTRAL_LAYOUT)

        



        self.LEFT_FRAME = widget.QFrame(self.CENTRAL_FRAME)
        self.LEFT_FRAME.setStyleSheet("background-color: rgba(0,0,0,0.4)")
        self.LEFT_LAYOUT = widget.QVBoxLayout(self.LEFT_FRAME)
        self.LEFT_LAYOUT.setContentsMargins(20, 20, 20, 20)
        self.LEFT_LAYOUT.setSpacing(20)
        self.LEFT_FRAME.setLayout(self.LEFT_LAYOUT)


        self.RIGHT_FRAME = widget.QFrame(self.CENTRAL_FRAME)
        self.RIGHT_LAYOUT = widget.QVBoxLayout(self.RIGHT_FRAME)
        self.RIGHT_FRAME.setLayout(self.RIGHT_LAYOUT)
        self.RIGHT_LAYOUT.setContentsMargins(0,0,0,0)

        self.CENTRAL_LAYOUT.addWidget(self.LEFT_FRAME)
        self.CENTRAL_LAYOUT.addWidget(self.RIGHT_FRAME, stretch=1)


        self.TOGGLE_SWITCH = ToggleSwitch(self.LEFT_FRAME)
        self.LEFT_LAYOUT.addWidget(self.TOGGLE_SWITCH, alignment=core.Qt.AlignmentFlag.AlignRight)

        self.NAVIGATION_FRAME = widget.QFrame(self.RIGHT_FRAME)
        self.NAVIGATION_FRAME.setFixedSize(core.QSize(788, 36))
        self.RIGHT_LAYOUT.addWidget(self.NAVIGATION_FRAME, alignment=core.Qt.AlignmentFlag.AlignCenter)
        self.NAVIGATION_FRAME.setStyleSheet("background-color:white")

        self.NAVIGATION_LAYOUT = widget.QHBoxLayout(self.NAVIGATION_FRAME)
        self.NAVIGATION_FRAME.setLayout(self.NAVIGATION_LAYOUT)
        self.NAVIGATION_LAYOUT.setContentsMargins(20,20,20,20)
        
        self.SETTINGS_FRAME = widget.QFrame(self.NAVIGATION_FRAME)
        self.NAVIGATION_LAYOUT.addWidget(self.SETTINGS_FRAME)

        self.SEARCH_FRAME = widget.QFrame(self.NAVIGATION_FRAME)
        self.NAVIGATION_LAYOUT.addWidget(self.SEARCH_FRAME)
 


        self.RIGHT_CARDS_FRAME = widget.QFrame(self.RIGHT_FRAME)
        self.RIGHT_CARDS_FRAME.setFixedSize(core.QSize(788, 724)) 
        self.RIGHT_LAYOUT.addWidget(self.RIGHT_CARDS_FRAME, alignment=core.Qt.AlignmentFlag.AlignCenter)


        self.RIGHT_CARDS_LAYOUT = widget.QVBoxLayout(self.RIGHT_CARDS_FRAME)
        self.RIGHT_CARDS_FRAME.setLayout(self.RIGHT_CARDS_LAYOUT)
        self.RIGHT_CARDS_LAYOUT.setContentsMargins(0,0,0,47)
        self.RIGHT_CARDS_LAYOUT.setSpacing(10)


        self.RIGHT_INFO_FRAME = widget.QFrame(self.RIGHT_CARDS_FRAME)
        self.RIGHT_INFO_FRAME.setFixedSize(core.QSize(788, 303))
        self.RIGHT_CARDS_LAYOUT.addWidget(self.RIGHT_INFO_FRAME)


        self.RIGHT_INFO_LAYOUT = widget.QHBoxLayout(self.RIGHT_INFO_FRAME)
        self.RIGHT_INFO_LAYOUT.setContentsMargins(0,0,0,0)

        
        
        self.CITY_INFO_FRAME = RightCityCard(self.RIGHT_CARDS_FRAME)
        self.RIGHT_INFO_LAYOUT.addWidget(self.CITY_INFO_FRAME)

        self.CITY_TIME_FRAME = widget.QFrame(self.RIGHT_CARDS_FRAME)
        self.CITY_TIME_FRAME.setFixedSize(core.QSize(390, 303))
        self.CITY_TIME_FRAME.setStyleSheet("background-color: rgba(0,0,0,0.2); border: none; padding: 5px; border-radius: 5px")
        self.RIGHT_INFO_LAYOUT.addWidget(self.CITY_TIME_FRAME)

        
        self.FORECAST_TIME = widget.QFrame(self.RIGHT_CARDS_FRAME)
        self.RIGHT_CARDS_LAYOUT.addWidget(self.FORECAST_TIME)
        self.FORECAST_TIME.setFixedSize(core.QSize(788, 157))
        self.FORECAST_TIME.setStyleSheet("background-color: rgba(255,255,255,0.8); border: none; padding: 5px; border-radius: 5px")

        self.FORECAST_GRAPH = widget.QFrame(self.RIGHT_CARDS_FRAME)
        self.RIGHT_CARDS_LAYOUT.addWidget(self.FORECAST_GRAPH)
        self.FORECAST_GRAPH.setFixedSize(core.QSize(788, 197))
        self.FORECAST_GRAPH.setStyleSheet("background-color: rgba(255,255,255,0.8); border: none; padding: 5px; border-radius: 5px")
        


        self.SCROLL_AREA = widget.QScrollArea(parent=self)
        self.SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SCROLL_AREA.setStyleSheet("background-color: rgba(0,0,0,0); border: none")
        self.LEFT_LAYOUT.addWidget(self.SCROLL_AREA)
        self.SCROLL_AREA.setWidgetResizable(True)
        
        self.SCROLL_FRAME = widget.QFrame(parent=self.SCROLL_AREA)
        self.SCROLL_LAYOUT = widget.QVBoxLayout()
        self.SCROLL_LAYOUT.setSpacing(0)
        self.SCROLL_FRAME.setLayout(self.SCROLL_LAYOUT)
        self.SCROLL_AREA.setWidget(self.SCROLL_FRAME)
        
        self.cards = []
        self.selected_card = None

        city_list = ["Київ", "Дніпро", "New York", "Lviv", "Esslingen", "Bad Herrenalb", "Munich", "Bratislava", "Paris"]

        for city in city_list:
            card = Card(parent = self.SCROLL_FRAME, city_name=city)
            card.setFont(roboto_font)
            self.cards.append(card)
            card.selected.connect(lambda c=card: self._on_card_selected(c))
            self.SCROLL_LAYOUT.addWidget(card)
            self.BOTTOM_LINE = widget.QFrame(self.SCROLL_FRAME)
            self.BOTTOM_LINE.setFixedSize(core.QSize(314,1))
            self.BOTTOM_LINE.setStyleSheet("background-color: rgba(255,255,255,0.2)")
            self.SCROLL_LAYOUT.addWidget(self.BOTTOM_LINE, alignment=core.Qt.AlignmentFlag.AlignCenter)
        self.SCROLL_LAYOUT.addStretch(1)
        

    def _on_card_selected(self, card):
        """Обработчик выбора карточки - деселектирует предыдущую выбранную карточку"""
        if self.selected_card is not None and self.selected_card != card:
            self.selected_card.deselect()
        self.selected_card = card


window = MainWindow()
        
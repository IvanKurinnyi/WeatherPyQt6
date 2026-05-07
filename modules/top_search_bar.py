import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
from PyQt6.QtSvgWidgets import QSvgWidget
#from .api_request import api_request, API_KEY

class SearchBar(widget.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedSize(core.QSize(788, 36))
        self.setStyleSheet("background-color:white")
        
        self.LAYOUT = widget.QHBoxLayout(self)
        self.LAYOUT.setContentsMargins(16, 16, 16, 16)
        self.LAYOUT.setSpacing(8)
        
        self.SETTINGS = widget.QWidget()
        self.SETTINGS.setFixedSize(core.QSize(32,32))
        self.SETTINGS_LAYOUT = widget.QVBoxLayout(self.SETTINGS)
        self.SETTINGS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.SETTINGS_LAYOUT.setSpacing(0)

        self.SETTINGS_ICON = QSvgWidget("media/right_frame/settings.svg", self)
        self.SETTINGS_ICON.setFixedSize(core.QSize(16,16))
        self.SETTINGS_LAYOUT.addWidget(self.SETTINGS_ICON)
        


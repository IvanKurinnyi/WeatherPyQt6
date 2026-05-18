import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtSvgWidgets import QSvgWidget


class SearchBar(widget.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedSize(core.QSize(788, 36))
        self.setStyleSheet("background-color:none")
        
        self.LAYOUT = widget.QHBoxLayout(self)
        self.LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.LAYOUT.setSpacing(0)
        
        self.SETTINGS_FRAME = widget.QFrame(self)
        self.LAYOUT.addWidget(self.SETTINGS_FRAME)

        self.S_LAYOUT = widget.QHBoxLayout(self.SETTINGS_FRAME)
        self.S_LAYOUT.setContentsMargins(0, 0, 0, 0)
        
        self.SETTINGS = widget.QPushButton(self.SETTINGS_FRAME)
        self.SETTINGS.setFixedSize(core.QSize(32,32))
        self.SETTINGS.setStyleSheet("background-color: rgba(0,0,0,0.2)")
        self.SETTINGS_LAYOUT = widget.QVBoxLayout(self.SETTINGS)
        self.SETTINGS_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.SETTINGS_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.SETTINGS_LAYOUT.setSpacing(0)
        self.S_LAYOUT.addWidget(self.SETTINGS)


        self.SETTINGS_ICON = QSvgWidget("media/right_frame/settings.svg", self.SETTINGS)
        self.SETTINGS_ICON.setStyleSheet("background-color:none;")
        self.SETTINGS_ICON.setFixedSize(core.QSize(16,16))
        self.SETTINGS_LAYOUT.addWidget(self.SETTINGS_ICON)
        
        self.SETTINGS_LABEL = widget.QLabel("Налаштування",self.SETTINGS_FRAME)
        self.setStyleSheet("font-size:14px; font-weight:500;")
        self.S_LAYOUT.addWidget(self.SETTINGS_LABEL)



        self.SEARCH = widget.QFrame(self)
        self.SEARCH.setFixedSize(core.QSize(261,36))
        self.SEARCH.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 4px;")
        self.LAYOUT.addWidget(self.SEARCH, alignment=core.Qt.AlignmentFlag.AlignRight)
        
        self.SEARCH_LAYOUT = widget.QHBoxLayout(self.SEARCH)
        self.SEARCH_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)


        self.IMG = widget.QLabel(self.SEARCH)
        self.IMG.setFixedSize(core.QSize(22,22))
        self.IMG.setStyleSheet("background-color: none; margin-top: -3px;")
        self.PIXMAP = gui.QPixmap("media/right_frame/Search.svg")
        self.IMG.setPixmap(self.PIXMAP)
        self.SEARCH_LAYOUT.addWidget(self.IMG)
        
        self.SEARCH_LINE = widget.QLineEdit(self.SEARCH)
        self.SEARCH_LINE.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
            }
        """)
        self.SEARCH_LINE.setPlaceholderText("Пошук")
        self.SEARCH_LAYOUT.addWidget(self.SEARCH_LINE)

        self.POPUP = widget.QFrame()
        self.POPUP.setWindowFlags(
            core.Qt.WindowType.Tool | 
            core.Qt.WindowType.CustomizeWindowHint | 
            core.Qt.WindowType.FramelessWindowHint |
            core.Qt.WindowType.WindowStaysOnTopHint |
            core.Qt.WindowType.WindowDoesNotAcceptFocus)
        self.POPUP.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.POPUP.setStyleSheet("background-color:rgba(0,0,0,0.2);border-radius: 10px; border: none;") 
        self.POPUP.setMinimumWidth(261)
        
        
        self.POPUP_LAYOUT = widget.QVBoxLayout(self.POPUP)
        self.RESULTS = widget.QLabel("Результати пошуку", self.POPUP)
        self.POPUP_LAYOUT.addWidget(self.RESULTS)
        self.POPUP.hide()

        self.SEARCH_LINE.textChanged.connect(self.on_text_changed)
        widget.QApplication.instance().installEventFilter(self)

    def on_text_changed(self, text):
        if text.strip(): 
            if not self.POPUP.isVisible():
                self.POPUP.show()
                pos = self.SEARCH.mapToGlobal(core.QPoint(0, self.SEARCH.height()))
                self.POPUP.move(pos)
    
        else:              
            self.POPUP.hide()
            
    def eventFilter(self, obj, event):
        if event.type() == core.QEvent.Type.MouseButtonPress:
            if self.POPUP.isVisible():
                global_pos = event.globalPosition().toPoint()
                
                if not self.SEARCH.geometry().contains(self.SEARCH.mapFromGlobal(global_pos)) and \
                   not self.POPUP.geometry().contains(self.POPUP.mapFromGlobal(global_pos)):
                    
                    self.POPUP.hide()
                    
        return super().eventFilter(obj, event)
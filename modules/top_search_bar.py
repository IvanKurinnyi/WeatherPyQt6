import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtSvgWidgets import QSvgWidget
from .find_town import find_cities_by_prefix
from .read_write_json import create_json, read_json

class SearchBar(widget.QFrame):
    city_selected = core.pyqtSignal(str)
    city_added = core.pyqtSignal(str)
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.CITIES_DATA = read_json("cities.json").get("data", [])
        self.CITY_NAMES = [city_obj.get('city', '').lower() for city_obj in self.CITIES_DATA]
        self.DYNAMIC_LABELS = []

        self.setFixedSize(core.QSize(788, 36))
        self.setStyleSheet("background-color:none")
        
        self.LAYOUT = widget.QHBoxLayout(self)
        self.LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.LAYOUT.setSpacing(10)
        
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
        self.SETTINGS_LABEL.setStyleSheet("font-size:14px; font-weight:500;")
        self.S_LAYOUT.addWidget(self.SETTINGS_LABEL)

        self.LAYOUT.addStretch(1) 

       
        self.ADD_BUTTON = widget.QPushButton(self)    
        self.ADD_BUTTON.setFixedSize(core.QSize(97, 36))
        self.ADD_BUTTON.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
        self.ADD_LAYOUT = widget.QHBoxLayout(self.ADD_BUTTON)
        self.ADD_LAYOUT.setContentsMargins(10, 0, 10, 0)
        self.ADD_LAYOUT.setSpacing(6)
        self.ADD_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.ADD_ICON = QSvgWidget("media/search_bar/plus.svg", self.ADD_BUTTON)
        self.ADD_ICON.setFixedSize(core.QSize(16, 16))
        
        self.ADD_TEXT = widget.QLabel("Додати", self.ADD_BUTTON)
        self.ADD_TEXT.setStyleSheet("color: white; font-size: 14px; font-weight: 500; background: none;")
        
        self.ADD_LAYOUT.addWidget(self.ADD_ICON)
        self.ADD_LAYOUT.addWidget(self.ADD_TEXT)
        self.LAYOUT.addWidget(self.ADD_BUTTON)
        self.ADD_BUTTON.hide()
        self.ADD_BUTTON.clicked.connect(self.add_city)
       

        self.SEARCH = widget.QFrame(self)
        self.SEARCH.setFixedSize(core.QSize(261,36))
        self.SEARCH.setStyleSheet("background-color: rgba(0,0,0,0.2); border-radius: 4px;")
        self.LAYOUT.addWidget(self.SEARCH)
        
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

        self.CLEAR = widget.QPushButton(self.SEARCH)
        self.CLEAR.setFixedSize(core.QSize(22,22))
        self.CLEAR.setStyleSheet("""
            QPushButton {
                background-color: none; 
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 3px;
            }
        """)
        self.CLEAR.setIcon(gui.QIcon("media/search_bar/Clear.svg"))
        self.CLEAR.setIconSize(core.QSize(22, 22))
        self.SEARCH_LAYOUT.addWidget(self.CLEAR, alignment=core.Qt.AlignmentFlag.AlignRight)
        self.CLEAR.hide()
        self.CLEAR.clicked.connect(self.clear_search_line)

        self.POPUP = widget.QWidget(self) 
        self.POPUP.setObjectName("PopupMain")
        
        self.POPUP.setWindowFlags(
            core.Qt.WindowType.Window | 
            core.Qt.WindowType.FramelessWindowHint |
            core.Qt.WindowType.WindowStaysOnTopHint |
            core.Qt.WindowType.WindowDoesNotAcceptFocus |
            core.Qt.WindowType.NoDropShadowWindowHint
        )
        self.POPUP.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.POPUP.setStyleSheet("""
            #PopupMain { 
                background: transparent; 
                border: none; 
            }
        """)
        self.POPUP.setMinimumWidth(261)
        
        self.POPUP_MAIN_LAYOUT = widget.QVBoxLayout(self.POPUP)
        self.POPUP_MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)

        self.POPUP_FRAME = widget.QFrame(self.POPUP)
        self.POPUP_FRAME.setObjectName("PopupFrame")
        self.POPUP_FRAME.setFrameShape(widget.QFrame.Shape.NoFrame)
        
        self.POPUP_FRAME.setStyleSheet("""
            #PopupFrame {
                background-color: rgba(0, 0, 0, 0.2); 
                border-radius: 10px; 
                border: none; 
            }
        """)
        self.POPUP_FRAME.setMinimumWidth(261)

        self.POPUP_MAIN_LAYOUT.addWidget(self.POPUP_FRAME)

        self.POPUP_LAYOUT = widget.QVBoxLayout(self.POPUP_FRAME)
        self.POPUP_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        self.RESULTS = widget.QLabel("Результати пошуку", self.POPUP_FRAME)
        self.RESULTS.setStyleSheet("background-color: none; color: white; padding-left: 5px; border: none;")
        self.POPUP_LAYOUT.addWidget(self.RESULTS)
        self.POPUP.hide()
        
        self.SEARCH_LINE.textChanged.connect(self.on_text_changed)
        widget.QApplication.instance().installEventFilter(self)
        
    def clear_old_results(self):
        for lbl in self.DYNAMIC_LABELS:
            lbl.hide()
            self.POPUP_LAYOUT.removeWidget(lbl)
            lbl.deleteLater()
        self.DYNAMIC_LABELS.clear()

        
        while self.POPUP_LAYOUT.count() > 1: 
            item = self.POPUP_LAYOUT.takeAt(1)
            if item.widget():
                item.widget().hide() 
                item.widget().deleteLater()

    def on_text_changed(self, text):
        self.clear_old_results()
        
        if text.strip():
            # Show clear button when there's text
            self.CLEAR.show()
            
            # Check if text exists in cities.json
            text_lower = text.strip().lower()
            city_exists = text_lower in self.CITY_NAMES
            
            # Show "Додати" button only if city exists in the database
            if city_exists:
                self.ADD_BUTTON.show()
            else:
                self.ADD_BUTTON.hide()
            
            # Show search results
            found_cities = find_cities_by_prefix(self.CITIES_DATA, text, limit=5)
            
            if found_cities:
                for city in found_cities:
                    btn = widget.QPushButton(city, self.POPUP_FRAME)
                    btn.setFixedHeight(36)
                    btn.setStyleSheet("""
                        QPushButton {
                            text-align: left; 
                            background-color: transparent; 
                            color: white; 
                            padding: 6px 10px;
                            border: none;
                            font-size: 14px;
                        }
                        QPushButton:hover {
                            background-color: rgba(255, 255, 255, 0.2);
                            border-radius: 4px;
                        }
                    """)
                    btn.clicked.connect(lambda checked, c=city: self._on_city_clicked(c))
                    
                    self.POPUP_LAYOUT.addWidget(btn)
                    self.DYNAMIC_LABELS.append(btn)

                if not self.POPUP.isVisible():
                    self.POPUP.show()
                
                self.POPUP_LAYOUT.activate()
                
                self.POPUP.resize(1, 1) 
                self.POPUP.adjustSize()
                
                pos = self.SEARCH.mapToGlobal(core.QPoint(0, self.SEARCH.height()))
                self.POPUP.move(pos)
        else:
            # Hide buttons when text is empty
            self.CLEAR.hide()
            self.ADD_BUTTON.hide()
            
    def _on_city_clicked(self, city_name):
        self.SEARCH_LINE.blockSignals(True)
        self.SEARCH_LINE.setText(city_name)
        self.SEARCH_LINE.blockSignals(False)
        self.CLEAR.show()
        self.ADD_BUTTON.show()
        
        self.POPUP.hide()       
        self.city_selected.emit(city_name)
            
    def eventFilter(self, obj, event):
        if event.type() == core.QEvent.Type.MouseButtonPress:
            if self.POPUP.isVisible():
                global_pos = event.globalPosition().toPoint()
                
                if not self.SEARCH.geometry().contains(self.SEARCH.mapFromGlobal(global_pos)) and \
                   not self.POPUP.geometry().contains(self.POPUP.mapFromGlobal(global_pos)):
                    
                    self.POPUP.hide()
                    
        return super().eventFilter(obj, event)

    def clear_search_line(self):
        """Clear the search line and hide buttons"""
        self.SEARCH_LINE.blockSignals(True)
        self.SEARCH_LINE.setText("")
        self.SEARCH_LINE.blockSignals(False)
        self.CLEAR.hide()
        self.ADD_BUTTON.hide()
        self.POPUP.hide()

    def add_city(self):
        """Add the city from search line to city.json and update cards"""
        city_name = self.SEARCH_LINE.text().strip()
        
        if not city_name:
            return
        
        # Read current cities from city.json
        try:
            cities = read_json("city.json")
        except:
            cities = []
        
        # Check if city already exists
        if any(c.lower() == city_name.lower() for c in cities):
            return
        
        # Add new city
        cities.append(city_name)
        
        # Write back to city.json
        create_json(cities, "city.json")
        
        # Clear the search line
        self.clear_search_line()
        
        # Emit signal to update cards
        self.city_added.emit(city_name)
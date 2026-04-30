import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from .title_bar_button import Button

class TitleBar(widget.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.WIDTH = 1200
        self.HEIGHT = 25
        self.setFixedSize(core.QSize(self.WIDTH,self.HEIGHT))
        self.setStyleSheet(f"background-color: rgba(0,0,0,0)")
        self.POSITION = self.pos()

        self.TITLE_LAYOUT = widget.QVBoxLayout()
        self.TITLE_LAYOUT.setContentsMargins(0,0,0,0)
        self.setLayout(self.TITLE_LAYOUT)
        

        self.BUTTON_FRAME = widget.QFrame(self)
        self.TITLE_LAYOUT.addWidget(self.BUTTON_FRAME)
        self.BUTTON_FRAME.setFixedSize(core.QSize(70, 20))
        self.BUTTON_LAYOUT = widget.QHBoxLayout()
        self.BUTTON_LAYOUT.setSpacing(5)
        self.BUTTON_FRAME.setLayout(self.BUTTON_LAYOUT)
        self.BUTTON_LAYOUT.setContentsMargins(5, 0, 0, 0)
        self.BUTTON_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.EXIT = Button(self.BUTTON_FRAME,"media/title_bar/Close_Button.svg","media/title_bar/Close_Button_Hover.svg")
        self.MIN = Button(self.BUTTON_FRAME,"media/title_bar/Minimize_Button.svg","media/title_bar/Minimize_Button_Hover.svg")
        self.MAX = Button(self.BUTTON_FRAME,"media/title_bar/Maximize_Button.svg","media/title_bar/Maximize_Button_Hover.svg")
        
        self.EXIT.setStyleSheet("border:none")
        self.MIN.setStyleSheet("border:none")  
        self.MAX.setStyleSheet("border:none")  

        self.BUTTON_LAYOUT.addWidget(self.EXIT)
        self.BUTTON_LAYOUT.addWidget(self.MIN)
        self.BUTTON_LAYOUT.addWidget(self.MAX)

        self.EXIT.clicked.connect(self.handleClose)
        self.MIN.clicked.connect(self.handleMinimize)
        self.MAX.clicked.connect(self.handleMaximize)



    def handleClose(self):
        self.window().close()
    def handleMinimize(self):
        self.window().showMinimized()
    def handleMaximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()
    
    def mouseMoveEvent(self, event:gui.QMouseEvent):
        mouse_pos = event.position().toPoint() - self.POSITION
        self.window().move(
            self.window().x() + mouse_pos.x() ,
            self.window().y() + mouse_pos.y()
        )
            
    def mousePressEvent(self, event:gui.QMouseEvent):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.POSITION = event.position().toPoint()

          
          
          
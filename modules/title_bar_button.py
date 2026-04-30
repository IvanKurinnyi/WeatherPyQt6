import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui




class Button(widget.QPushButton):
    def __init__(self, frame, icon_path, hover_icon_path,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ICON = gui.QIcon(icon_path)
        self.HOVER_ICON = gui.QIcon(hover_icon_path)
        self.setIcon(self.ICON)  

    def enterEvent(self, event):
        self.setIcon(self.HOVER_ICON)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIcon(self.ICON)
        super().leaveEvent(event)    


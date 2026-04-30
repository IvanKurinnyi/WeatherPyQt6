import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui

class ToggleSwitch(widget.QFrame):
    TOGGLED = core.pyqtSignal(bool)
    #это сигнал для других частей приложения
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.IS_CHECKED = False
        self.WIDTH = 52
        self.HEIGHT = 24
        self.setFixedSize(core.QSize(self.WIDTH,self.HEIGHT))
        self.setStyleSheet("""
            background-color: rgba(0,0,0,0.2); 
            border-radius: 12px;
        """)



        self.setCursor(core.Qt.CursorShape.PointingHandCursor)

        self.ICON_ON = gui.QPixmap("media/night_switch.svg")
        self.ICON_OFF = gui.QPixmap("media/day_switch.svg")
        
        self.ICON_LABEL = widget.QLabel(self)
        self.ICON_LABEL.setPixmap(self.ICON_OFF)
        self.ICON_LABEL.setFixedSize(core.QSize(18,18))
        self.ICON_LABEL.move(2,3)
        self.ICON_LABEL.setStyleSheet("background: transparent")

        self.ANIMATION = core.QPropertyAnimation(self.ICON_LABEL, b"pos")
        self.ANIMATION.setDuration(250)  # Длительность в миллисекундах (0.25 сек)
        # Тип кривой: OutCubic дает плавное замедление в конце
        self.ANIMATION.setEasingCurve(core.QEasingCurve.Type.OutCubic)

    def mousePressEvent(self, event):
        self.IS_CHECKED = not self.IS_CHECKED
        #переключение состояния с помощью .эмит
        self.update_icon()
        self.TOGGLED.emit(self.IS_CHECKED)
        #посылает сигнал с текущим состоянем(self.IS_CHECKED) другим виджетам(чтоб менять тему)

    def update_icon(self):
        if self.IS_CHECKED:
            self.ICON_LABEL.setPixmap(self.ICON_ON)
            self.ICON_LABEL.move(self.WIDTH - 20, 3)
            self.setStyleSheet("background-color:white;border-radius: 12px;")
            self.ANIMATION.setStartValue(core.QPoint(2,3))
            self.ANIMATION.setEndValue(core.QPoint(self.WIDTH - 20, 3))
            self.ANIMATION.start()
        else:
            self.ICON_LABEL.setPixmap(self.ICON_OFF)
            self.ICON_LABEL.move(2, 3)
            self.setStyleSheet("background-color:rgba(0,0,0,0.2);border-radius: 12px;")
            self.ANIMATION.setStartValue(core.QPoint(self.WIDTH - 20, 3))
            self.ANIMATION.setEndValue(core.QPoint(2,3))
            self.ANIMATION.start()


        
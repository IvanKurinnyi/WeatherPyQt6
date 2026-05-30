import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core
import PyQt6.QtGui as gui

class ComboBox(widget.QComboBox):
    def __init__(self,layout,items:list,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
        QComboBox {
            background-color: white;
            color: black;
            border: none;
            border-radius: 4px;
            padding-left: 6px;
        }

        QComboBox::drop-down {
            border: none;
            background: transparent;
            width: 20px;
        }
                           
        QComboBox::down-arrow {
            image:url(media/search_bar/combobox_arrow.svg);
            width: 16px;
            height: 16px;
        }

        QComboBox QAbstractItemView {
            background-color: white;
            color: black;
            border: none;
            selection-background-color: lightgray;
        }
        """)
        self.setFixedSize(core.QSize(239, 32))
        self.addItems(items)
        
        layout.addWidget(self, alignment=core.Qt.AlignmentFlag.AlignLeft)
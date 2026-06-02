import sys
import PyQt6.QtWidgets as widget
import PyQt6.QtCore as core

widget.QApplication.setAttribute(core.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
app = widget.QApplication(sys.argv)
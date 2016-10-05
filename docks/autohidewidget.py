from PyQt5.QtWidgets import *

class AutohideWidget(QWidget):
    def __init__(self, parent=None):
        super(AutohideWidget, self).__init__(parent)
        # how many pixels the widget lurks into the view while scrolled out
        self.OutOffset = 14

    def paintEvent(self, e):
        QWidget.paintEvent(e)
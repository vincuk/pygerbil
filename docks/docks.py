from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.uic

from autohideview import *
from autohidewidget import *
import gerbil_rc

class BandDock(QDockWidget):
    def __init__(self, parent):
        super(BandDock, self).__init__(parent)

class FalseColorDock(QDockWidget):
    def __init__(self, parent=None):
        super(FalseColorDock, self).__init__(parent)
        contents = QWidget(self)
        self.layout = QVBoxLayout(contents)
        view = AutohideView(contents)
        view.setBaseSize(QSize(50, 300))
        view.setFrameShape(QFrame.NoFrame)
        view.setVerticalScrollBarPolicy(1)
        view.setHorizontalScrollBarPolicy(1)

        self.layout.addWidget(view)
        self.setWidget(contents)

        self.scene = ScaledView()
        view.setScene(self.scene)

        # initialize selection widget
        # sel = AutohideWidget()
        # uisel = PyQt5.uic.loadUi('falsecolordock_sel.ui')
        # # uisel.setupUi(sel)
        # scene.offTop = sel.OutOffset
        # view.addWidget(sel)

    def Update(self, filename):
        self.scene.DrawScene(filename)

class ScaledView(QGraphicsScene):
    def __init__(self, parent=None):
        super(ScaledView, self).__init__(parent)
        self.scaler = QTransform()

    def DrawScene(self, filename):
        self.addPixmap(QPixmap(filename))

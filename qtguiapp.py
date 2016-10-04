import sys

import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.uic

from docks.docks import *
from distviewgui import *

import docks.gerbil_rc

class GUIApp(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)

        mainwin = MyMainWindow()
        mainwin.show()
        self.exec_()

class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        # self.main_widget = QWidget(self)
        self.mainwindow = PyQt5.uic.loadUi('mainwindow.ui')

        self.fm = FalseColorModel()
        # initFalseColor()

        self.falseColorDock = FalseColorDock(self)
        self.bandDock = PyQt5.uic.loadUi('docks/banddock.ui')
        self.illumDock = PyQt5.uic.loadUi('docks/illumdock.ui')
        self.normDock = PyQt5.uic.loadUi('docks/normdock.ui')
        self.distView = DistView(self)
        self.distView.setActive()

        pos = self.mainwindow.distviewLayout.count() - 1
        self.mainwindow.distviewLayout.insertWidget(pos, self.distView.gv, 1)

        # pos = self.mainwindow.distviewLayout.count() - 1
        # self.mainwindow.distviewLayout.insertWidget(pos, self.bandDock, 1)

        # pos = self.mainwindow.distviewLayout.count() - 1
        # self.mainwindow.distviewLayout.insertWidget(pos, self.falseColorDock, 1)

        self.mainwindow.addDockWidget(Qt.RightDockWidgetArea, self.bandDock)
        self.mainwindow.addDockWidget(Qt.RightDockWidgetArea, self.illumDock)
        self.mainwindow.addDockWidget(Qt.RightDockWidgetArea, self.normDock)
        self.mainwindow.addDockWidget(Qt.RightDockWidgetArea, self.falseColorDock)
        self.mainwindow.tabifyDockWidget(self.illumDock, self.normDock)


        # self.mainwindow = QVBoxLayout(self.main_widget)
        # self.mainwindow.sizeConstraint = QLayout.SetDefaultConstraint
        # self.mainwindow.setLayout(self.main_layout)

        self.setCentralWidget(self.mainwindow)


class FalseColorModel():
    def __init__(self):
        self.type = "FalseColoring"


if __name__ == "__main__":
    app = GUIApp(sys.argv)
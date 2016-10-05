from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *

class AutohideView(QGraphicsView):
    def __init__(self, parent=None):
        super(AutohideView, self).__init__(parent)
        format = QGLFormat()
        format.setDepth(False)
        format.setSampleBuffers(False)
        self.target = QGLWidget(format)

        self.target.setMouseTracking(True)
        #
        self.setViewport(self.target)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

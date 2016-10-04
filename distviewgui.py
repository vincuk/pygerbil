from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.uic
from docks.autohideview import *
from docks.autohidewidget import *
import docks.gerbil_rc

DistViewGUI, DistViewBase = PyQt5.uic.loadUiType('docks/distviewgui.ui')

# ViewportControlUI, ViewportControlBase = PyQt5.uic.loadUiType('docks/viewportcontrol.ui')
#
# class ViewportControl(ViewportControlBase, ViewportControlUI):
#     def __init__(self, parent=None):
#         ViewportControlBase.__init__(self, parent)
#         self.setupUi(parent)

class DistView(DistViewBase, DistViewGUI):
    def __init__(self, parent):
        DistViewBase.__init__(self, parent)
        self.frame = QWidget()
        self.setupUi(self.frame)
        self.vp = Viewport(self.gv.target)
        self.gv.setScene(self.vp)

        # self.gv.render(self.vp.painter)

        # self.uivc = PyQt5.uic.loadUi('docks/viewportcontrol.ui')
        # p = QGraphicsScene().addWidget(self.uivc)
        # scene = QGraphicsScene()
        # scene.addWidget(self.uivc, Qt.Window)
        # self.gv.setScene(scene)

        #
        #
        # p.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        # self.layout = QVBoxLayout(self)
        # self.layout.addWidget(self.uivc)
        #
        #
        # self.setLayout(self.layout)

    def setActive(self):
        self.vp.active = True
        self.vp.update()

    def setInactive(self):
        self.vp.active = False
        self.vp.update()

    # def rebuild(self):
    #     self.vp.rebuild()

class Viewport(QGraphicsScene):
    def __init__(self, target, parent=None):
        super(Viewport, self).__init__(parent)
        self.active = True
        target.makeCurrent()
        self.painter = QPainter()

    def drawScene(self, painter):
        rect = QRect(0, 0, width, height)
        painter.save()
        self.drawAxesBg(painter)
        painter.restore()

    def drawAxesBg(self, painter):
        #draw axes in background
        pen = QPen(QColor(64, 64, 64))
        pen.setWidth(0)
        painter.setPen(pen)

        # polygon describing illuminant
        poly = QPolygonF()
        dimensionality = 3
        for i in range(dimensionality):
            top = 5 #((*ctx)->nbins-1) * illuminantCurve.at(i);
            self.painter.drawLine(QPointF(i, 0.), QPointF(i, top))
            poly.append(QPointF(i, top))

        # poly << QPointF((*ctx)->dimensionality-1, (*ctx)->nbins-1);
        # poly << QPointF(0, (*ctx)->nbins-1);

	# // visualize illuminant
	# QPolygonF poly2 = modelview.map(poly);
	# poly2.translate(0., -5.);
	# painter->restore();
	# QBrush brush(QColor(32, 32, 32), Qt::Dense3Pattern);
	# painter->setBrush(brush);
	# painter->setPen(Qt::NoPen);
	# painter->drawPolygon(poly2);
	# painter->setPen(Qt::white);
	# poly2.remove((int)(*ctx)->dimensionality, 2);
	# painter->drawPolyline(poly2);
	# painter->save();
	# painter->setWorldTransform(modelview);

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
        self.setAutoFillBackground(True)


        self.vp = Viewport(self.frame)
        #
        #
        #
        # # scene = QGraphicsScene()
        # # scene.addText("GraphicsView rotated clockwise")
        #
        # self.gv.setScene(self.vp)



        # self.gv.render(self.vp.painter)



        # self.uivc = PyQt5.uic.loadUi('docks/viewportcontrol.ui')
        # p = QGraphicsScene().addWidget(self.uivc)
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


    # def rebuild(self):
    #     self.vp.rebuild()

class Viewport(QWidget):
    def __init__(self, parent=None):
        super(Viewport, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.active = True

    def setActive(self):
        self.active = True
        self.update()

    def setInactive(self):
        self.active = False
        self.update()

    def paintEvent(self, target):
        # target.makeCurrent()
        painter = QPainter(self)
        self.drawScene(painter)

    def drawScene(self, painter):
        withDynamics = False
        rect = QRect(0, 0, self.width(), self.height())

        #/* Hack: without dynamics, we typically also want a boring background */
        if withDynamics:
            painter.fillRect(rect, QColor(15, 7, 15))
    	else:
            painter.fillRect(rect, Qt.black)

        painter.setRenderHint(QPainter.Antialiasing)

        # if disabled:
		 #    drawWaitMessage(painter)
		 #    return False

        painter.save()
        # painter.setWorldTransform(modelview)
        self.drawAxesBg(painter)
        painter.restore()

        #/* determine if we draw the highlight part */
        # only draw when active and dynamic content is desired
        drawHighlight = self.active and withDynamics

        if withDynamics:
            self.drawLegend(painter) #, selection);
        else:
            self.drawLegend(painter)

    def drawLegend(self, painter):
        width, height = self.width(), self.height()
        painter.setPen(Qt.white)

        # drawing background for x-axis
        xbgrect = QRectF(0, height-35, width, 35)

        painter.save()
        painter.setBrush(QColor(0,0,0, 128))
        painter.fillRect(xbgrect, QBrush(QColor(0,0,0,128)))
        painter.restore()

     #    # x-axis
	#     for (size_t i = 0; i < (*ctx)->dimensionality; ++i) {
     #        QPointF l = modelview.map(QPointF(i - 1.f, 0.f));
	# 	    l.setY(height - 30);
    #
	# 	QPointF r = modelview.map(QPointF(i + 1.f, 0.f));
	# 	r.setY(height);
    #
	# 	QRectF rect(l, r);
    #
	# 	// only draw every xth label if we run out of space
	# 	int stepping = std::max<int>(1, 150 / rect.width());
    #
	# 	// only draw regular steppings and selected band
	# 	if (i % stepping && (int)i != sel)
	# 		continue;
    #
	# 	// also do not draw near selected band
	# 	if ((int)i != sel && sel > -1 && std::abs((int)i - sel) < stepping)
	# 		continue;
    #
	# 	rect.adjust(-50.f, 0.f, 50.f, 0.f);
    #
	# 	bool highlight = ((int)i == sel);
	# 	if (highlight)
	# 		painter->setPen(Qt::red);
	# 	painter->drawText(rect, Qt::AlignCenter, (*ctx)->xlabels[i]);
	# 	if (highlight)	// revert back color
	# 		painter->setPen(Qt::white);
	# }

        #drawing background for y-axis
        yaxisWidth = 0
        yaxis = ["12", "14", "16"]
        displayHeight = height

        ybgrect = QRectF(0, 0, yaxisWidth+25, height-35)
        painter.save()
        painter.setBrush(QColor(0,0,0, 128))
        painter.fillRect(ybgrect, QBrush(QColor(0,0,0,128)))
        painter.restore()

        #y-axis
        for i in range(len(yaxis)): # yaxis.size(); ++i):
            b = QPointF(0, (displayHeight)/(len(yaxis) - 1) * i + 12)

            t = b
            t += QPointF(0, 10)
            t.setX(0)
            b.setX(yaxisWidth+15)
            rect = QRectF(t, b)

            painter.drawText(rect, Qt.AlignVCenter | Qt.AlignRight, yaxis[i])


    def drawAxesBg(self, painter):
        #draw axes in background
        pen = QPen(QColor(64, 64, 64))
        pen.setWidth(0)
        painter.setPen(pen)

        # polygon describing illuminant
        poly = QPolygonF()
        dimensionality = 3
        for i in range(dimensionality):
            top = 500 #((*ctx)->nbins-1) * illuminantCurve.at(i);
            painter.drawLine(QPointF(i, 0.), QPointF(i, top))
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

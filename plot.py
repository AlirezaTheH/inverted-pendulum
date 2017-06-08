# Module level imports
import PyQt4.Qwt5 as Qwt

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qt import QEvent
from numpy import *


class PlotWindow(Qwt.QwtPlot):
    def __init__(self, nplots, *args):
        """
        Initializes the graph plotting. The usual parameters are available.

        :Parameters:
          nplots
            Number of plots in the same window.
        """
        Qwt.QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.white)
        grid = Qwt.QwtPlotGrid()
        grid.attach(self)
        grid.setMajPen(QPen(Qt.black, 0, Qt.DotLine))

        self.__nplots = nplots
        self.__curves = []
        colors = [Qt.red, Qt.darkCyan, Qt.green, Qt.darkYellow, Qt.cyan, Qt.magenta]
        for i in xrange(nplots):
            new_curve = Qwt.QwtPlotCurve('')
            new_curve.attach(self)
            new_curve.setPen(QPen(colors[i % 6]))
            new_curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
            self.__curves.append(new_curve)

    def set_curve_color(self, i, color):
        """
        Sets the color of a given plot.
        """
        self.__curves[i].setPen(QPen(color))

    def set_curve_style(self, i, estilo):
        """
        Sets the style of a given plot.
        """
        self.__curves[i].pen().setStyle(estilo)

    def set_curve_baseline(self, i, ref):
        """
        Sets the baseline of a given plot.
        """
        self.__curves[i].setBaseline(ref)

    def set_curve_brush(self, i, brush):
        """
        Sets the brush of a given plot.
        """
        self.__curves[i].setBrush(brush)

    def setData(self, i, x, y):
        """
        Plots the x, y data in the ith plot.

        :Parameters:
          i
            Number of the plot to be drawn.
          x
            Horizontal coordinates
          y
            Vertical coordinates
        """
        x = array(x)
        y = array(y)
        self.__curves[i].setData(x, y)
        self.replot()

    def set_multi_data(self, xy):
        """
        Plots the data in the set.

        :Parameters:
          xy
            List of two-tuples, where xy[:, 0] is the horizontal coordinate, and
            xy[:, 1] is the vertical coordinate.
        """
        n = len(xy)
        if n != self.__nplots:
            raise ValueError, "data and plots not equal"
        for i in xrange(n):
            x = array(xy[i][0])
            y = array(xy[i][1])
            self.__curves[i].setData(x, y)
        self.replot()

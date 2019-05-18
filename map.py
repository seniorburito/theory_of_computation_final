import time

import numpy
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.pyplot import (figure, close, text)
from matplotlib.ticker import NullLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

def getDistanceTable(positions):
    return numpy.sqrt(((positions[:,numpy.newaxis] - positions)**2).sum(axis=2))

class Map(FigureCanvasQTAgg):

    def __init__(self, parent):
        self.numberOfPoints = None
        self.positions = None
        self.distanceTable = None
        self.paths = None
        self.initialDist = None
        self.currentDist = None
        self.count = None
        self.isShift = False
        self.figure = figure()
        super(Map, self).__init__(self.figure)
        self.setParent(parent)
        self.initializeAxes()
        self.connect()

    def initializeAxes(self):
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlim(0.0, 1.0)
        self.axes.set_ylim(0.0, 1.0)
        self.axes.set_aspect("equal")
        self.axes.xaxis.set_major_locator(NullLocator())
        self.axes.yaxis.set_major_locator(NullLocator())
        self.dist_text = self.axes.text(0.0, 1.12,
                                      'Initial distance   \nCurrent distance   \n\n',
                                      va='top')


    def addPoint(self, event):
        if event.inaxes != self.axes:
            return
        if event.button != 1 or self.isShift:
            return
        x = event.xdata
        y = event.ydata
        self.axes.plot(x, y, "bo", markersize=10, picker=7)
        self.axes.lines[0].set_color("r")
        self.draw()

    def removePoint(self, event):
        mouseevent = event.mouseevent
        if mouseevent.button != 3:
            return
        thisline = event.artist
        thisline.remove()
        if len(self.axes.lines) != 0:
            self.axes.lines[0].set_color('r')
        self.draw()

    def onShiftPress(self, event):
        if event.key == 'shift':
            self.isShift = True

    def onShiftRelease(self, event):
        if event.key == 'shift':
            self.isShift = False

    def selectInitialPoint(self, event):
        mouseevent = event.mouseevent
        if mouseevent.button != 1 or not self.isShift:
            return
        thisline = event.artist
        self.axes.lines.remove(thisline)
        self.axes.lines[0].set_color('b')
        self.axes.lines.insert(0, thisline)
        self.axes.lines[0].set_color('r')
        self.draw()

    def clear(self):
        if self.numberOfPoints is not None:
            for line in self.axes.lines[self.numberOfPoints:]:
                line.remove()
                self.draw()
        self.unfreezeCurrentStatus()
        self.axes.cla()
        self.figure.clf()
        self.initializeAxes()
        self.connect()
        self.draw()


    def connect(self):
        self.cidAddPoint = self.figure.canvas.mpl_connect('button_press_event', self.addPoint)
        self.cidRemovePoint = self.figure.canvas.mpl_connect('pick_event', self.removePoint)
        self.cidShiftPress = self.figure.canvas.mpl_connect('key_press_event', self.onShiftPress)
        self.cidShiftRelease = self.figure.canvas.mpl_connect('key_release_event', self.onShiftRelease)
        self.cidSelectInitialPoint = self.figure.canvas.mpl_connect('pick_event', self.selectInitialPoint)

    def disconnect(self):
        self.figure.canvas.mpl_disconnect(self.cidAddPoint)
        self.figure.canvas.mpl_disconnect(self.cidRemovePoint)
        self.figure.canvas.mpl_disconnect(self.cidShiftPress)
        self.figure.canvas.mpl_disconnect(self.cidShiftRelease)
        self.figure.canvas.mpl_disconnect(self.cidSelectInitialPoint)

    def getx(self):
        lines = self.axes.lines
        return numpy.array([line.get_xdata() for line in lines]).flatten()

    def gety(self):
        lines = self.axes.lines
        return numpy.array([line.get_ydata() for line in lines]).flatten()

    def freezeCurrentStatus(self):
        self.disconnect()
        self.numberOfPoints = len(self.axes.lines)
        xs = self.getx()
        ys = self.gety()
        self.positions = numpy.vstack((xs, ys)).transpose()
        self.distanceTable = getDistanceTable(self.positions)
        self.paths = numpy.array(range(self.numberOfPoints))
        self.count = 0

    def unfreezeCurrentStatus(self):
        self.connect()
        self.numberOfPoints = None
        self.positions = None
        self.distanceTable = None
        self.paths = None
        self.count = None
        #self.current_dist = None

    def run(self, method):

        return {
            "Greedy Algorithm": self.greedy(),
            #"Genetic Algorithm": self.genetic(),
        }[method]

    def greedy(self):
        self.freezeCurrentStatus()
        delay = 0.5
        for index in range(self.numberOfPoints):
            if index < self.numberOfPoints - 1:
                currentPoint = self.paths[index]
                print(currentPoint)
                print(self.paths)
                remainedPoints = self.paths[index+1:]
                remainedDistance = numpy.take(self.distanceTable[currentPoint], remainedPoints)
                minPosition = numpy.argmin(remainedDistance)
                self.paths[index+1], remainedPoints[minPosition] = remainedPoints[minPosition], self.paths[index+1]
                self.plotBetweenPoints(currentPoint, self.paths[index+1])
                self.draw()
                self.figure.canvas.flush_events()
                time.sleep(delay)
                self.axes.lines[-1].set_color('b')
                self.draw()
            else:
                self.plotBetweenPoints(self.paths[index], self.paths[0])
                self.draw()
                self.figure.canvas.flush_events()
                time.sleep(delay)
                self.axes.lines[-1].set_color('b')
                self.draw()
        self.initialDist = self.calc_total_dist()
        print(self.initialDist)
        self.update_distance_displayed()

    def genetic(self):
        self.freezeCurrentStatus()
        delay = 0.5
        for index in range(self.numberOfPoints):
            if index < self.numberOfPoints - 1:


    def plotBetweenPoints(self, cind1, cind2, style='r-'):
        point1 = self.positions[cind1]
        self.count += 1
        text(point1[0], point1[1]+0.04, str(self.count), fontsize=12)
        point2 = self.positions[cind2]
        line, = self.axes.plot([point1[0], point2[0]], [point1[1], point2[1]], style)
        return line

    def calc_total_dist(self):
        size = self.numberOfPoints
        sum = 0.0
        for i in range(size):
            if i == size - 1:
                i1 = 0
            else:
                i1 = i + 1
            sum += self.distanceTable[self.paths[i], self.paths[i1]]
        return sum

    def update_distance_displayed(self):
        if self.initialDist is not None:
            if self.currentDist is not None:
                self.dist_text.set_text('Initial distance   {0:.4f}\n'\
                                        'Current distance   {1:.4f}'\
                                        .format(self.initialDist, self.currentDist))
                print(self.currentDist)
            else:
                self.dist_text.set_text('Initial distance   {0:.4f}\n'\
                                        'Current distance   '\
                                        .format(self.initialDist))
            self.draw()


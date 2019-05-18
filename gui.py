from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from map import Map


solutionMethods = ["Greedy Algorithm","Genetic Algorithm"]
defaultMethod = solutionMethods[0]

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.method = defaultMethod
        self.setUI()
        self.show()

    def setUI(self):
        self.setWindowTitle("Travelling Salesman Simulator")
        self.setGeometry(50, 50, 1280, 960)

        self.canvas = Map(self)
        self.canvas.setFocusPolicy(Qt.StrongFocus)

        labelMethods = QLabel("Method:")
        dropdownMenuMethods = QComboBox()
        dropdownMenuMethods.addItems(solutionMethods)
        dropdownMenuMethods.currentIndexChanged[str].connect(self.method_changed)

        self.buttonRun = QPushButton("Run")
        self.buttonRun.clicked.connect(self.run)

        self.buttonClear = QPushButton("Clear")
        self.buttonClear.clicked.connect(self.clear)

        layout = QHBoxLayout()

        layout.addWidget(self.canvas)

        optionLayout = QGridLayout()
        methodLayout = QHBoxLayout()
        methodLayout.addWidget(labelMethods)
        methodLayout.addWidget(dropdownMenuMethods)
        optionLayout.addLayout(methodLayout, 0, 0, 1, 2)
        optionLayout.addWidget(self.buttonRun, 1, 0)
        optionLayout.addWidget(self.buttonClear, 1, 1)
        layout.addLayout(optionLayout)

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def method_changed(self, method):
        self.method = method

    def run(self):
        self.canvas.run(self.method)

    def clear(self):
        self.canvas.clear()

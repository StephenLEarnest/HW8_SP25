import numpy as np
import PyQt5.QtWidgets as qtw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from pathlib import Path
import sys
import os
from pump import Ui_Form
from Pump_MVC import Pump_Controller


class PumpCurve_GUI_Class(Ui_Form, qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.AssignSignals()
        self.FilePath = os.getcwd()
        self.FileName = ""

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(5, 3), tight_layout=True, frameon=True))
        self.ax = self.canvas.figure.add_subplot()
        self.GL_Output.addWidget(self.canvas, 5, 0, 1, 4)

        self.myPump = Pump_Controller()
        self.setViewWidgets()
        self.show()

    def AssignSignals(self):
        self.PB_Exit.clicked.connect(self.Exit)
        self.CMD_Open.clicked.connect(self.ReadAndCalculate)

    def setViewWidgets(self):
        w = [self.LE_PumpName, self.LE_FlowUnits, self.LE_HeadUnits, self.LE_HeadCoefs, self.LE_EffCoefs, self.ax,
             self.canvas]
        self.myPump.setViewWidgets(w)

    def ReadAndCalculate(self):
        if self.OpenFile():
            with open(self.FileName, 'r') as f1:
                data = f1.readlines()
            self.myPump.ImportFromFile(data)
            return True
        return False

    def OpenFile(self):
        fname = qtw.QFileDialog.getOpenFileName(self, 'Open file',
                                                self.FilePath,
                                                "Text files (*.txt *.csv);;All files (*.*)")
        oTF = len(fname[0]) > 0
        if oTF:
            self.FileName = fname[0]
            self.FilePath = str(Path(fname[0]).parents[0])
            self.TE_Filename.setText(self.FileName)
        return oTF

    def Exit(self):
        qapp.exit()


def main():
    PumpCurve_GUI = PumpCurve_GUI_Class()
    qapp.exec_()


if __name__ == "__main__":
    qapp = qtw.QApplication(sys.argv)
    main()
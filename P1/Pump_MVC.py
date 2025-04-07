import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import PyQt5.QtWidgets as qtw
from LeastSquares import LeastSquaresFit_Class


class Pump_Model():
    def __init__(self):
        self.PumpName = ""
        self.FlowUnits = ""
        self.HeadUnits = ""
        self.FlowData = np.array([])
        self.HeadData = np.array([])
        self.EffData = np.array([])
        self.HeadCoefficients = np.array([])
        self.EfficiencyCoefficients = np.array([])
        self.LSFitHead = LeastSquaresFit_Class()
        self.LSFitEff = LeastSquaresFit_Class()


class Pump_Controller():
    def __init__(self):
        self.Model = Pump_Model()
        self.View = Pump_View()

    def ImportFromFile(self, data):
        self.Model.PumpName = data[0].split(':')[1].strip()  # Parse "PumpName: TestPump"
        L = data[1].split()  # Parse units line
        self.Model.FlowUnits = L[0].split('(')[1].rstrip(')')  # Extract "gpm" from "FlowUnits(gpm)"
        self.Model.HeadUnits = L[1].split('(')[1].rstrip(')')  # Extract "ft" from "HeadUnits(ft)"
        self.SetData(data[3:])  # Skip header lines
        self.updateView()

    def SetData(self, data):
        self.Model.FlowData = np.array([])
        self.Model.HeadData = np.array([])
        self.Model.EffData = np.array([])
        for L in data:
            Cells = L.split()
            if len(Cells) >= 3:
                self.Model.FlowData = np.append(self.Model.FlowData, float(Cells[0].strip()))
                self.Model.HeadData = np.append(self.Model.HeadData, float(Cells[1].strip()))
                self.Model.EffData = np.append(self.Model.EffData, float(Cells[2].strip()))
        self.LSFit()

    def LSFit(self):
        # Quadratic fit for Head (degree 2)
        self.Model.LSFitHead.x = self.Model.FlowData
        self.Model.LSFitHead.y = self.Model.HeadData
        self.Model.LSFitHead.LeastSquares(2)
        # Cubic fit for Efficiency (degree 3)
        self.Model.LSFitEff.x = self.Model.FlowData
        self.Model.LSFitEff.y = self.Model.EffData
        self.Model.LSFitEff.LeastSquares(3)

    def setViewWidgets(self, w):
        self.View.setViewWidgets(w)

    def updateView(self):
        self.View.updateView(self.Model)


class Pump_View():
    def __init__(self):
        self.LE_PumpName = qtw.QLineEdit()
        self.LE_FlowUnits = qtw.QLineEdit()
        self.LE_HeadUnits = qtw.QLineEdit()
        self.LE_HeadCoefs = qtw.QLineEdit()
        self.LE_EffCoefs = qtw.QLineEdit()
        self.ax = None
        self.canvas = None

    def updateView(self, Model):
        self.LE_PumpName.setText(Model.PumpName)
        self.LE_FlowUnits.setText(Model.FlowUnits)
        self.LE_HeadUnits.setText(Model.HeadUnits)
        self.LE_HeadCoefs.setText(Model.LSFitHead.GetCoeffsString())
        self.LE_EffCoefs.setText(Model.LSFitEff.GetCoeffsString())
        self.DoPlot(Model)

    def DoPlot(self, Model):
        headx, heady, headRSq = Model.LSFitHead.GetPlotInfo(2, npoints=500)
        effx, effy, effRSq = Model.LSFitEff.GetPlotInfo(3, npoints=500)

        self.ax.clear()
        # Head plot (left y-axis)
        self.ax.plot(Model.FlowData, Model.HeadData, 'bo', label='Head Data')
        self.ax.plot(headx, heady, 'b-', label=f'Head Fit (R²={headRSq:.3f})')
        self.ax.set_xlabel(f'Flow ({Model.FlowUnits})')
        self.ax.set_ylabel(f'Head ({Model.HeadUnits})', color='b')
        self.ax.tick_params(axis='y', labelcolor='b')

        # Efficiency plot (right y-axis)
        ax2 = self.ax.twinx()
        ax2.plot(Model.FlowData, Model.EffData, 'ro', label='Efficiency Data')
        ax2.plot(effx, effy, 'r-', label=f'Eff Fit (R²={effRSq:.3f})')
        ax2.set_ylabel(f'Efficiency (%)', color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        # Title and legend
        self.ax.set_title(f'Pump Curve: {Model.PumpName}')
        lines1, labels1 = self.ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        self.ax.legend(lines1 + lines2, labels1 + labels2, loc='best')

        self.canvas.draw()

    def setViewWidgets(self, w):
        self.LE_PumpName, self.LE_FlowUnits, self.LE_HeadUnits, self.LE_HeadCoefs, self.LE_EffCoefs, self.ax, self.canvas = w


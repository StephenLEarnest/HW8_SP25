class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.AssignSlots()
        self.MakeCanvas()

        self.input_widgets = [self.rb_SI, self.le_PHigh, self.le_PLow, self.le_TurbineInletCondition, self.rdo_Quality, self.le_TurbineEff, self.cmb_XAxis, self.cmb_YAxis, self.chk_logX, self.chk_logY]
        self.display_widgets = [self.lbl_PHigh, self.lbl_PLow, self.lbl_SatPropLow, self.lbl_SatPropHigh, self.lbl_TurbineInletCondition, self.lbl_H1, self.lbl_H1Units, self.lbl_H2, self.lbl_H2Units, self.lbl_H3, self.lbl_H3Units, self.lbl_H4, self.lbl_H4Units, self.lbl_TurbineWork, self.lbl_TurbineWorkUnits, self.lbl_PumpWork, self.lbl_PumpWorkUnits, self.lbl_HeatAdded, self.lbl_HeatAddedUnits, self.lbl_ThermalEfficiency, self.canvas, self.figure, self.ax]
        self.RC = rankineController(self.input_widgets, self.display_widgets)

        self.setNewPHigh()  # Initialize P High
        self.setNewPLow()   # Initialize P Low
        self.Calculate()    # Perform initial calculation

        self.oldXData = 0.0
        self.oldYData = 0.0
        self.show()

# Rest of the class remains unchanged

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Rankine calculator')  # Corrected window title line
    sys.exit(app.exec())
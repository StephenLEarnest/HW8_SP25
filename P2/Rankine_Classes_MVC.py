class rankineView():
    def __init__(self):
        pass

    def setWidgets(self, *args):
        self.rb_SI, self.le_PHigh, self.le_PLow, self.le_TurbineInletCondition, self.rdo_Quality, self.le_TurbineEff, self.cmb_XAxis, self.cmb_YAxis, self.chk_logX, self.chk_logY = args[0]
        self.lbl_PHigh, self.lbl_PLow, self.lbl_SatPropLow, self.lbl_SatPropHigh, self.lbl_TurbineInletCondition, self.lbl_H1, self.lbl_H1Units, self.lbl_H2, self.lbl_H2Units, self.lbl_H3, self.lbl_H3Units, self.lbl_H4, self.lbl_H4Units, self.lbl_TurbineWork, self.lbl_TurbineWorkUnits, self.lbl_PumpWork, self.lbl_PumpWorkUnits, self.lbl_HeatAdded, self.lbl_HeatAddedUnits, self.lbl_ThermalEfficiency, self.canvas, self.figure, self.ax = args[1]

    def selectQualityOrTHigh(self, Model=None):
        SI = self.rb_SI.isChecked()
        if self.rdo_Quality.isChecked():
            self.le_TurbineInletCondition.setText("1.0")
            self.le_TurbineInletCondition.setEnabled(False)
        else:
            satProps = Model.steam.getsatProps_p(Model.p_high)
            T = satProps.tsat if SI else UC.C_to_F(satProps.tsat)
            self.le_TurbineInletCondition.setText("{:0.2f}".format(T))
            self.le_TurbineInletCondition.setEnabled(True)
        x = self.rdo_Quality.isChecked()
        self.lbl_TurbineInletCondition.setText(
            "Turbine Inlet: {}{} =".format('x' if x else 'THigh', '' if x else ('(C)' if SI else '(F)')))

    def setNewPHigh(self, Model=None):
        SI = self.rb_SI.isChecked()
        PCF = 1 if SI else UC.psi_to_bar
        try:
            p_high = float(self.le_PHigh.text()) * PCF
            satProps = Model.steam.getsatProps_p(p=p_high)
            self.lbl_SatPropHigh.setText(satProps.getTextOutput(SI=SI))
            if not self.rdo_Quality.isChecked():  # Update T High if selected
                T = satProps.tsat if SI else UC.C_to_F(satProps.tsat)
                self.le_TurbineInletCondition.setText("{:0.2f}".format(T))
        except ValueError:
            self.lbl_SatPropHigh.setText("Invalid P High")
        self.selectQualityOrTHigh(Model)  # Ensure label updates

    def setNewPLow(self, Model=None):
        SI = self.rb_SI.isChecked()
        PCF = 1 if SI else UC.psi_to_bar
        try:
            p_low = float(self.le_PLow.text()) * PCF
            satProps = Model.steam.getsatProps_p(p=p_low)
            self.lbl_SatPropLow.setText(satProps.getTextOutput(SI=SI))
        except ValueError:
            self.lbl_SatPropLow.setText("Invalid P Low")

    def outputToGUI(self, Model=None):
        if Model.state1 is None:
            return
        HCF = 1 if Model.SI else UC.kJperkg_to_BTUperlb
        self.lbl_H1.setText("{:0.2f}".format(Model.state1.h * HCF))
        self.lbl_H2.setText("{:0.2f}".format(Model.state2.h * HCF))
        self.lbl_H3.setText("{:0.2f}".format(Model.state3.h * HCF))
        self.lbl_H4.setText("{:0.2f}".format(Model.state4.h * HCF))
        self.lbl_TurbineWork.setText("{:0.2f}".format(Model.turbine_work * HCF))
        self.lbl_PumpWork.setText("{:0.2f}".format(Model.pump_work * HCF))
        self.lbl_HeatAdded.setText("{:0.2f}".format(Model.heat_added * HCF))
        self.lbl_ThermalEfficiency.setText("{:0.2f}".format(Model.efficiency))
        satPropsLow = Model.steam.getsatProps_p(p=Model.p_low)
        satPropsHigh = Model.steam.getsatProps_p(p=Model.p_high)
        self.lbl_SatPropLow.setText(satPropsLow.getTextOutput(SI=Model.SI))
        self.lbl_SatPropHigh.setText(satPropsHigh.getTextOutput(SI=Model.SI))
        self.plot_cycle_XY(Model=Model)

    def updateUnits(self, Model=None):
        SI = Model.SI
        pCF = 1 if SI else UC.bar_to_psi
        HCF = 1 if SI else UC.kJperkg_to_BTUperlb

        # Update pressure inputs
        try:
            self.le_PHigh.setText("{:0.2f}".format(float(self.le_PHigh.text()) * pCF))
            self.le_PLow.setText("{:0.2f}".format(float(self.le_PLow.text()) * pCF))
        except ValueError:
            pass  # Ignore invalid inputs
        self.lbl_PHigh.setText("PHigh ({}) =".format("bar" if SI else "psi"))
        self.lbl_PLow.setText("PLow ({}) =".format("bar" if SI else "psi"))

        # Update T High if applicable
        if not self.rdo_Quality.isChecked():
            try:
                T = float(self.le_TurbineInletCondition.text())
                T_converted = T if SI else UC.F_to_C(T)  # Convert current value to SI
                self.le_TurbineInletCondition.setText("{:0.2f}".format(T_converted if SI else UC.C_to_F(T_converted)))
            except ValueError:
                satProps = Model.steam.getsatProps_p(Model.p_high)
                T = satProps.tsat if SI else UC.C_to_F(satProps.tsat)
                self.le_TurbineInletCondition.setText("{:0.2f}".format(T))

        # Update unit labels
        hUnits = "kJ/kg" if SI else "BTU/lb"
        self.lbl_H1Units.setText(hUnits)
        self.lbl_H2Units.setText(hUnits)
        self.lbl_H3Units.setText(hUnits)
        self.lbl_H4Units.setText(hUnits)
        self.lbl_TurbineWorkUnits.setText(hUnits)
        self.lbl_PumpWorkUnits.setText(hUnits)
        self.lbl_HeatAddedUnits.setText(hUnits)

        # Update outputs and plot
        self.outputToGUI(Model=Model)

    # No changes to print_summary, plot_cycle_TS, plot_cycle_XY
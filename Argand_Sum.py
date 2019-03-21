import sys, os
import scipy as sp
import numpy as np

# GUI and plotting
import pyqtgraph as pg
import pyqtgraph.exporters # is not imported automatically with pyqtgraph in newer versions
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4 import QtCore, QtGui

Torricelli_program_folder_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(Torricelli_program_folder_path+os.sep+'imports')

from pyArgand import ArgandPlotWidget
from GUI_Argand_Sum import Ui_MainWindow



class ArgandSum(QtGui.QMainWindow):
    ## Torricelli class constructor
    def __init__(self, parent=None):
        super(ArgandSum, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.argand = ArgandPlotWidget()
        self.ui.verticalLayout.addWidget(self.argand)
        self.connect_all()
        self.Argand_replot_Components()
        #self.Display_Sum()


    def Argand_replot_Components(self):
        if self.ui.checkBox_keepTrackofSum.isChecked() == False : self.argand.clearArgand()
        pc_ZL    = self.ui.doubleSpinBox_Pc_ZL.value()
        fc_ZL    = self.ui.doubleSpinBox_Fc_ZL.value()
        pc_1stGr = self.ui.doubleSpinBox_Pc_1stGr.value()
        fc_1stGr = self.ui.doubleSpinBox_Fc_1stGr.value()
        pc_2ndGr = self.ui.doubleSpinBox_Pc_2ndGr.value()
        fc_2ndGr = self.ui.doubleSpinBox_Fc_2ndGr.value()
        
        self.argand.addDataSet([pc_ZL, fc_ZL], [0,0], drawError=False, color=(255,0,0), symb='o', size=10, ident='ZL')
        self.argand.addDataSet([pc_1stGr, fc_1stGr], [0,0], drawError=False, color=(0,255,0), symb='o', size=10, ident='1stGr')
        self.argand.addDataSet([pc_2ndGr, fc_2ndGr], [0,0], drawError=False, color=(0,0,255), symb='o', size=10, ident='2ndGr')

        qty_ZL    = self.ui.doubleSpinBox_Qty_ZL.value()
        qty_1stGr = self.ui.doubleSpinBox_Qty_1stGr.value()
        qty_2ndGr = self.ui.doubleSpinBox_Qty_2ndGr.value()
        Total_qty = qty_ZL + qty_1stGr + qty_2ndGr
        n_ZL    = qty_ZL    / Total_qty
        n_1stGr = qty_1stGr / Total_qty
        n_2ndGr = qty_2ndGr / Total_qty
        self.ui.doubleSpinBox_n_ZL.setValue(n_ZL)
        self.ui.doubleSpinBox_n_1stGr.setValue(n_1stGr)
        self.ui.doubleSpinBox_n_2ndGr.setValue(n_2ndGr)
        self.ui.doubleSpinBox_n_Sum.setValue(n_ZL+n_1stGr+n_2ndGr)
        self.ui.doubleSpinBox_Qty_Sum.setValue(Total_qty)

        xA, yA = self.argand.convertPcFc_to_cartesian(pc_ZL,    fc_ZL   *n_ZL)
        xB, yB = self.argand.convertPcFc_to_cartesian(pc_1stGr, fc_1stGr*n_1stGr)
        xC, yC = self.argand.convertPcFc_to_cartesian(pc_2ndGr, fc_2ndGr*n_2ndGr)
        pos_complex_A = xA + 1j*yA
        pos_complex_B = xB + 1j*yB
        pos_complex_C = xC + 1j*yC
        pos_complex_sum = pos_complex_A + pos_complex_B + pos_complex_C
        pcSum, fcSum = self.Argand_convertComplex2Argand(pos_complex_sum)
        self.ui.doubleSpinBox_Pc_Sum.setValue(pcSum)
        self.ui.doubleSpinBox_Fc_Sum.setValue(fcSum)
        self.argand.addDataSet([pcSum, fcSum], [0,0], drawError=False, color=(255*n_ZL, 255*n_1stGr, 255*n_2ndGr), symb='o', size=5, ident='2ndGrSum')       

    def connect_all(self):
        self.ui.doubleSpinBox_Pc_ZL.valueChanged.connect(self.Argand_replot_Components)
        self.ui.doubleSpinBox_Fc_ZL.valueChanged.connect(self.Argand_replot_Components)
        self.ui.doubleSpinBox_Qty_ZL.valueChanged.connect(self.Argand_replot_Components)
        self.ui.doubleSpinBox_Pc_1stGr.valueChanged.connect(self.Argand_replot_Components)
        self.ui.doubleSpinBox_Fc_1stGr.valueChanged.connect(self.Argand_replot_Components)
        self.ui.doubleSpinBox_Qty_1stGr.valueChanged.connect(self.Argand_replot_Components)
        self.ui.doubleSpinBox_Pc_2ndGr.valueChanged.connect(self.Argand_replot_Components)
        self.ui.doubleSpinBox_Fc_2ndGr.valueChanged.connect(self.Argand_replot_Components)
        self.ui.doubleSpinBox_Qty_2ndGr.valueChanged.connect(self.Argand_replot_Components)

    ## convert a complex (cartesian) value to positon and fraction
    # Makes sure that 0<pc<1
    def Argand_convertComplex2Argand(self, pos_cartesian):
        pc = np.angle(pos_cartesian)/(2*np.pi)
        fc = np.absolute(pos_cartesian)
        while pc > 1.:
            pc = pc - 1.
        while pc < 0.:
            pc = pc + 1.
        return pc, fc

        
# Starts the program
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ArgandSum()
    myapp.show()
    sys.exit(app.exec_())

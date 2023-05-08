
import sys
import numpy as np
import ctypes

from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QPushButton, 
    QDialog, 
    QComboBox,
    QStyleFactory, 
    QLabel, 
    QCheckBox, 
    QHBoxLayout, 
    QVBoxLayout, 
    QGroupBox, 
    QRadioButton,
    QTabWidget, 
    QSizePolicy, 
    QTableWidget, 
    QTextEdit, 
    QLineEdit, 
    QSpinBox, 
    QDateTimeEdit, 
    QSlider, 
    QScrollBar, 
    QDial, 
    QGridLayout, 
    QFileDialog, 
    QDialogButtonBox, 
    QFormLayout, 
    QInputDialog,
    QColorDialog
)
from PyQt6.QtCore import (
    QCoreApplication, 
    Qt, 
    QDateTime, 
    QDir
)

from PyQt6.QtGui import QColor

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qtagg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)

################################################################################

class InputDialog(QDialog):

    def __init__(self, labels, parent=None):
      super().__init__(parent)
                    
      buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
          QDialogButtonBox.StandardButton.Cancel, self)
      layout = QFormLayout(self)
        
      self.inputs = []
      for lab in labels:
        self.inputs.append(QLineEdit(self))
        layout.addRow(lab, self.inputs[-1])
        
      layout.addWidget(buttonBox)
        
      buttonBox.accepted.connect(self.accept)
      buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
      return tuple(input.text() for input in self.inputs)

################################################################################

class Voigt(QMainWindow):

    def __init__(self, main, parent=None):
      super().__init__()
      INPUT['Par'] = []
      INPUT['Par'].append(["","","500","1"])
      INPUT['Color'] = []
      INPUT['Color'].append(QColor(155, 0, 155))
      INPUT['Curve'] = []
      INPUT['Curve'].append(plt.plot([0],[0]))
      INPUT['Curve_plot'] = []
      INPUT['Curve_plot'].append(False)
      INPUT['Curve_xlabel'] = False
      self.initUI(main)
      self.libpath()

    def initUI(self, main):
 
      self.__createCurveGroupBox()
      self.__createLibBox()
      createBottomlayout(self,main)

      self.figure = plt.figure()
      self.canvas = FigureCanvas(self.figure)
      self.ax = None
      layout = QGridLayout()

      layout.addWidget(self.canvas, 0, 0, 3, 3)
      layout.addWidget(NavigationToolbar(self.canvas, self), 3, 0, 1, 3)

      layout.addWidget(self.CurveGroupBox, 0, 3, 4, 1)
     
      layout.addWidget(self.LibBox, 4, 0, 1, 4)
      layout.addLayout(self.Bottomlayout, 5, 0, 1, 4)

      layout.setRowStretch(0, 1)
      layout.setColumnStretch(0, 1)

      widget = QWidget()
      widget.setLayout(layout)
      self.statusBar()
      self.setCentralWidget(widget)

    def libpath(self):
      INPUT['Path'] = './lib/clib.so'
      self.LibBox.path[0].setText(INPUT['Path'])
      global clib
      clib = ctypes.CDLL(INPUT['Path'])
      clib.profile.argtypes=[ctypes.POINTER(ctypes.c_double),
                      ctypes.c_int,
                      ctypes.c_double,
                      ctypes.c_double,
                      ctypes.POINTER(ctypes.c_double),
                      ctypes.POINTER(ctypes.c_double)]

      clib.GAUSS_PROFILE.argtypes=[ctypes.POINTER(ctypes.c_double),
                      ctypes.c_int,
                      ctypes.c_double,
                      ctypes.POINTER(ctypes.c_double)]

      clib.LORENTZ_PROFILE.argtypes=[ctypes.POINTER(ctypes.c_double),
                      ctypes.c_int,
                      ctypes.c_double,
                      ctypes.POINTER(ctypes.c_double)]
      print(INPUT['Path'])

################################################################################

################################################################################
            
    def __createCurveGroupBox(self):

      labels=['\u0394\u03BB  [m\u212B]','a  [m\u212B]', 'Number of grids', 
          'Resulution  [m\u212B]']
        
      self.CurveGroupBox = QGroupBox("")

      self.CurveGroupBox.Curve_Indx = QLabel("Curve Number:")
      self.CurveGroupBox.Curve_Indx.setAlignment(Qt.AlignmentFlag.AlignCenter)

      self.CurveGroupBox.NCurve = QLineEdit(self)
      self.CurveGroupBox.NCurve.setEnabled(False)
      self.CurveGroupBox.NCurve.setText(str(INPUT['Ncurves']))
      self.CurveGroupBox.NCurve.setAlignment(Qt.AlignmentFlag.AlignCenter)

      self.CurveGroupBox.CurveParBox = QComboBox()
      self.CurveGroupBox.CurveParBox.addItems(['Curve '
          +str(INPUT['Ncurves'])+': '])
      self.CurveGroupBox.CurveParBox.currentIndexChanged.connect(
          self.__Curve_index_changed
      )

      self.CurveGroupBox.plus= QPushButton("+", self)
      self.CurveGroupBox.plus.clicked.connect(
          lambda: self.__plus(layout)
      )
        
      self.CurveGroupBox.minus = QPushButton("-", self)
      self.CurveGroupBox.minus.clicked.connect(
          lambda: self.__minus(layout)
      )
        
      self.CurveGroupBox.par = []
      self.CurveGroupBox.Label = []
    
      self.CurveGroupBox.par = []
      self.CurveGroupBox.Label = []
      for i in range(4):
        self.CurveGroupBox.Label.append(QLabel(labels[i]))
        self.CurveGroupBox.par.append(QLineEdit(self))
        self.CurveGroupBox.par[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.CurveGroupBox.par[i].setEnabled(False)
        #self.CurveGroupBox.par[i].setPlaceholderText(str(i))
        self.CurveGroupBox.par[i].setText(INPUT['Par'][0][i])


      self.CurveGroupBox.par[0].editingFinished.connect(
        lambda: self.__get_par(0)
      )
      self.CurveGroupBox.par[1].editingFinished.connect(
        lambda: self.__get_par(1)
      )
      self.CurveGroupBox.par[2].editingFinished.connect(
        lambda: self.__get_par(2)
      )
      self.CurveGroupBox.par[3].editingFinished.connect(
        lambda: self.__get_par(3)
      )

      self.CurveGroupBox.CurveTypeBox = QComboBox()
      self.CurveGroupBox.CurveTypeBox.addItem("Voigt")  
      self.CurveGroupBox.CurveTypeBox.addItem("Gaussian")  
      self.CurveGroupBox.CurveTypeBox.addItem("Lorentz")  
      self.CurveGroupBox.CurveTypeBox.addItem("Dispersion")  


      self.CurveGroupBox.cbutton = QPushButton("Choose a color")
      self.CurveGroupBox.cbutton.setStyleSheet(
          f"background-color: {INPUT['Color'][0].name()}"
      )
      self.CurveGroupBox.cbutton.clicked.connect(self.__color)

      self.CurveGroupBox.btn= QPushButton("plot")
      self.CurveGroupBox.btn.clicked.connect(self.__plot)


      layout = QGridLayout()

      layout.addWidget(self.CurveGroupBox.Curve_Indx,0,0,1,2)
      layout.addWidget(self.CurveGroupBox.NCurve,1,0,1,2)
      layout.addWidget(self.CurveGroupBox.minus,2, 0, 1, 1)
      layout.addWidget(self.CurveGroupBox.plus,2, 1, 1, 1)

      layout.addWidget(self.CurveGroupBox.CurveParBox, 3, 0, 1, 2)

      for i in range(4):
        layout.addWidget(self.CurveGroupBox.Label[i], 4+i, 0, 1, 1)
        layout.addWidget(self.CurveGroupBox.par[i], 4+i, 1, 1, 1)
      layout.addWidget(self.CurveGroupBox.CurveTypeBox, 8, 0, 1, 2)
      layout.addWidget(self.CurveGroupBox.cbutton, 9, 0, 1, 2)
      layout.addWidget(self.CurveGroupBox.btn, 10, 0, 1, 2)


      layout.setRowStretch(12, 1)
      layout.setColumnStretch(0, 1)
      layout.setColumnStretch(1, 1)

      self.CurveGroupBox.setLayout(layout)

    def __plus(self, layout):
      INPUT['Ncurves'] = INPUT['Ncurves']+1
      self.CurveGroupBox.NCurve.setText(str(INPUT['Ncurves']))
      INPUT['Par'].append(["","","500","1"])
      INPUT['Color'].append(QColor(155, 0, 155))
      self.CurveGroupBox.CurveParBox.addItems(['Curve '+str(INPUT['Ncurves'])+': '])
      INPUT['Curve'].append(plt.plot([0],[0]))
      INPUT['Curve_plot'].append(False)
        
    def __minus(self, layout):
      INPUT['Ncurves'] = INPUT['Ncurves']-1
      if INPUT['Ncurves'] <1 :
        INPUT['Ncurves'] = 1
      else:
        del(INPUT['Par'][INPUT['Ncurves']])
        del(INPUT['Color'][INPUT['Ncurves']])
        if INPUT['Curve_plot'][INPUT['Ncurves']]:
          INPUT['Curve'][INPUT['Ncurves']].remove()
          self.canvas.draw()
        del(INPUT['Curve'][INPUT['Ncurves']])
        del(INPUT['Curve_plot'][INPUT['Ncurves']])
        self.CurveGroupBox.CurveParBox.removeItem(INPUT['Ncurves'])
        
      self.CurveGroupBox.NCurve.setText(str(INPUT['Ncurves']))

    def __Curve_index_changed(self, index):
      for i in range(4):
        self.CurveGroupBox.par[i].setText(INPUT['Par'][index][i])
      if INPUT['Color'][index].isValid():
        self.CurveGroupBox.cbutton.setStyleSheet(
            f"background-color: {INPUT['Color'][index].name()}"
        )
        
    def __get_par(self, i):
      index = self.CurveGroupBox.CurveParBox.currentIndex()
      INPUT['Par'][index][i] = self.CurveGroupBox.par[i].text()

    def __color(self):
      index = self.CurveGroupBox.CurveParBox.currentIndex()
      INPUT['Color'][index] = QColorDialog.getColor()
     
      if INPUT['Color'][index].isValid():
        self.CurveGroupBox.cbutton.setStyleSheet(
            f"background-color: {INPUT['Color'][index].name()}"
        )

    def __plot(self):

      if self.ax is None:
        self.ax = self.figure.add_subplot(111)

      index = self.CurveGroupBox.CurveParBox.currentIndex()
      cindex = self.CurveGroupBox.CurveTypeBox.currentIndex()


      dnu = float(INPUT['Par'][index][0])/1e3
      a = float(INPUT['Par'][index][1])/1e3
      num = int(INPUT['Par'][index][2])
      res = float(INPUT['Par'][index][3])/1e3

      length = res/2.0*num
      ll = np.linspace(-length,length,num)

      c_Lambd = (ctypes.c_double*num)()
      c_H = (ctypes.c_double*num)()
      c_L = (ctypes.c_double*num)()

      c_Nlambd = ctypes.c_int(num)
      c_dnu = ctypes.c_double(dnu)
      c_a = ctypes.c_double(a)
      for i in range(num):
        c_Lambd[i] = ll[i]
     
      if cindex == 0:
        clib.profile(c_Lambd, c_Nlambd, c_dnu, c_a, c_H, c_L)
      elif cindex == 1:
        clib.GAUSS_PROFILE(c_Lambd, c_Nlambd, c_dnu, c_H)
      elif cindex == 2:
        clib.LORENTZ_PROFILE(c_Lambd, c_Nlambd, c_a, c_H)
      elif cindex == 3:
        clib.profile(c_Lambd, c_Nlambd, c_dnu, c_a, c_L, c_H)


      if INPUT['Curve_plot'][index]:
        INPUT['Curve'][index].remove()
      else:
        INPUT['Curve_plot'][index] = True

      if INPUT['Color'][index].isValid():
        INPUT['Curve'][index], = self.ax.plot(c_Lambd[:],c_H[:],
            color=INPUT['Color'][index].name())
      else:
        INPUT['Curve'][index], = self.ax.plot(c_Lambd[:],c_H[:],
            color='k')

      if INPUT['Curve_xlabel'] == False:
        self.ax.set_xlabel(r'$\lambda$ [$\rm \AA$]')

      self.canvas.draw()

    def __createLibBox(self):
    
      self.LibBox = QGroupBox("")
      layout = QGridLayout()
    
      INPUT['Path'] = ''

      self.LibBox.label = []
      self.LibBox.label.append(QLabel('Path to C lib',self))
      self.LibBox.label[0].setIndent(10)

      self.LibBox.btn = []
      self.LibBox.path = []
      self.LibBox.btnrm = []

      self.LibBox.btn.append(QPushButton('Find',self))
      self.LibBox.path.append(QLineEdit(self))
      self.LibBox.path[0].setEnabled(False)
      self.LibBox.btnrm.append(QPushButton('remove',self))
            
      self.LibBox.btn[0].clicked.connect(
        lambda text: self.__getFiles()
      )

      self.LibBox.btnrm[0].clicked.connect(
        lambda text: self.__removebtn()
      )
    
        
      layout.addWidget(self.LibBox.label[0], 0, 0, 1, 2)
      layout.addWidget(self.LibBox.path[0], 0, 2, 1, 4)
      layout.addWidget(self.LibBox.btn[0], 0, 6, 1, 1)
      layout.addWidget(self.LibBox.btnrm[0], 0, 7, 1, 1)
    

      #layout.setRowStretch(3, 1)
      layout.setColumnStretch(4, 1)

      self.LibBox.setLayout(layout)
           
    def __getFiles(self):
      dig = QFileDialog()
      #help(QFileDialog)
      #dig.setFileMode(QFileDialog.AnyFile)
      #dig.setFilter(QDir.Files)
      if dig.exec():
        filenames = dig.selectedFiles()
        self.LibBox.path[0].setText(filenames[0])
        INPUT['Path'] = filenames[0]
        clib = ctypes.CDLL(INPUT['Path'])
        clib.profile.argtypes=[ctypes.POINTER(ctypes.c_double),
                      ctypes.c_int,
                      ctypes.c_double,
                      ctypes.c_double,
                      ctypes.POINTER(ctypes.c_double),
                      ctypes.POINTER(ctypes.c_double)]

        clib.GAUSS_PROFILE.argtypes=[ctypes.POINTER(ctypes.c_double),
                      ctypes.c_int,
                      ctypes.c_double,
                      ctypes.POINTER(ctypes.c_double)]

        clib.LORENTZ_PROFILE.argtypes=[ctypes.POINTER(ctypes.c_double),
                      ctypes.c_int,
                      ctypes.c_double,
                      ctypes.POINTER(ctypes.c_double)]
        print(INPUT['Path'])
         
    def __removebtn(self):
        self.LibBox.path[0].setText('')
        INPUT['Path'] = ''

################################################################################
    
def createBottomlayout(self, main):
    
    self.Bottomlayout = QHBoxLayout()
    self.Bottomlayout.btn = []
    self.Bottomlayout.btn.append(QPushButton("Return", self))
    self.Bottomlayout.btn[0].clicked.connect(main.show)
    self.Bottomlayout.btn[0].clicked.connect(self.close)
      
    self.Bottomlayout.btn.append(QPushButton("reset", self))
    self.Bottomlayout.btn[1].clicked.connect(main.show)
    self.Bottomlayout.btn[1].clicked.connect(self.close)

    self.Bottomlayout.btn.append(QPushButton("Quit", self))
    self.Bottomlayout.btn[2].clicked.connect(QCoreApplication.instance().quit)
        
    for i in range(3):
      self.Bottomlayout.addWidget(self.Bottomlayout.btn[i])
       
################################################################################

class Main(QMainWindow):
    def __init__(self):
      global INPUT
      global clib
      super().__init__()
      INPUT = {}
      INPUT['Ncurves'] = 1
      self.initUI()

    def initUI(self):

      self.setWindowTitle("Illustration")
      self.__window1 = Voigt(self)

      layout = QVBoxLayout()
        
      self.btn = []
      self.btn.append(QPushButton("Voigt Profile", self))
      self.btn.append(QPushButton("Quit", self))

      self.btn[0].clicked.connect(self.__window1.show)
      self.btn[0].clicked.connect(self.__closewindow)
      self.btn[1].clicked.connect(QCoreApplication.instance().quit)
    
      self.btn[0].setStatusTip("Voigt Profile")
      self.btn[1].setStatusTip("Quit:Ctrl+Q")
      self.btn[1].setShortcut("Ctrl+Q")

      for i in range(2):
        layout.addWidget(self.btn[i])

      self.statusBar()
      widget = QWidget()
      widget.setLayout(layout)
      self.setCentralWidget(widget)
        
    def __closewindow(self):
      self.close()

################################################################################

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec())
    

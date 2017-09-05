import sys
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Fourier Series')
        self.setMinimumWidth(400)
        
        #create inputs and add them to UI
        groupBox1= QtWidgets.QGroupBox("Signal Parameters")
        form = QtWidgets.QFormLayout()
        form_ui_label=["f0","a0","a1","b1","a2","b2","a3","b3","a4","b4","a5","b5","a6","b6"]
        
        self.form_ui=[]
        for index in range(14):
            self.form_ui.append(QtWidgets.QDoubleSpinBox())
            self.form_ui[index].setMinimum(-99)
            self.form_ui[index].valueChanged.connect(self.plot)
            form.addRow(QtWidgets.QLabel("%s :" % form_ui_label[index]), self.form_ui[index])

        groupBox1.setLayout(form)
        
        self.figure = plt.figure(facecolor=(228/255, 228/255, 228/255))   # uniformize background color
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        groupBox2= QtWidgets.QGroupBox("Signal Waveform")
        vBox2 = QtWidgets.QVBoxLayout()
        vBox2.addStretch(1)
        vBox2.addWidget(self.toolbar)
        vBox2.addWidget(self.canvas)
        groupBox2.setLayout(vBox2)
        
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addWidget(groupBox1)
        mainLayout.addWidget(groupBox2)
        self.setLayout(mainLayout)
        
        #self.setGeometry(500, 300, 250, 150)
            
#self.setLayout(mainLayout)
    
    def plot(self):
        f0=self.form_ui[0].value();         #extract frequency
        t=np.arange(0,1,1/1000)             #discretize time axis

        a0=self.form_ui[1].value()
        data=a0*np.cos(0*t)                 #DC component
        for k in range(1,6):
            ak=self.form_ui[2*k].value()    #extract ak Fourier Coefficients
            bk=self.form_ui[1+2*k].value()  #extract bk Fourier Coefficients
            data = data+ak*np.cos(2*np.pi*k*f0*t)+bk*np.sin(2*np.pi*k*f0*t) #add harmonic
        
        ax = self.figure.add_subplot(111)   #update matplotlib figure
        ax.hold(False)
        ax.plot(t,data, '-')
        self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.plot()
    main.show()
    sys.exit(app.exec_())
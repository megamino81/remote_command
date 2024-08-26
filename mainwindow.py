#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer
from pyqtgraph import PlotWidget, plot

import pyqtgraph as pg
import os, time
import utils

UPDATE_INTERVAL = 2000

###############################################################################
# Main UI

_uiClass = uic.loadUiType("ui/mainwindow.ui")[0]
class MainWindow(QMainWindow, _uiClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_Start.clicked.connect(self.start_clicked)
        self.pushButton_Stop.clicked.connect(self.stop_clicked)
        self.pushButton_UncoreSet.clicked.connect(self.uncore_set_clicked)
        self.pushButton_CoreSet.clicked.connect(self.core_set_clicked)
        self.pushButton_Cmd.clicked.connect(self.cmd_clicked)

        self.timer=QTimer()
        self.timer.timeout.connect(self.update)


        self.sec_list = [1,2,3,4,5,6,7,8,9,10]
        self.core_list = [10,22,24,12,13,21,19,12,25,25]
        self.uncore_list = [12,24,21,10,18,29,29,22,15,15]
        self.power_list = [30,32,34,32,33,31,29,32,35,45]

        self.monitor_stop()
        self.init_graph()

    def showTime(self):
        print ("update")

    def start_clicked(self):
        print ("Start")
        self.monitor_start()

    def stop_clicked(self):
        print ("Stop")
        self.monitor_stop()

    def uncore_set_clicked(self):
        print ("Uncore Set")
        # textEdit_UncoreWrite
        # wrmsr 0x620
        value = self.textEdit_UncoreWrite.toPlainText()
        print (value)
        utils.wrmsr("0x620", value)

    def core_set_clicked(self):
        print ("Core set")
        # textEdit_CoreWrite
        # wrmsr -a 0x199
        value = self.textEdit_CoreWrite.toPlainText()
        print (value)
        utils.wrmsr("0x199", value)

    def monitor_start(self):
        print ("Monitor start")
        self.label_MonitorStatus.setText("Started")
        self.label_MonitorStatus.setStyleSheet("background-color: yellow; border: 1px solid black;")
        self.timer.start(UPDATE_INTERVAL)
        self.update()

    def monitor_stop(self):
        print ("Monitor stop")
        self.label_MonitorStatus.setText("Stopped")
        self.label_MonitorStatus.setStyleSheet("background-color: red; border: 1px solid black;")

        self.timer.stop()

    def update(self):
        self.update_uncore()
        self.update_core()
        self.update_graph()

    def update_uncore(self):
        result = utils.rdmsr("0x621")
        value = '0x%s' % result[-2:]
        mhz = int(value, 16) * 100
        txt = result + ' (%s Mhz)' % mhz

        self.textEdit_UncoreRead.setPlainText(txt)

        self.uncore_list.append(mhz)
        self.uncore_list = self.uncore_list[1:]

    def update_core(self):
        result = utils.rdmsr("0x198")

        value = '0x%s' % result[-4:-2]
        mhz = int(value, 16) * 100
        txt = result + ' (%s Mhz)' % mhz

        self.textEdit_CoreRead.setPlainText(txt)

        self.core_list.append(mhz)
        self.core_list = self.core_list[1:]

    def init_graph(self):
        graphWidget = pg.PlotWidget(self)

        # plot data: x, y values
        graphWidget.setBackground('w')

        styles = {'color':'r', 'font-size':'15px'}
        graphWidget.setLabel('left', 'Core(Green), Uncore(Blue), Power(Red)', **styles)
        graphWidget.setLabel('bottom', 'Sec', **styles)
        graphWidget.showGrid(x=True, y=True)

        power_pen = pg.mkPen(color=(255, 0, 0), width=2)
        self.power_plot = graphWidget.plot(self.sec_list, self.power_list, pen=power_pen)

        core_pen = pg.mkPen(color=(0, 255, 0), width=2)
        self.core_plot = graphWidget.plot(self.sec_list, self.core_list, pen=core_pen)

        uncore_pen = pg.mkPen(color=(0, 0, 255), width=2)
        self.uncore_plot  = graphWidget.plot(self.sec_list, self.uncore_list, pen=uncore_pen)

        graphWidget.setGeometry(10, 320, 700, 321)
        graphWidget.show()

    def update_graph(self):
        self.core_plot.setData(self.sec_list, self.core_list)
        self.uncore_plot.setData(self.sec_list, self.uncore_list)

    def cmd_clicked(self):
        cmd = self.textEdit_Cmd.toPlainText()
        result = utils.ssh_command(cmd)

        self.textEdit_CmdResult.setPlainText(result)

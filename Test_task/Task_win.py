# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import time
import Task
import analysis_cfg


class k_Taskwindow(Task.Ui_MainWindow):
    def __init__(self,parent=None):
        super(k_Taskwindow,self).__init__()
        self.setupUi(MainWindow)


        #设置tabwidget的宽度

        self.Mapping_tableWidget.setColumnWidth(1,330)

        self.Plugins_tableWidget.setColumnWidth(1,130)

        #实例 配置json脚本
        cfg = analysis_cfg.analysisCfg()

        #将数据填入TableWidget
        Plugins = cfg.analysisPlugins()
        self.setItemToQTableWidget(self.Plugins_tableWidget,Plugins)

        Mapping = cfg.analysisMapping()

        self.setItemToQTableWidget(self.Mapping_tableWidget, Mapping)

        mayaver = cfg.analysisSoft()

        self.Version_lineEdit.setText(mayaver)



    def setItemToQTableWidget(self,QTablename,cfg_dic):
        for Plugin in cfg_dic:
            Plugins_Itemname    = QTableWidgetItem(Plugin)
            Plugins_Itemversion = QTableWidgetItem(cfg_dic[Plugin])

            QTablename.insertRow(0)
            QTablename.setItem(0, 0, Plugins_Itemname)
            QTablename.setItem(0, 1, Plugins_Itemversion)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    kwin = k_Taskwindow()
    #kwin.setWindowTitle(u'测试任务工具')

    MainWindow.show()
    sys.exit(app.exec_())
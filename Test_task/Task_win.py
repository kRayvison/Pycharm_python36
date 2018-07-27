# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import os
import time
import Task
import analysis_cfg
#import QDesktopServices

class k_Taskwindow(Task.Ui_MainWindow):
    def __init__(self,parent=None):
        super(k_Taskwindow,self).__init__()
        self.setupUi(MainWindow)


        #设置tabwidget的宽度

        self.Mapping_tableWidget.setColumnWidth(1,330)

        self.Plugins_tableWidget.setColumnWidth(1,130)

        #实例 配置json脚本
        cfg = analysis_cfg.analysisCfg()

        #填入plugins数据
        Plugins = cfg.analysisPlugins()
        self.setItemToQTableWidget(self.Plugins_tableWidget,Plugins)
        #填入Mapping数据
        Mapping = cfg.analysisMapping()
        self.setItemToQTableWidget(self.Mapping_tableWidget, Mapping)
        #填入maya版本号
        mayaver = cfg.analysisSoft()
        self.Version_lineEdit.setText(mayaver)

        sysPath = cfg.analysisPath()

        self.Close_Button.clicked.connect(self.kclose)
        self.Input_Button.clicked.connect(self.OpenInput)
        self.Output_Button.clicked.connect(self.OpenOutput)

        #self.k_inputPath = sysPath['tiles_path']

        #maya文件目录
        self.k_inputPath = sysPath['input_cg_file']
        self.k_inputPath = os.path.dirname(self.k_inputPath).replace('/','\\')
        print(self.k_inputPath)

        #maya输出图片目录
        self.k_outputPath = sysPath['output_user_path'].replace('/','\\')
        print(self.k_outputPath)

        #maya首选项目录


    #Input按钮功能
    def OpenInput(self):
        #QDesktopServices.openUrl(QUrl(self.k_inputPath))
        os.startfile(self.k_inputPath)

    #Output按钮功能
    def OpenOutput(self):
        os.startfile(self.k_outputPath)

    #Preferences按钮功能
    #def OpenPreferences按钮功能(self):
        #os.startfile(self.k_outputPath)

    #close按钮功能
    def kclose(self):
        #self.close()
        #self.hide()
        app.exit()


    def getData(self):
        #获取Plugins的数据
        getPluginsQtab = self.getItemfromQTableWidget(self.Plugins_tableWidget)
        #print (getPluginsQtab)

        # 获取Mapping的数据
        getMappingQtab = self.getItemfromQTableWidget(self.Mapping_tableWidget)
        #print (getMappingQtab)

        # 获取maya版本数据
        getMayaVer = self.Version_lineEdit.text()
        #print (getMayaVer)


    def getItemfromQTableWidget(self,QTablename):
        #获取行数与列数
        getRow=QTablename.rowCount()
        getcolumn = QTablename.columnCount()
        QTabData = {}
        for row in range(getRow):
            for column in range(getcolumn):
                #获取Qtab内的每个格子的数据
                getText = QTablename.item(row, column).text()
                #将数据放入字典
                QTabData[getText] = (getText if getText in QTabData else '')

        return QTabData

    def setItemToQTableWidget(self,QTablename,cfg_dic):
        for Plugin in cfg_dic:
            #将数据转成 QTableWidgetItem
            Plugins_Itemname    = QTableWidgetItem(Plugin)
            Plugins_Itemversion = QTableWidgetItem(cfg_dic[Plugin])
            #将数据塞入第一行
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
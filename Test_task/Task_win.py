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
import k_mapping

class k_Taskwindow(Task.Ui_MainWindow,QWidget):
    def __init__(self,parent=None):
        super(k_Taskwindow,self).__init__()
        self.setupUi(MainWindow)

        #设置tabwidget的宽度

        self.Mapping_tableWidget.setColumnWidth(1,330)

        self.Plugins_tableWidget.setColumnWidth(1,130)


        #按钮功能设置
        self.Get_Button.clicked.connect(self.kGetcfg)

        self.Mapping_netuse.clicked.connect(self.knetuse)
        self.Mapping_add.clicked.connect(self.setBlankToMappingQTable)
        self.Mapping_reduce.clicked.connect(self.clearMappingQTableItem)

        self.Plugins_add.clicked.connect(self.setBlankToPluginQTable)
        self.Plugins_reduce.clicked.connect(self.clearPluginQTableItem)

        self.Close_Button.clicked.connect(self.kclose)
        self.Input_Button.clicked.connect(self.OpenInput)
        self.Output_Button.clicked.connect(self.OpenOutput)

        #self.k_inputPath = sysPath['tiles_path']



        #maya首选项目录

        #获取窗口的信息
        self.getData()

    def kGetcfg(self):
        #实例 配置json脚本
        cfg = analysis_cfg.analysisCfg()

        #填入plugins数据
        Plugins = cfg.analysisPlugins()
        #print (Plugins)
        self.setItemToQTableWidget(self.Plugins_tableWidget,Plugins)


        #填入Mapping数据
        Mapping = cfg.analysisMapping()
        #print (Mapping)
        self.setItemToQTableWidget(self.Mapping_tableWidget, Mapping)
        #填入maya版本号
        mayaver = cfg.analysisSoft()
        self.Version_lineEdit.setText(mayaver)

        sysPath = cfg.analysisPath()

        #maya文件目录
        self.k_inputPath = sysPath['input_cg_file']
        self.k_inputPath = os.path.dirname(self.k_inputPath).replace('/','\\')
        #print(self.k_inputPath)

        #maya输出图片目录
        self.k_outputPath = sysPath['output_user_path'].replace('/','\\')
        #print(self.k_outputPath)


    def OpenInput(self):
        """ Input按钮功能 """
        #QDesktopServices.openUrl(QUrl(self.k_inputPath))
        if os.path.exists(self.k_inputPath):
            os.startfile(self.k_inputPath)
        else:
            self.msg('%s path is not exists' %self.k_inputPath)

    def OpenOutput(self):
        """ Output按钮功能 """
        if os.path.exists(self.k_outputPath):
            os.startfile(self.k_outputPath)
        else:
            #不存在路径时 弹出窗口
            self.msg('%s path is not exists' %self.k_outputPath)

    #Preferences按钮功能
    #def OpenPreferences按钮功能(self):
        #os.startfile(self.k_outputPath)

    def knetuse(self):
        """根据 mapping的内容 映射盘符"""
        self.getData()
        k_mapping.k_mapping(self.getMappingQtab)



    def kclose(self):
        """close按钮功能"""
        #self.close()
        #self.hide()
        #app.exit()
        self.getData()

    def getData(self):
        """获取窗口内 Plugins Mapping maya版本 的数据"""

        #获取Plugins的数据
        getPluginsQtab = self.getItemfromQTableWidget(self.Plugins_tableWidget)
        print (getPluginsQtab)

        # 获取Mapping的数据
        self.getMappingQtab = self.getItemfromQTableWidget(self.Mapping_tableWidget)
        print (self.getMappingQtab)

        # 获取maya版本数据
        getMayaVer = self.Version_lineEdit.text()
        print (getMayaVer)


    def getItemfromQTableWidget(self,QTablename):
        """获取QTab内每个格子的数据，并组成字典，QTablename输入的数据为QTab的名字"""
        #获取行数与列数
        getRow=QTablename.rowCount()
        getcolumn = QTablename.columnCount()
        QTabData = {}
        for row in range(getRow):
            # 获取Qtab内的每个格子的数据
            for column in range(getcolumn):
                #先判断格子是否为空
                if QTablename.item(row, column):
                    getText = QTablename.item(row, column).text()
                    #print (getText)

                    #将数据放入字典
                    if not column and getText:
                        QTabData[getText] = ''
                    elif column == 1:
                        # 先判断格子是否为空
                        if QTablename.item(row, column-1):
                            getText_key = QTablename.item(row, column-1).text()
                            QTabData[getText_key] = getText

        return QTabData

    def setItemToQTableWidget(self,QTablename,cfg_dic):
        """为QTab的第一行加入数据，QTablename=QTab的名称，cfg_dic=数据字典 key=column 0 value=column 1"""
        for Plugin in cfg_dic:
            #将数据转成 QTableWidgetItem
            Plugins_Itemname    = QTableWidgetItem(Plugin)
            Plugins_Itemversion = QTableWidgetItem(cfg_dic[Plugin].replace('/','\\'))
            #将数据塞入第一行
            QTablename.insertRow(0)
            QTablename.setItem(0, 0, Plugins_Itemname)
            QTablename.setItem(0, 1, Plugins_Itemversion)
            #选择的时候 选择一整行
            QTablename.setSelectionBehavior(QAbstractItemView.SelectRows)

    def setBlankToMappingQTable(self):
        """加入空白行"""
        self.Mapping_tableWidget.insertRow(0)
        #选择的时候 选择一整行
        self.Mapping_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def clearMappingQTableItem(self):
        #self.k_tabWidget.clearContents()
        krow=self.Mapping_tableWidget.currentRow()
        self.Mapping_tableWidget.removeRow(krow)

    def setBlankToPluginQTable(self):
        """加入空白行"""
        self.Plugins_tableWidget.insertRow(0)
        #选择的时候 选择一整行
        self.Plugins_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def clearPluginQTableItem(self):
        #self.k_tabWidget.clearContents()
        krow=self.Plugins_tableWidget.currentRow()
        self.Plugins_tableWidget.removeRow(krow)

    def msg(self,message):
        kMessage = QMessageBox.information(self,  # 使用infomation信息框
                                        "出问题啦，请注意！！！",
                                        message,
                                        QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    kwin = k_Taskwindow()
    #kwin.setWindowTitle(u'测试任务工具')

    MainWindow.show()
    sys.exit(app.exec_())
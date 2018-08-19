# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Task.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(567, 675)
        MainWindow.setStatusTip("")
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("/* === Shared === */\n"
"* {\n"
"    background-color: #333333;\n"
"    color: #BBBBBB;\n"
"    font-family: \"Segoe UI\";\n"
"}\n"
"\n"
"/* === QWidget === */\n"
"QWidget:window {\n"
"    background: #333333;\n"
"    color: #BBBBBB;\n"
"    font-family: \"Segoe UI\";\n"
"\n"
"}\n"
"\n"
"/* === QPushButton === */\n"
"QPushButton {\n"
"    border: 1px solid #4f4f4f;\n"
"    padding: 4px;\n"
"    min-width: 65px;\n"
"    min-height: 12px;\n"
"\n"
"}\n"
"\n"
"\n"
"/* =================== */\n"
"QLineEdit, QListView, QTreeView, QTableView, QAbstractSpinBox {\n"
"    background-color: rgb(66, 66, 66);\n"
"    color: #000;\n"
"    border: 1px solid #555;\n"
"}\n"
"\n"
"QAbstractScrollArea, QLineEdit, QTextEdit, QAbstractSpinBox, QComboBox {\n"
"    border: 1px solid #555;\n"
"    color:rgb(200, 200, 200);\n"
"}\n"
"\n"
"/* === QHeaderView === */\n"
"QHeaderView::section {\n"
"    height: 20px;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background: rgb(55, 55, 55);\n"
"    border: 0;\n"
"    /*字体颜色*/\n"
"    color: rgb(200, 200, 200);\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"QTableWidget{\n"
"    background: rgb(55, 55, 55);\n"
"    selection-background-color: rgb(77, 77, 77);\n"
"    font-family: \"Segoe UI\";\n"
"\n"
"}\n"
"")
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ID_horizontalLayout = QtWidgets.QHBoxLayout()
        self.ID_horizontalLayout.setContentsMargins(-1, 10, -1, -1)
        self.ID_horizontalLayout.setObjectName("ID_horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ID_horizontalLayout.addItem(spacerItem)
        self.TaskID = QtWidgets.QLabel(self.centralwidget)
        self.TaskID.setMaximumSize(QtCore.QSize(50, 25))
        self.TaskID.setObjectName("TaskID")
        self.ID_horizontalLayout.addWidget(self.TaskID)
        self.TaskID_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.TaskID_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.TaskID_lineEdit.setObjectName("TaskID_lineEdit")
        self.ID_horizontalLayout.addWidget(self.TaskID_lineEdit)
        self.UserID = QtWidgets.QLabel(self.centralwidget)
        self.UserID.setMaximumSize(QtCore.QSize(50, 25))
        self.UserID.setObjectName("UserID")
        self.ID_horizontalLayout.addWidget(self.UserID)
        self.UserID_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.UserID_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.UserID_lineEdit.setObjectName("UserID_lineEdit")
        self.ID_horizontalLayout.addWidget(self.UserID_lineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ID_horizontalLayout.addItem(spacerItem1)
        self.Get_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Get_Button.setMinimumSize(QtCore.QSize(75, 22))
        self.Get_Button.setMaximumSize(QtCore.QSize(60, 25))
        self.Get_Button.setObjectName("Get_Button")
        self.ID_horizontalLayout.addWidget(self.Get_Button)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.ID_horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.ID_horizontalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.maya_horizontalLayout = QtWidgets.QHBoxLayout()
        self.maya_horizontalLayout.setContentsMargins(-1, 5, -1, -1)
        self.maya_horizontalLayout.setSpacing(6)
        self.maya_horizontalLayout.setObjectName("maya_horizontalLayout")
        self.Maya_label = QtWidgets.QLabel(self.centralwidget)
        self.Maya_label.setMinimumSize(QtCore.QSize(0, 25))
        self.Maya_label.setObjectName("Maya_label")
        self.maya_horizontalLayout.addWidget(self.Maya_label)
        self.Version_label = QtWidgets.QLabel(self.centralwidget)
        self.Version_label.setMinimumSize(QtCore.QSize(0, 25))
        self.Version_label.setObjectName("Version_label")
        self.maya_horizontalLayout.addWidget(self.Version_label)
        self.Version_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Version_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.Version_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.Version_lineEdit.setText("")
        self.Version_lineEdit.setObjectName("Version_lineEdit")
        self.maya_horizontalLayout.addWidget(self.Version_lineEdit)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.maya_horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.maya_horizontalLayout)
        self.Plugins_horizontalLayout = QtWidgets.QHBoxLayout()
        self.Plugins_horizontalLayout.setContentsMargins(-1, 5, -1, -1)
        self.Plugins_horizontalLayout.setObjectName("Plugins_horizontalLayout")
        self.Plugins_verticalLayout = QtWidgets.QVBoxLayout()
        self.Plugins_verticalLayout.setContentsMargins(-1, -1, 10, -1)
        self.Plugins_verticalLayout.setObjectName("Plugins_verticalLayout")
        self.Plugins_label = QtWidgets.QLabel(self.centralwidget)
        self.Plugins_label.setObjectName("Plugins_label")
        self.Plugins_verticalLayout.addWidget(self.Plugins_label)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.Plugins_verticalLayout.addItem(spacerItem4)
        self.Plugins_horizontalLayout.addLayout(self.Plugins_verticalLayout)
        self.Plugins_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.Plugins_tableWidget.setStyleSheet("")
        self.Plugins_tableWidget.setObjectName("Plugins_tableWidget")
        self.Plugins_tableWidget.setColumnCount(2)
        self.Plugins_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Plugins_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Plugins_tableWidget.setHorizontalHeaderItem(1, item)
        self.Plugins_horizontalLayout.addWidget(self.Plugins_tableWidget)
        self.Plugins_verticalLayout2 = QtWidgets.QVBoxLayout()
        self.Plugins_verticalLayout2.setObjectName("Plugins_verticalLayout2")
        self.Plugins_add = QtWidgets.QPushButton(self.centralwidget)
        self.Plugins_add.setObjectName("Plugins_add")
        self.Plugins_verticalLayout2.addWidget(self.Plugins_add)
        self.Plugins_reduce = QtWidgets.QPushButton(self.centralwidget)
        self.Plugins_reduce.setObjectName("Plugins_reduce")
        self.Plugins_verticalLayout2.addWidget(self.Plugins_reduce)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.Plugins_verticalLayout2.addItem(spacerItem5)
        self.Plugins_horizontalLayout.addLayout(self.Plugins_verticalLayout2)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Plugins_horizontalLayout.addItem(spacerItem6)
        self.verticalLayout_3.addLayout(self.Plugins_horizontalLayout)
        self.Mapping_verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.Mapping_verticalLayout_2.setObjectName("Mapping_verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Mapping_verticalLayout = QtWidgets.QVBoxLayout()
        self.Mapping_verticalLayout.setObjectName("Mapping_verticalLayout")
        self.Mapping_label = QtWidgets.QLabel(self.centralwidget)
        self.Mapping_label.setObjectName("Mapping_label")
        self.Mapping_verticalLayout.addWidget(self.Mapping_label)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.Mapping_verticalLayout.addItem(spacerItem7)
        self.horizontalLayout_2.addLayout(self.Mapping_verticalLayout)
        self.Mapping_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.Mapping_tableWidget.setObjectName("Mapping_tableWidget")
        self.Mapping_tableWidget.setColumnCount(2)
        self.Mapping_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Mapping_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Mapping_tableWidget.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_2.addWidget(self.Mapping_tableWidget)
        self.Mapping_verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem8 = QtWidgets.QSpacerItem(65, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.Mapping_add = QtWidgets.QPushButton(self.centralwidget)
        self.Mapping_add.setMinimumSize(QtCore.QSize(40, 22))
        self.Mapping_add.setMaximumSize(QtCore.QSize(40, 22))
        self.Mapping_add.setSizeIncrement(QtCore.QSize(0, 0))
        self.Mapping_add.setObjectName("Mapping_add")
        self.horizontalLayout.addWidget(self.Mapping_add)
        spacerItem9 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.Mapping_reduce = QtWidgets.QPushButton(self.centralwidget)
        self.Mapping_reduce.setEnabled(True)
        self.Mapping_reduce.setMinimumSize(QtCore.QSize(40, 22))
        self.Mapping_reduce.setMaximumSize(QtCore.QSize(40, 22))
        self.Mapping_reduce.setObjectName("Mapping_reduce")
        self.horizontalLayout.addWidget(self.Mapping_reduce)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem10)
        self.Mapping_netuse = QtWidgets.QPushButton(self.centralwidget)
        self.Mapping_netuse.setMinimumSize(QtCore.QSize(75, 22))
        self.Mapping_netuse.setSizeIncrement(QtCore.QSize(0, 0))
        self.Mapping_netuse.setBaseSize(QtCore.QSize(0, 0))
        self.Mapping_netuse.setObjectName("Mapping_netuse")
        self.horizontalLayout.addWidget(self.Mapping_netuse)
        self.Mapping_verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.Mapping_verticalLayout_2)
        self.path_horizontalLayout = QtWidgets.QHBoxLayout()
        self.path_horizontalLayout.setContentsMargins(-1, 5, -1, -1)
        self.path_horizontalLayout.setObjectName("path_horizontalLayout")
        self.Input_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Input_Button.setMinimumSize(QtCore.QSize(75, 22))
        self.Input_Button.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Input_Button.setObjectName("Input_Button")
        self.path_horizontalLayout.addWidget(self.Input_Button)
        self.Output_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Output_Button.setMinimumSize(QtCore.QSize(75, 22))
        self.Output_Button.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Output_Button.setObjectName("Output_Button")
        self.path_horizontalLayout.addWidget(self.Output_Button)
        self.Preferences_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Preferences_Button.setMinimumSize(QtCore.QSize(75, 22))
        self.Preferences_Button.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Preferences_Button.setObjectName("Preferences_Button")
        self.path_horizontalLayout.addWidget(self.Preferences_Button)
        self.PreRender_Button = QtWidgets.QPushButton(self.centralwidget)
        self.PreRender_Button.setMinimumSize(QtCore.QSize(75, 22))
        self.PreRender_Button.setMaximumSize(QtCore.QSize(120, 16777215))
        self.PreRender_Button.setObjectName("PreRender_Button")
        self.path_horizontalLayout.addWidget(self.PreRender_Button)
        self.verticalLayout_3.addLayout(self.path_horizontalLayout)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem11)
        self.execute_horizontalLayout = QtWidgets.QHBoxLayout()
        self.execute_horizontalLayout.setContentsMargins(-1, 5, -1, -1)
        self.execute_horizontalLayout.setObjectName("execute_horizontalLayout")
        self.Maya_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Maya_Button.setMinimumSize(QtCore.QSize(75, 22))
        self.Maya_Button.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Maya_Button.setObjectName("Maya_Button")
        self.execute_horizontalLayout.addWidget(self.Maya_Button)
        self.CMD_Button = QtWidgets.QPushButton(self.centralwidget)
        self.CMD_Button.setMinimumSize(QtCore.QSize(75, 22))
        self.CMD_Button.setMaximumSize(QtCore.QSize(120, 16777215))
        self.CMD_Button.setObjectName("CMD_Button")
        self.execute_horizontalLayout.addWidget(self.CMD_Button)
        self.Close_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Close_Button.setMinimumSize(QtCore.QSize(75, 22))
        self.Close_Button.setMaximumSize(QtCore.QSize(120, 16777215))
        self.Close_Button.setObjectName("Close_Button")
        self.execute_horizontalLayout.addWidget(self.Close_Button)
        self.verticalLayout_3.addLayout(self.execute_horizontalLayout)
        self.line.raise_()
        self.Mapping_add.raise_()
        self.Mapping_reduce.raise_()
        self.Mapping_netuse.raise_()
        self.Mapping_tableWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 567, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TaskID.setText(_translate("MainWindow", "Task ID"))
        self.UserID.setText(_translate("MainWindow", "User ID"))
        self.Get_Button.setText(_translate("MainWindow", "Get"))
        self.Maya_label.setText(_translate("MainWindow", "  Maya    :"))
        self.Version_label.setText(_translate("MainWindow", "version "))
        self.Plugins_label.setText(_translate("MainWindow", " Plugins  :"))
        item = self.Plugins_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.Plugins_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Version"))
        self.Plugins_add.setText(_translate("MainWindow", "+"))
        self.Plugins_reduce.setText(_translate("MainWindow", "-"))
        self.Mapping_label.setText(_translate("MainWindow", " Mapping  :"))
        item = self.Mapping_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Drive"))
        item = self.Mapping_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Folder"))
        self.Mapping_add.setText(_translate("MainWindow", "+"))
        self.Mapping_reduce.setText(_translate("MainWindow", "-"))
        self.Mapping_netuse.setText(_translate("MainWindow", "net use"))
        self.Input_Button.setText(_translate("MainWindow", "Input"))
        self.Output_Button.setText(_translate("MainWindow", "Output"))
        self.Preferences_Button.setText(_translate("MainWindow", "Preferences"))
        self.PreRender_Button.setText(_translate("MainWindow", "PreRender"))
        self.Maya_Button.setText(_translate("MainWindow", "Maya"))
        self.CMD_Button.setText(_translate("MainWindow", "CMD"))
        self.Close_Button.setText(_translate("MainWindow", "Close"))


# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#from k_frist2 import *
import k_frist4
import shoudong_win
import sys
import time
import ctypes  

class k_Cthread(QThread):
    #信号变量
    k_processed = pyqtSignal(int)
    k_finished = pyqtSignal()

    def __init__(self,parent = None):
        super(k_Cthread, self).__init__(parent)

    #Qthread的star执行命令
    def run (self):
        #print ("start k .....run")
        #执行的方法
        self.k_progress()

    #执行的内容
    def k_progress(self):
        #关联k_window的内容
        parent = self.parent()

        #设置进度条属性
        parent.k_progressBar.setValue(0)
        parent.kmaxCount = parent.k_tabWidget.rowCount()
        parent.k_progressBar.setMinimum (0)
        parent.k_progressBar.setMaximum (parent.kmaxCount)
        #执行k_startT（）
        parent.k_startT()


        for i in range(parent.kmaxCount):
            parent.k_tabWidget.removeRow(0)
            time.sleep(0.1)
            self.k_processed.emit(i +1)
        self.k_finished.emit()


class k_window(QWidget,k_frist4.Ui_k_widget):
    def __init__(self,parent=None):
        super(k_window,self).__init__()
        self.setupUi(self)
        
        #设置可以拖入文件
        self.setAcceptDrops(True)

        #多线程实例化
        self.kextraThread = QThread()

        #设置k_window为k_Cthread的爸爸
        self.kthread = k_Cthread(self)

        #启用多线程
        self.kthread2 = k_Cthread()
        self.kthread2.moveToThread(self.kextraThread)


        #添加Button
        self.k_Bopen.setDefault(True)
        go_button = QPushButton(u'手动添加')
        self.k_progressBar.setValue(0)

        #布局里添加控件
        self.k_wlayout.addWidget(go_button)
        
        #控件联接方法
        go_button.clicked.connect(self.sd_win)
        self.k_button2.clicked.connect(self.cleartabItem)
        self.k_Bopen.clicked.connect(self.kop)
        self.k_Bclose.clicked.connect(self.kcl)
        #self.k_convert.clicked.connect(self.startProgress)

        krow=self.k_tabWidget.currentRow()
        #self.k_tabWidget.itemClicked.connect(self.cleartabItem)

        #设置window的选择目录
        cde = QFileSystemModel()
        cde.setRootPath(QDir.homePath())
        self.k_treeView.setModel(cde)

        #设置tabwidget的宽度
        self.k_tabWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.k_tabWidget.setColumnWidth(0,140)
        self.k_tabWidget.setColumnWidth(1,340)
        self.k_tabWidget.setColumnWidth(2,90)

        self.k_convert.clicked.connect(self.kthread.start)
        self.kthread.k_processed.connect(self.k_progressBar.setValue)
        self.kthread.k_finished.connect(self.k_finishedT)    

        #设置控件
        self.k_progressBar.hide()
        #self.kextraThread.started.connect(self.kthread.k_progress)

        #添加主程序图标
        self.ktabicon = QIcon()
        self.ktabicon.addPixmap(QPixmap("icon/floatComposite.png"),QIcon.Normal,QIcon.Off)
        self.setWindowIcon(self.ktabicon)
        #让window任务栏图标跟随主程序图标
        #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID()

        #添加托盘功能
        self.ktuopan = QSystemTrayIcon(self)
        #添加托盘图标
        self.ktuopanicon = QIcon("icon/floatComposite.png")
        self.ktuopan.setIcon(self.ktuopanicon)
        #托盘添加点击功能
        self.ktuopan.activated.connect(self.ktuopan_click)
        self.ktuopan.show()
        #托盘提示功能
        self.ktuopan.showMessage(u"托盘",u"启动成功！")
        #托盘右键弹出菜单
        self.k_Menu()

    #托盘单击改成双击
    def ktuopan_click(self,double_click):
        if double_click == QSystemTrayIcon.DoubleClick:
            self.show()


    def k_Menu(self):
        #鼠标移动到图标上面提示的语句
        self.ktuopan.setToolTip(u"测试托盘")
        #添加菜单栏
        self.kMenuTeam = QMenu(self)
        self.one = self.kMenuTeam.addAction(QIcon('icon/bullet_selectSolverNode.png'),u'kone')
        self.two = self.kMenuTeam.addAction(QIcon('icon/bullet_selectSolverNode.png'),u'ktwo')
        self.three = self.kMenuTeam.addAction(QIcon('icon/bullet_selectSolverNode.png'),u'第三个')
        #华丽的分割线
        self.kMenuTeam.addSeparator()
        self.kquit = self.kMenuTeam.addAction(QIcon('icon/bullet_interactivePlayback.png'),u'退出')
        self.kquit.triggered.connect(qApp.quit)
        #设置托盘
        self.ktuopan.setContextMenu(self.kMenuTeam)

    #设置关闭事件（右上角X按钮）
    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, u'提示',u'确定退出程序？',QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()
            self.hide()

    def k_startT(self):
        self.k_progressBar.setValue(0)
        self.k_convert.setDisabled(True)
        #self.btnCancel.setEnabled(True)
        self.k_progressBar.show()
        #print  'starting k....thread'
        #self.kextraThread.start()

    def k_finishedT(self):
        print  ('finished k....thread')
        #self.btnCancel.setDisabled(True)
        self.k_convert.setEnabled(True)
        # self.extraThread.deleteLater()
        # self.worker.deleteLater()
        self.kextraThread.quit()
        self.k_progressBar.hide()

    # 设置快捷键 按Delete删除tabwidget里的东西
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            self.cleartabItem()


    #手动添加tab元素的方法
    def sd_win(self):


        self.sdwin=shoudong_win()
        self.sdwin.exec_()

        k_ffname=self.sdwin.klinename.text()
        k_ffpath=self.sdwin.klinepath.text()
        k_ffsize=self.sdwin.klinesize.text()

        if k_ffname and k_ffpath:
            kItemname=QTableWidgetItem(k_ffname)
            kItempath=QTableWidgetItem(k_ffpath)
            kItemsize=QTableWidgetItem(str(k_ffsize))

            self.k_tabWidget.insertRow(0)
            self.k_tabWidget.setItem(0,0,kItemname)
            self.k_tabWidget.setItem(0,1,kItempath)
            self.k_tabWidget.setItem(0,2,kItemsize)


    #设置拖拽东西进widget的事件
    def dragEnterEvent(self,event):
        event.acceptProposedAction()
    #设置拖拽放松时的事件
    def dropEvent(self,event):
        #super(k_window,self).dropEvent(event)
        #print("file droping")
        mimeData = event.mimeData()
        files=[]
        for url in mimeData.urls():
            #print  url.toLocalFile()
            files.append(url.toLocalFile())
            
        
        self.k_getfile(files)


    # 打开按钮的设置
    def kop(self):
        k_files=QFileDialog.getOpenFileNames(self,caption=u'选择文件',\
        filter="Pyhon(*.py;*pyc);;TXT(*.txt)",options=0)

        self.k_getfile(k_files[0])

        #print k_files
        #print type(k_files)

        #for k_file in k_files[0]:
            
            #将字符串转换成QT的info格式
            #fileInfo=QFileInfo(k_file)

            #获取 不带后缀的文件名
            #k_fname = fileInfo.completeBaseName()
            #print k_fname
            #获取 纯路径
            #k_fpath = fileInfo.path()
            #print k_fpath
            #测试是否为文件
            #aaa=fileInfo.isFile()
            #print aaa
            #
            #获取带后缀的文件名
            #k_ffname = fileInfo.fileName()
            #print k_ffname   
            #获取带文件名及后缀的路径
            #k_ffpath = fileInfo.path()
            #print k_ffpath   
            #获取文件最后一次读取的时间
            #k_flastRead = fileInfo.lastRead()
            #print k_flastRead 
            #k_ffsize = fileInfo.size()/1024./1024.
            #print k_ffsize             
            #k_ffsize = '{:.3f}M'.format(k_ffsize)


            #kItemname=QTableWidgetItem(k_ffname)
            #kItempath=QTableWidgetItem(k_ffpath)
            #kItemsize=QTableWidgetItem(str(k_ffsize))

            #self.k_tabWidget.insertRow(0)
            #self.k_tabWidget.setItem(0,0,kItemname)
            #self.k_tabWidget.setItem(0,1,kItempath)
            #self.k_tabWidget.setItem(0,2,kItemsize)
            
    # 设置获取文件的属性分类 
    def k_getfile(self,kfiles):
        for kfile in kfiles:
            fileInfo= QFileInfo(kfile)
            k_fname = fileInfo.fileName()
            k_fpath = fileInfo.path()
            k_fsize = fileInfo.size()
            ks = len(str(k_fsize))
            if ks > 9:
                k_fsize=k_fsize/1024./1024./1024.
                k_fsize = '{:.2f}G'.format(k_fsize)
            elif ks > 6:
                k_fsize=k_fsize/1024./1024.
                k_fsize = '{:.2f}M'.format(k_fsize)   
            elif ks > 3:
                k_fsize=k_fsize/1024.
                k_fsize = '{:.2f}k'.format(k_fsize)   
            else :
                k_fsize = '{:.2f}b'.format(k_fsize) 

            kItemname=QTableWidgetItem(k_fname)
            kItempath=QTableWidgetItem(k_fpath)
            kItemsize=QTableWidgetItem(str(k_fsize))

            self.k_tabWidget.insertRow(0)
            self.k_tabWidget.setItem(0,0,kItemname)
            self.k_tabWidget.setItem(0,1,kItempath)
            self.k_tabWidget.setItem(0,2,kItemsize)

    # 删除tab里的元素
    def cleartabItem(self):
        #self.k_tabWidget.clearContents()
        krow=self.k_tabWidget.currentRow()
        self.k_tabWidget.removeRow(krow)
    # 退出窗口按键
    def kcl(self):
        #self.close()
        self.hide()
        #app.exit()



class shoudong_win(QDialog,shoudong_win.Ui_Dialog):
    def __init__(self,parent=None):
         super(shoudong_win,self).__init__()
         self.setupUi(self)
         self.setAcceptDrops(True)





app = QApplication(sys.argv)
kwin = k_window()
#kwin.setMinimumSize(500,500)
#kwin.setMaximumSize(1300,900)

kwin.setWindowTitle(u'我是来做测试的')

#kwin.show()
print ('aaaaaa')

app.exec_()




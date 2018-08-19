# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.myButton = QtWidgets.QPushButton(self)

        self.myButton.clicked.connect(self.msg)
        self.msg()
    def msg(self):
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        "标题",
                                        "消息",
                                        QMessageBox.Yes | QMessageBox.No)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())    
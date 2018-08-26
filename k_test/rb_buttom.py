from PyQt5.QtWidgets import QApplication, QRadioButton
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class RadioButton(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Check')

        self.rb = QRadioButton('Show title', self)
        self.rb.setFocusPolicy(Qt.NoFocus)

        self.rb.move(10, 10)
        self.rb.toggle()
        self.rb.toggled.connect(self.changeTitle)

    def changeTitle(self, value):
        if self.rb.isChecked():
            self.setWindowTitle('Check')
        else:
            self.setWindowTitle('unchecked')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    qb = RadioButton()
    qb.show()
    sys.exit(app.exec_())
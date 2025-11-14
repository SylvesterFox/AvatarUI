# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QColorDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.setWindowTitle("webst")

        self.ui.colorPick.clicked.connect(self.choose_color)
        self.ui.frameColor.setStyleSheet("background-color: #000000;")
        self.ui.lineEdit.setReadOnly(True)
        self.ui.lineEdit.setText("Loading..")

    def choose_color(self):
        color = QColorDialog.getColor(parent=self, title="Выбрать цвет")
        if color.isValid():
            self.ui.colorHex.setText(f"{color.name()}")
            self.ui.frameColor.setStyleSheet(f"background-color: {color.name()};")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())

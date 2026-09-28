from PySide6.QtWidgets import (
                               QWidget, QApplication, QGridLayout,
                               QVBoxLayout, QHBoxLayout, QFrame,
                               QPushButton, QLabel
                               )
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication
import re

class Custom_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(630, 700)
        self.layout = QVBoxLayout(self)
        self.type_text = QLabel("",
        alignment = Qt.AlignmentFlag.AlignBottom |
        Qt.AlignmentFlag.AlignRight
        )
        self.type_text.setMinimumHeight(100)
        self.type_text.setStyleSheet("font-size: 30px;") 
        self.layout.addWidget(self.type_text)
        self.move_center()

    def move_center(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = screen.width() / 2 - self.width() / 2
        y = screen.height() / 2 - self.height() / 2
        self.move(int(x), int(y))


class Buttons():
    def __init__(self, window, label):
        self.label = label
        self.window = window
        self.layout_all_buttons = QGridLayout()
        self.buttons = []
        all_buttons = [
        "Exit","Narek","Mardoyan","Delete",
        "1","2","3","+"
        ,"4","5","6","-"
        ,"7","8","9","*"
        ,".","0","=","/"
        ]
        clear_button = ["Clear"]

        for y in range(0, 5):
            for x in range(0, 4):
                button = QPushButton(all_buttons[y * 4 + x])
                button.setFixedSize(150, 50)
                button.clicked.connect(
                lambda checked=False, b=button:
                self.add_to_display(b.text())
                )
                self.buttons.append(button)
                self.layout_all_buttons.addWidget(button, y + 1, x)
        else:
            button = QPushButton(clear_button[0])
            button.setFixedSize(630, 50)
            button.clicked.connect(
                self.clearing
            )
            self.buttons.append(button)
            self.layout_all_buttons.addWidget(button, 0, 0)

    def clearing(self):
        self.label.setText("")
        return

    def add_to_display(self, text):
        if text == "Delete":
            self.label.setText(self.label.text()[:-1])
            return

        if text == "Exit":
            self.window.close()
            return

        if text == "Narek" or text == "Mardoyan":
            return

        if self.label.text() == "" and text in "+-*/=":
            return
       
        if self.label.text() and self.label.text()[-1] in "+-*/" and text in "+-*/=":
            return

        if self.label.text() and self.label.text()[-1] in "." and text in "+-*/=":
            return

        if text == "=":
            try:
                expression = self.label.text()
                expression = re.sub(r'(?<![\d.])0+(\d+)', r'\1', expression)
                result = eval(expression)

            except ZeroDivisionError:
                self.label.setText("=              You Can't Divide By Zero           ")
                result = None

            if result == None:
                QTimer.singleShot(1500, self.clearing)
            elif isinstance(result, int):
                self.label.setText(str(result))
                return
            elif result.is_integer():
                self.label.setText(str(int(result)))
                return
            else:
                self.label.setText(str(result))
                return

        self.label.setText(
            self.label.text() + text
        )

class Visual:
    def __init__(self):
        self.cw = Custom_Window()
        self.b = Buttons(self.cw, self.cw.type_text)
        self.cw.layout.addLayout(self.b.layout_all_buttons)
        self.cw.show()

if __name__ == "__main__":
    app = QApplication()
    v = Visual()
    app.exec()

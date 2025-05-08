import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone 스타일 계산기')
        self.setFixedSize(320, 550)  # 아이폰 스타일 크기
        self.setStyleSheet("background-color: #000000;")  # 배경 검정색
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # 디스플레이 설정
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(100)
        self.display.setStyleSheet("""
            color: #FFFFFF;
            background-color: #000000;
            border: none;
            padding-right: 20px;
            font-size: 48px;
        """)
        self.display.setFont(QFont('Helvetica', 48, QFont.Bold))
        self.layout.addWidget(self.display)
        self.layout.addStretch(1)

        # 버튼 생성
        buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        grid = QGridLayout()
        grid.setSpacing(10)

        for row_idx, row in enumerate(buttons):
            col_offset = 0
            for col_idx, text in enumerate(row):
                if text == '0':
                    button = QPushButton(text)
                    button.setFixedSize(150, 70)
                    grid.addWidget(button, row_idx + 1, col_idx, 1, 2)
                    col_offset = 1  # 다음 버튼 위치 보정
                elif text == '.':
                    button = QPushButton(text)
                    button.setFixedSize(70, 70)
                    grid.addWidget(button, row_idx + 1, col_idx + col_offset)
                else:
                    button = QPushButton(text)
                    button.setFixedSize(70, 70)
                    grid.addWidget(button, row_idx + 1, col_idx)

                button.setFont(QFont('Helvetica', 24, QFont.Bold))
                button.setStyleSheet(self.get_button_style(text))
                button.clicked.connect(self.on_button_clicked)

        self.layout.addLayout(grid)
        self.layout.setContentsMargins(10, 10, 10, 20)
        self.setLayout(self.layout)

    def get_button_style(self, text):
        base_style = """
            border-radius: 35px;
            border: none;
        """
        if text in ['AC', '+/-', '%']:
            return base_style + """
                background-color: #A5A5A5;
                color: #000000;
                font-size: 22px;
            """
        elif text in ['/', '*', '-', '+', '=']:
            return base_style + """
                background-color: #F5A623;
                color: #FFFFFF;
                font-size: 28px;
            """
        else:
            return base_style + """
                background-color: #333333;
                color: #FFFFFF;
                font-size: 24px;
            """

    def on_button_clicked(self):
        sender = self.sender()
        text = sender.text()

        if text == 'AC':
            self.display.setText('')
        elif text == '=':
            try:
                result = str(eval(self.display.text().replace('×', '*').replace('÷', '/')))
                self.display.setText(result)
            except Exception:
                self.display.setText('Error')
        elif text == '+/-':
            current = self.display.text()
            if current.startswith('-'):
                self.display.setText(current[1:])
            elif current:
                self.display.setText('-' + current)
        else:
            self.display.setText(self.display.text() + text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())

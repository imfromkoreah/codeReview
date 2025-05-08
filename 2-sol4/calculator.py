import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QGridLayout, QLineEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_input = '0'
        self.last_result = None
        self.last_operator = None
        self.new_input = True

    def input_number(self, num):
        if self.new_input:
            self.current_input = num
            self.new_input = False
        else:
            if self.current_input == '0' and num != '.':
                self.current_input = num
            else:
                self.current_input += num

    def input_dot(self):
        if '.' not in self.current_input:
            self.current_input += '.'
            self.new_input = False

    def set_operator(self, operator):
        if self.last_operator:
            self.equal()
        self.last_result = float(self.current_input)
        self.last_operator = operator
        self.new_input = True

    def add(self): self.set_operator('+')
    def subtract(self): self.set_operator('-')
    def multiply(self): self.set_operator('*')
    def divide(self): self.set_operator('/')

    def equal(self):
        if self.last_operator is None or self.last_result is None:
            return
        try:
            current = float(self.current_input)
            result = None
            if self.last_operator == '+':
                result = self.last_result + current
            elif self.last_operator == '-':
                result = self.last_result - current
            elif self.last_operator == '*':
                result = self.last_result * current
            elif self.last_operator == '/':
                if current == 0:
                    self.current_input = 'Error'
                    self.last_result = None
                    self.last_operator = None
                    return
                result = self.last_result / current
            result = round(result, 6)
            self.current_input = str(result)
        except:
            self.current_input = 'Error'
        self.last_operator = None
        self.last_result = None
        self.new_input = True

    def negative_positive(self):
        if self.current_input.startswith('-'):
            self.current_input = self.current_input[1:]
        else:
            if self.current_input != '0':
                self.current_input = '-' + self.current_input

    def percent(self):
        try:
            value = float(self.current_input)
            value = value / 100
            self.current_input = str(round(value, 6))
        except:
            self.current_input = 'Error'
        self.new_input = True

    def get_display(self):
        return self.current_input

class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('iPhone 스타일 계산기')
        self.setFixedSize(320, 550)  # 아이폰 비율에 더 가까운 크기
        self.setStyleSheet("background-color: #000000;")
        self.calculator = Calculator()
        self.create_ui()

    def create_ui(self):
        # 디스플레이 설정
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setFixedHeight(100)  # 더 큰 디스플레이 영역
        self.display.setStyleSheet("""
            color: #FFFFFF; 
            background-color: #000000; 
            border: none; 
            padding-right: 20px;
            font-size: 48px;  /* 더 큰 폰트 크기 */
        """)
        self.display.setFont(QFont('Helvetica', 48, QFont.Bold))  # Helvetica로 아이폰 느낌
        self.display.setText(self.calculator.get_display())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)
        main_layout.addStretch(1)  # 디주변 여백

        # 버튼 그리드
        grid = QGridLayout()
        grid.setSpacing(10)  # 버튼 간 간격
        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3),
        ]

        for item in buttons:
            if len(item) == 3:
                text, row, col = item
                rowspan, colspan = 1, 1
            else:
                text, row, col, rowspan, colspan = item

            btn = QPushButton(text)
            btn.setFixedSize(70, 70)  # 정사각형 버튼
            if text == '0':
                btn.setFixedSize(150, 70)  # 0 버튼은 가로로 길게
            btn.setFont(QFont('Helvetica', 24, QFont.Bold))
            btn.setStyleSheet(self.get_button_style(text))
            grid.addWidget(btn, row, col, rowspan, colspan, alignment=Qt.AlignCenter)
            btn.clicked.connect(self.create_handler(text))

        main_layout.addLayout(grid)
        main_layout.setContentsMargins(10, 10, 10, 20)  # 전체 레이아웃 여백
        self.setLayout(main_layout)

    def get_button_style(self, text):
        base_style = """
            border-radius: 35px;  /* 완벽한 원형 버튼 */
            border: none;
        """
        if text in ['C', '±', '%']:
            return base_style + """
                background-color: #A5A5A5; 
                color: #000000;
                font-size: 22px;
            """
        elif text in ['÷', '×', '-', '+', '=']:
            return base_style + """
                background-color: #F5A623;  /* 아이폰 주황색 */
                color: #FFFFFF;
                font-size: 28px;
            """
        else:
            return base_style + """
                background-color: #333333; 
                color: #FFFFFF;
                font-size: 24px;
            """

    def create_handler(self, text):
        def handler():
            if text == 'C':
                self.calculator.reset()
            elif text == '±':
                self.calculator.negative_positive()
            elif text == '%':
                self.calculator.percent()
            elif text in '0123456789':
                self.calculator.input_number(text)
            elif text == '.':
                self.calculator.input_dot()
            elif text == '+':
                self.calculator.add()
            elif text == '-':
                self.calculator.subtract()
            elif text == '×':
                self.calculator.multiply()
            elif text == '÷':
                self.calculator.divide()
            elif text == '=':
                self.calculator.equal()
            self.display.setText(self.calculator.get_display())
        return handler

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())
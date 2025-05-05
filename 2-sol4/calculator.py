import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QGridLayout, QLineEdit
)
from PyQt5.QtCore import Qt

# ========================
# 계산 로직을 담당하는 클래스
# ========================
class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        # 초기 상태로 설정
        self.current_input = '0'  # 현재 입력된 값
        self.last_result = None   # 마지막 연산 결과
        self.last_operator = None # 마지막 연산자 (+, -, *, /)
        self.new_input = True     # 새로운 입력 시작 여부

    def input_number(self, num):
        # 입력된 숫자 처리리
        if self.new_input:
            self.current_input = num
            self.new_input = False
        else:
            if self.current_input == '0' and num != '.':
                self.current_input = num
            else:
                self.current_input += num

    def input_dot(self):
        # 소수점 처리리
        if '.' not in self.current_input:
            self.current_input += '.'
            self.new_input = False

    def set_operator(self, operator):
        # 연산자 설정 (+, -, *, /)
        if self.last_operator:
            self.equal() # 이전 연산 수행 
        self.last_result = float(self.current_input)
        self.last_operator = operator
        self.new_input = True

    def add(self):
        self.set_operator('+')

    def subtract(self):
        self.set_operator('-')

    def multiply(self):
        self.set_operator('*')

    def divide(self):
        self.set_operator('/')

    def equal(self):
        # 등호(=) 눌렀을 때 연산 처리 로직
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
                    self.current_input = 'Error: Divide by 0'
                    self.last_result = None
                    self.last_operator = None
                    return
                result = self.last_result / current

            result = round(result, 6)

            if abs(result) > 1e100:
                self.current_input = 'Error: Overflow'
            else:
                self.current_input = str(result)

        except Exception:
            self.current_input = 'Error'
            
        # 연산 후 초기화
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
        except Exception:
            self.current_input = 'Error'
        self.new_input = True

    def get_display(self):
        return self.current_input

# ========================
# UI를 구성하는 클래스
# ========================
class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt5 계산기')  # 창 제목
        self.calculator = Calculator()      # 계산 로직 인스턴스
        self.create_ui()                    # UI 구성 호출

    def create_ui(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(40)
        self.display.setText(self.calculator.get_display())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)

        grid = QGridLayout()
        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('÷', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('×', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0, 1, 2), ('.', 4, 2), ('=', 4, 3),
        ]

        for item in buttons:
            if len(item) == 3:
                btn_text, row, col = item
                rowspan = 1
                colspan = 1
            else:
                btn_text, row, col, rowspan, colspan = item

            btn = QPushButton(btn_text)
            btn.setFixedSize(60, 40)
            grid.addWidget(btn, row, col, rowspan, colspan)
            btn.clicked.connect(self.create_handler(btn_text))

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

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

# ========================
# 메인 함수 (앱 실행 부분)
# ========================
if __name__ == '__main__':
    app = QApplication(sys.argv)  # PyQt 앱 실행 준비
    window = CalculatorApp()      # 계산기 앱 생성
    window.show()                 # 창 띄우기
    sys.exit(app.exec_())         # 이벤트 루프 실행

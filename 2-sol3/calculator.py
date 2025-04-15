import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()  # 부모 클래스의 초기화 호출
        self.setWindowTitle('Emergency Calculator')  # 창 제목 설정
        self.setFixedSize(300, 400)  # 창 크기 고정
        self.init_ui()  # UI 초기화 함수 호출

    def init_ui(self):
        # 버튼 딕셔너리 초기화
        self.buttons = {}  # 버튼을 저장할 딕셔너리 초기화
        
        # 레이아웃 설정
        self.layout = QVBoxLayout()  # 세로 방향 레이아웃

        # 디스플레이 부분 (입력 값 보여주는 곳)
        self.display = QLineEdit()  # 텍스트 입력 필드
        self.display.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        self.display.setReadOnly(True)  # 텍스트 수정 불가
        self.display.setFixedHeight(50)  # 높이 고정
        self.display.setStyleSheet('font-size: 24px;')  # 폰트 크기 설정

        # 레이아웃에 디스플레이 추가
        self.layout.addWidget(self.display)

        # 버튼 배치 레이아웃 (격자형)
        self.buttons_layout = QGridLayout()

        # 버튼 레이블 정의 (숫자, 연산자, AC 등)
        buttons = [
            ['AC', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # 버튼 생성 및 배치
        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                # '0'은 가로로 2개 칸을 차지하므로 두 칸에 걸쳐 배치
                if btn_text == '0':
                    button = QPushButton(btn_text)
                    button.setFixedSize(140, 60)  # 크기 설정
                    self.buttons_layout.addWidget(button, row_idx + 1, col_idx, 1, 2)  # 두 칸에 걸쳐 배치
                # '.' 버튼은 기본 크기대로 배치
                elif btn_text == '.':
                    button = QPushButton(btn_text)
                    button.setFixedSize(60, 60)
                    self.buttons_layout.addWidget(button, row_idx + 1, col_idx + 1)
                else:
                    button = QPushButton(btn_text)
                    button.setFixedSize(60, 60)  # 크기 설정
                    self.buttons_layout.addWidget(button, row_idx + 1, col_idx)  # 일반 버튼 배치

                # 버튼 클릭 시 이벤트 처리 함수 연결
                button.clicked.connect(self.on_button_clicked)
                self.buttons[btn_text] = button  # 버튼을 딕셔너리에 저장

        # 레이아웃에 버튼 추가
        self.layout.addLayout(self.buttons_layout)

        # 계산기 위젯 설정
        self.setLayout(self.layout)

    # 버튼 클릭 시 호출되는 함수
    def on_button_clicked(self):
        sender = self.sender()  # 클릭된 버튼을 가져옴
        text = sender.text()  # 버튼의 텍스트 가져옴

        # 'AC' 버튼은 입력 초기화
        if text == 'AC':
            self.display.setText('')  # 입력 필드 초기화
        # '=' 버튼은 계산 후 결과를 표시
        elif text == '=':
            try:
                # 수식 평가 후 결과를 디스플레이에 표시
                result = str(eval(self.display.text()))  # eval을 사용해 수식을 평가
                self.display.setText(result)  # 결과 표시
            except Exception:
                self.display.setText('Error')  # 예외 발생 시 'Error' 표시
        # '+/-' 버튼은 부호 반전
        elif text == '+/-':
            current = self.display.text()  # 현재 입력된 값
            if current.startswith('-'):  # 음수일 경우
                self.display.setText(current[1:])  # 부호 제거
            elif current:  # 양수일 경우
                self.display.setText('-' + current)  # 부호 추가
        else:
            # 숫자나 연산자를 입력 필드에 추가
            self.display.setText(self.display.text() + text)

# 앱 실행 부분
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 앱 객체 생성
    calc = Calculator()  # 계산기 객체 생성
    calc.show()  # 계산기 창 띄우기
    sys.exit(app.exec_())  # 앱 실행

import os
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt

# Qt platform plugins 경로 지정 -> 개인마다 저장되는 경로가 다를 수 있기에 확인해보고 설정하기!!!
plugin_path = os.path.join(os.path.dirname(QtCore.__file__), 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

# 사칙연산
class Calculator:
    def __init__(self):
        """Calculator 초기화"""
        self.reset()
    
    def add(self, a, b):
        """더하기"""
        return a + b
    
    def subtract(self, a, b):
        """빼기"""
        return a - b
    
    def multiply(self, a, b):
        """곱하기"""
        return a * b
    
    def divide(self, a, b):
        """나누기"""
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        return a / b
    
    def reset(self):
        """계산기 초기화"""
        self.first_number = 0
        self.second_number = 0
        self.operation = None
        self.result = 0
        return 0
    
    def negative_positive(self, number):
        """음수/양수 변환"""
        return -number
    
    def percent(self, number):
        """퍼센트 계산"""
        return number / 100
    
    def equal(self, first_num, second_num, operation):
        """결과 계산"""
        try:
            if operation == '+':
                self.result = self.add(first_num, second_num)
            elif operation == '-':
                self.result = self.subtract(first_num, second_num)
            elif operation == '×':
                self.result = self.multiply(first_num, second_num)
            elif operation == '÷':
                self.result = self.divide(first_num, second_num)
            else:
                return first_num
            
            return self.result
        except ValueError as e:
            raise e


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()  # Calculator 인스턴스 생성
        self.first_number = 0
        self.current_operation = None
        self.waiting_for_number = False

        self.setWindowTitle("iPhone-style Calculator")
        self.setFixedSize(320, 480)  # 아이폰 비슷한 화면 비율
        self.init_ui()

    def init_ui(self):
        # 전체 레이아웃
        vbox = QVBoxLayout()

        # 출력 창
        self.display = QLineEdit('0')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 32px; padding: 10px;")
        vbox.addWidget(self.display)

        # 버튼 배치
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # 그리드 레이아웃
        grid = QGridLayout()

        for row, button_row in enumerate(buttons):
            for col, btn_text in enumerate(button_row):
                btn = QPushButton(btn_text)
                btn.setFixedSize(70, 70)
                btn.setStyleSheet("font-size: 20px;")

                # 0은 2칸 차지
                if btn_text == '0':
                    grid.addWidget(btn, row + 1, 0, 1, 2)
                    continue
                if btn_text == '=':
                    grid.addWidget(btn, row + 1, 3)
                else:
                    adjusted_col = col if btn_text != '0' else 2
                    grid.addWidget(btn, row + 1, adjusted_col)

                # 이벤트 연결
                btn.clicked.connect(lambda _, b=btn_text: self.button_clicked(b))

        vbox.addLayout(grid)
        self.setLayout(vbox)

    def button_clicked(self, button_text):
        try:
            current_text = self.display.text()
            
            # 숫자 입력 - 누를 때마다 화면에 누적
            if button_text.isdigit():
                if self.waiting_for_number or current_text == '0':
                    self.display.setText(button_text)
                    self.waiting_for_number = False
                else:
                    # 숫자를 누적해서 표시
                    self.display.setText(current_text + button_text)
            
            # 소수점 입력 - 이미 있으면 추가되지 않음
            elif button_text == '.':
                if self.waiting_for_number:
                    self.display.setText('0.')
                    self.waiting_for_number = False
                elif '.' not in current_text:
                    # 소수점이 없을 때만 추가
                    self.display.setText(current_text + '.')
            
            # AC (All Clear) - Calculator의 reset() 메소드 사용
            elif button_text == 'AC':
                self.calculator.reset()
                self.display.setText('0')
                self.first_number = 0
                self.current_operation = None
                self.waiting_for_number = False
            
            # +/- (부호 변경) - Calculator의 negative_positive() 메소드 사용
            elif button_text == '+/-':
                current_value = float(current_text)
                result = self.calculator.negative_positive(current_value)
                # 결과가 정수면 정수로, 소수면 소수로 표시
                if result == int(result):
                    self.display.setText(str(int(result)))
                else:
                    self.display.setText(str(result))
            
            # 백분율 - Calculator의 percent() 메소드 사용
            elif button_text == '%':
                current_value = float(current_text)
                result = self.calculator.percent(current_value)
                # 결과가 정수면 정수로, 소수면 소수로 표시
                if result == int(result):
                    self.display.setText(str(int(result)))
                else:
                    self.display.setText(str(result))
            
            # 연산자들
            elif button_text in ['+', '-', '×', '÷']:
                if self.current_operation and not self.waiting_for_number:
                    self.calculate()
                
                self.first_number = float(current_text)
                self.current_operation = button_text
                self.waiting_for_number = True
            
            # 등호 (계산 실행) - Calculator의 equal() 메소드 사용
            elif button_text == '=':
                if self.current_operation:
                    self.calculate()
                    
        except ValueError as e:
            self.display.setText("Error")
            self.first_number = 0
            self.current_operation = None
            self.waiting_for_number = False
    
    def calculate(self):
        """계산을 실행하는 메소드 - Calculator의 equal() 메소드 사용"""
        try:
            second_number = float(self.display.text())
            
            # Calculator의 equal() 메소드를 사용하여 결과 계산
            result = self.calculator.equal(self.first_number, second_number, self.current_operation)
            
            # 결과가 정수면 정수로 표시, 아니면 소수로 표시
            if result == int(result):
                self.display.setText(str(int(result)))
            else:
                self.display.setText(str(result))
            
            self.current_operation = None
            self.waiting_for_number = True
            
        except ValueError as e:
            self.display.setText("Error")
            self.current_operation = None
            self.waiting_for_number = False
        except Exception as e:
            self.display.setText("Error")
            self.current_operation = None
            self.waiting_for_number = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())

import os
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt

# Qt platform plugins 경로 명시적으로 지정
plugin_path = os.path.join(os.path.dirname(QtCore.__file__), 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPhone-style Calculator (UI only)")
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
        # 숫자 및 '.'만 입력 처리
        if button_text.isdigit() or button_text == '.':
            current = self.display.text()
            if current == '0':
                self.display.setText(button_text)
            else:
                self.display.setText(current + button_text)
        else:
            # 연산자나 특수 키는 별도 처리 안 함 (계산 기능은 요구사항 X)
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())

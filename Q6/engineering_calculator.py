import os
import sys
import math
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

plugin_path = os.path.join(os.path.dirname(QtCore.__file__), 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class EngineeringCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.display_text = "0"
        
    def initUI(self):
        self.setWindowTitle('Engineering Calculator')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #000000;")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Display
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setStyleSheet("""
            QLabel {
                background-color: #000000;
                color: white;
                font-size: 48px;
                font-weight: 200;
                padding: 20px;
                border: none;
            }
        """)
        self.display.setMinimumHeight(100)
        main_layout.addWidget(self.display)
        
        # Button layout
        button_layout = QGridLayout()
        main_layout.addLayout(button_layout)
        
        # Button configurations: [text, row, col, color_type]
        buttons = [
            # Row 0 - Scientific functions
            ["(", 0, 0, "function"], [")", 0, 1, "function"], ["mc", 0, 2, "function"], 
            ["m+", 0, 3, "function"], ["m-", 0, 4, "function"], ["mr", 0, 5, "function"],
            ["C", 0, 6, "clear"], ["±", 0, 7, "function"], ["%", 0, 8, "function"], ["÷", 0, 9, "operator"],
            
            # Row 1 - Scientific functions
            ["2nd", 1, 0, "function"], ["x²", 1, 1, "function"], ["x³", 1, 2, "function"],
            ["xʸ", 1, 3, "function"], ["eˣ", 1, 4, "function"], ["10ˣ", 1, 5, "function"],
            ["7", 1, 6, "number"], ["8", 1, 7, "number"], ["9", 1, 8, "number"], ["×", 1, 9, "operator"],
            
            # Row 2 - Scientific functions
            ["1/x", 2, 0, "function"], ["²√x", 2, 1, "function"], ["³√x", 2, 2, "function"],
            ["ʸ√x", 2, 3, "function"], ["ln", 2, 4, "function"], ["log₁₀", 2, 5, "function"],
            ["4", 2, 6, "number"], ["5", 2, 7, "number"], ["6", 2, 8, "number"], ["-", 2, 9, "operator"],
            
            # Row 3 - Scientific functions
            ["x!", 3, 0, "function"], ["sin", 3, 1, "function"], ["cos", 3, 2, "function"],
            ["tan", 3, 3, "function"], ["e", 3, 4, "function"], ["EE", 3, 5, "function"],
            ["1", 3, 6, "number"], ["2", 3, 7, "number"], ["3", 3, 8, "number"], ["+", 3, 9, "operator"],
            
            # Row 4 - Scientific functions and numbers
            ["Rad", 4, 0, "function"], ["sinh", 4, 1, "function"], ["cosh", 4, 2, "function"],
            ["tanh", 4, 3, "function"], ["π", 4, 4, "function"], ["Rand", 4, 5, "function"],
            ["0", 4, 6, "number"], ["0", 4, 7, "number"], [".", 4, 8, "number"], ["=", 4, 9, "equals"],
        ]
        
        # Create buttons
        self.buttons = {}
        for button_info in buttons:
            text, row, col, button_type = button_info
            
            # Skip duplicate "0" button
            if text == "0" and col == 7:
                continue
                
            button = QPushButton(text)
            button.clicked.connect(lambda checked, t=text: self.button_clicked(t))
            
            # Style buttons based on type
            if button_type == "number":
                button.setStyleSheet(self.get_button_style("#333333", "white"))
            elif button_type == "operator":
                button.setStyleSheet(self.get_button_style("#ff9500", "white"))
            elif button_type == "equals":
                button.setStyleSheet(self.get_button_style("#ff9500", "white"))
            elif button_type == "clear":
                button.setStyleSheet(self.get_button_style("#a6a6a6", "black"))
            else:  # function
                button.setStyleSheet(self.get_button_style("#505050", "white"))
            
            button.setMinimumHeight(60)
            button.setFont(QFont("Arial", 16))
            
            # Special handling for wide "0" button
            if text == "0" and col == 6:
                button_layout.addWidget(button, row, col, 1, 2)  # Span 2 columns
            else:
                button_layout.addWidget(button, row, col)
            
            self.buttons[text] = button
    
    def get_button_style(self, bg_color, text_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid #555555;
                border-radius: 8px;
                font-size: 16px;
                font-weight: normal;
            }}
            QPushButton:pressed {{
                background-color: #666666;
            }}
        """
    
    # 삼각함수 관련 기능들
    def calculate_sin(self, x):
        """사인 함수 계산"""
        return math.sin(math.radians(x))
    
    def calculate_cos(self, x):
        """코사인 함수 계산"""
        return math.cos(math.radians(x))
    
    def calculate_tan(self, x):
        """탄젠트 함수 계산"""
        return math.tan(math.radians(x))
    
    def calculate_sinh(self, x):
        """하이퍼볼릭 사인 함수 계산"""
        return math.sinh(x)
    
    def calculate_cosh(self, x):
        """하이퍼볼릭 코사인 함수 계산"""
        return math.cosh(x)
    
    def calculate_tanh(self, x):
        """하이퍼볼릭 탄젠트 함수 계산"""
        return math.tanh(x)
    
    def get_pi(self):
        """원주율 π 반환"""
        return math.pi
    
    def calculate_square(self, x):
        """x의 제곱 계산"""
        return x ** 2
    
    def calculate_cube(self, x):
        """x의 세제곱 계산"""
        return x ** 3
    
    def calculate_power(self, x, y):
        """x의 y제곱 계산"""
        return x ** y
    
    def calculate_sqrt(self, x):
        """제곱근 계산"""
        if x < 0:
            raise ValueError("음수의 제곱근을 계산할 수 없습니다")
        return math.sqrt(x)
    
    def calculate_cbrt(self, x):
        """세제곱근 계산"""
        return x ** (1/3) if x >= 0 else -((-x) ** (1/3))
    
    def calculate_reciprocal(self, x):
        """역수 계산 (1/x)"""
        if x == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        return 1 / x
    
    def calculate_factorial(self, x):
        """팩토리얼 계산"""
        if x < 0 or x != int(x):
            raise ValueError("팩토리얼은 음이 아닌 정수에 대해서만 정의됩니다")
        return math.factorial(int(x))
    
    def calculate_ln(self, x):
        """자연로그 계산"""
        if x <= 0:
            raise ValueError("로그의 인수는 양수여야 합니다")
        return math.log(x)
    
    def calculate_log10(self, x):
        """상용로그 계산"""
        if x <= 0:
            raise ValueError("로그의 인수는 양수여야 합니다")
        return math.log10(x)
    
    def calculate_exp(self, x):
        """e^x 계산"""
        return math.exp(x)
    
    def calculate_10_power_x(self, x):
        """10^x 계산"""
        return 10 ** x
    
    def get_e(self):
        """자연상수 e 반환"""
        return math.e
    
    def button_clicked(self, text):
        """Handle button click events"""
        print(f"Button clicked: {text}")
        
        try:
            # Handle different button types
            if text.isdigit() or text == ".":
                # Number input
                if self.display_text == "0":
                    self.display_text = text
                else:
                    self.display_text += text
                    
            elif text == "C":
                # Clear
                self.display_text = "0"
                
            elif text == "±":
                # Toggle sign
                if self.display_text != "0":
                    if self.display_text.startswith("-"):
                        self.display_text = self.display_text[1:]
                    else:
                        self.display_text = "-" + self.display_text
                        
            elif text in ["+", "-", "×", "÷"]:
                # Operators
                if not self.display_text.endswith(" "):
                    self.display_text += f" {text} "
                    
            elif text == "=":
                # Equals (basic calculation)
                self.calculate_result()
                
            # Scientific function buttons
            elif text == "sin":
                self.apply_function(self.calculate_sin)
            elif text == "cos":
                self.apply_function(self.calculate_cos)
            elif text == "tan":
                self.apply_function(self.calculate_tan)
            elif text == "sinh":
                self.apply_function(self.calculate_sinh)
            elif text == "cosh":
                self.apply_function(self.calculate_cosh)
            elif text == "tanh":
                self.apply_function(self.calculate_tanh)
            elif text == "π":
                self.display_text = str(self.get_pi())
            elif text == "e":
                self.display_text = str(self.get_e())
            elif text == "x²":
                self.apply_function(self.calculate_square)
            elif text == "x³":
                self.apply_function(self.calculate_cube)
            elif text == "²√x":
                self.apply_function(self.calculate_sqrt)
            elif text == "³√x":
                self.apply_function(self.calculate_cbrt)
            elif text == "1/x":
                self.apply_function(self.calculate_reciprocal)
            elif text == "x!":
                self.apply_function(self.calculate_factorial)
            elif text == "ln":
                self.apply_function(self.calculate_ln)
            elif text == "log₁₀":
                self.apply_function(self.calculate_log10)
            elif text == "eˣ":
                self.apply_function(self.calculate_exp)
            elif text == "10ˣ":
                self.apply_function(self.calculate_10_power_x)
            elif text == "%":
                self.apply_function(lambda x: x / 100)
                
        except Exception as e:
            self.display_text = f"Error: {str(e)}"
            
        # Update display
        self.display.setText(self.display_text)
    
    def apply_function(self, func):
        """Apply a mathematical function to the current display value"""
        try:
            current_value = float(self.display_text)
            result = func(current_value)
            
            # Format result appropriately
            if result == int(result):
                self.display_text = str(int(result))
            else:
                self.display_text = f"{result:.10g}"  # Remove trailing zeros
                
        except ValueError as e:
            self.display_text = f"Error: {str(e)}"
        except Exception as e:
            self.display_text = "Error"
    
    def calculate_result(self):
        """Calculate basic arithmetic operations"""
        try:
            # Simple evaluation for basic operations
            expression = self.display_text
            
            # Replace display symbols with Python operators
            expression = expression.replace("×", "*").replace("÷", "/")
            
            # Evaluate the expression
            result = eval(expression)
            
            # Format result
            if result == int(result):
                self.display_text = str(int(result))
            else:
                self.display_text = f"{result:.10g}"
                
        except:
            self.display_text = "Error"

def main():
    app = QApplication(sys.argv)
    calculator = EngineeringCalculator()
    calculator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
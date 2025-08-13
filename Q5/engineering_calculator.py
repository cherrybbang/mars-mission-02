import os
import sys
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
    
    def button_clicked(self, text):
        """Handle button click events"""
        
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
            # Equals (calculation would go here)
            pass
        else:
            # Other functions
            if self.display_text == "0":
                self.display_text = f"{text}("
            else:
                self.display_text += f"{text}("
        
        # Update display
        self.display.setText(self.display_text)

def main():
    app = QApplication(sys.argv)
    calculator = EngineeringCalculator()
    calculator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
import sys
import math
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                             QPushButton, QLineEdit, QVBoxLayout, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculatrice Scientifique")
        self.setFixedSize(450, 700)  # Ajusté pour inclure l'historique

        # Style global
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                padding: 10px;
                font-size: 24px;
                color: #2d3436;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #2d3436;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                font-size: 18px;
                color: #2d3436;
                padding: 10px;
                margin: 4px;
            }
            QPushButton:hover {
                background-color: #e8ecef;
            }
            QPushButton:pressed {
                background-color: #dfe4ea;
            }
            QPushButton#operator {
                background-color: #74b9ff;
                color: white;
                border: none;
            }
            QPushButton#operator:hover {
                background-color: #339af0;
            }
            QPushButton#function {
                background-color: #dfe4ea;
                color: #2d3436;
                border: none;
            }
            QPushButton#function:hover {
                background-color: #ced4da;
            }
            QPushButton#equals {
                background-color: #ff7675;
                color: white;
                border: none;
            }
            QPushButton#equals:hover {
                background-color: #ff5e57;
            }
        """)

        # Widget principal
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Champ d'affichage
        self.display = QLineEdit()
        self.display.setFixedHeight(80)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Arial", 24))
        self.layout.addWidget(self.display)

        # Zone d'historique
        self.history_display = QTextEdit()
        self.history_display.setFixedHeight(150)
        self.history_display.setReadOnly(True)
        self.history_display.setFont(QFont("Arial", 14))
        self.history_display.setHtml("<b>Historique :</b><br>")
        self.layout.addWidget(self.history_display)

        # Grille des boutons
        self.button_grid = QGridLayout()
        self.button_grid.setSpacing(8)
        self.layout.addLayout(self.button_grid)

        # Dictionnaire des boutons
        self.buttons = {}
        button_layout = [
            ('C', 0, 0, 'function'), ('(', 0, 1), (')', 0, 2), ('÷', 0, 3, 'operator'),
            ('sin', 1, 0, 'function'), ('7', 1, 1), ('8', 1, 2), ('9', 1, 3),
            ('cos', 2, 0, 'function'), ('4', 2, 1), ('5', 2, 2), ('6', 2, 3),
            ('tan', 3, 0, 'function'), ('1', 3, 1), ('2', 3, 2), ('3', 3, 3),
            ('ln', 4, 0, 'function'), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3, 'equals'),
            ('√', 5, 0, 'function'), ('×', 5, 1, 'operator'), ('−', 5, 2, 'operator'), ('+', 5, 3, 'operator'),
        ]

        # Création des boutons
        for text, row, col, *style in button_layout:
            button = QPushButton(text)
            button.setFixedSize(90, 70)
            button.setFont(QFont("Arial", 18))

            # Appliquer le style spécifique
            if style and style[0]:
                button.setObjectName(style[0])

            # Ajouter des icônes pour certaines fonctions
            if text == '√':
                button.setText("√x")
            elif text == '−':
                button.setText("−")
            elif text == '×':
                button.setText("×")

            self.button_grid.addWidget(button, row, col)
            self.buttons[text] = button
            button.clicked.connect(self.button_clicked)

        # Variables de calcul
        self.current_expression = ""
        self.result_shown = False
        self.history = []

    def button_clicked(self):
        button = self.sender()
        key = button.text()

        # Normaliser les symboles pour le calcul
        key = key.replace('√x', '√').replace('−', '-').replace('×', '*')

        if key == 'C':
            self.current_expression = ""
            self.display.setText("")
            self.history = []
            self.history_display.setHtml("<b>Historique :</b><br>")

        elif key == '=':
            try:
                # Remplacer les symboles pour eval
                expr = self.current_expression.replace('*', '×').replace('-', '−')
                expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-')
                expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos')
                expr = expr.replace('tan', 'math.tan').replace('ln', 'math.log')
                expr = expr.replace('√', 'math.sqrt')

                result = eval(expr, {"math": math, "__builtins__": {}})
                result_str = str(round(result, 8))
                self.history.append(f"{self.current_expression} = {result_str}")
                self.history_display.setHtml("<b>Historique :</b><br>" + "<br>".join(self.history[-5:]))
                self.display.setText(result_str)
                self.current_expression = result_str
                self.result_shown = True
            except Exception:
                self.display.setText("Erreur")
                self.current_expression = ""

        else:
            if self.result_shown and key in '0123456789.':
                self.current_expression = ""
                self.result_shown = False

            self.current_expression += key
            display_text = self.current_expression.replace('*', '×').replace('-', '−')
            self.display.setText(display_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
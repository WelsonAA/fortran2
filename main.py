"""import graphviz

def generate_dfa(lex):
    identifier_dfa = graphviz.Digraph(comment='DFA for Identifier')

    identifier_dfa.node('start')
    identifier_dfa.node('accept', shape='doublecircle')

    input_word = lex
    current_node = 'start'
    a=1
    for node_count, char in enumerate(input_word):
        next_node = f'node{node_count}'
        identifier_dfa.node(next_node, label="S"+str(a))
        identifier_dfa.edge(current_node, next_node, label=char)
        current_node = next_node
        a=a+1

    identifier_dfa.edge(current_node, 'accept', label='')

    identifier_dfa.attr(rankdir='LR')

    identifier_dfa.render('identifier', format='png', view=True, directory="DFA")

import tkinter as tk

def create_gui(word_list):
    root = tk.Tk()

    for word in word_list:
        frame = tk.Frame(root)
        frame.pack()

        label = tk.Label(frame, text=word)
        label.pack(side=tk.LEFT)

        button = tk.Button(frame, text="Click", command=lambda w=word: generate_dfa(w))
        button.pack(side=tk.LEFT)

    root.mainloop()

# Example usage
#words = ["PROGRAM", "IF", "END", "IMPLICIT", "NONE", "DO", "ELSE", "INTEGER", "REAL", "PARAMETER", "COMPLEX", "THEN", "CHARACTER", "READ", "PRINT", "LOGICAL", "TRUE", "FALSE"]
#create_gui(words)"""
"""import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
import graphviz

def generate_dfa(lex):
    identifier_dfa = graphviz.Digraph(comment='DFA for Identifier')

    identifier_dfa.node('start')
    identifier_dfa.node('accept', shape='doublecircle')

    input_word = lex

    current_node = 'start'
    for node_count, char in enumerate(input_word):
        next_node = f'node{node_count}'
        identifier_dfa.node(next_node, label=char)
        identifier_dfa.edge(current_node, next_node, label=char)
        current_node = next_node

    identifier_dfa.edge(current_node, 'accept', label='')

    identifier_dfa.attr(rankdir='LR')

    # Render the DFA to PNG format
    identifier_dfa.render('identifier', format='png', directory="DFA", cleanup=True)

class DFAViewer(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle('DFA Viewer')
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def load_dfa(self, image_path):
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)

if __name__ == '__main__':
    lex = "LOGICAL"
    generate_dfa(lex)

    app = QApplication(sys.argv)

    dfa_viewer = DFAViewer()
    dfa_viewer.load_dfa('DFA/identifier.png')
    dfa_viewer.show()

    sys.exit(app.exec_())"""


import scan
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QFileDialog, QVBoxLayout, QStackedWidget
from PyQt5.QtGui import QFont, QColor, QPalette, QTextCursor, QTextCharFormat, QTextDocument, QIcon, QPixmap
from PyQt5.QtCore import Qt, QRegExp


class TokenVisualizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Token DFA Visualization")
        self.setGeometry(300, 300, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        stacked_widget = QStackedWidget(self)

        # Page 1: Upload file page
        upload_page = QWidget()
        upload_layout = QVBoxLayout(upload_page)

        # Create a label for file upload
        label = QLabel("Upload a text file:", self)
        label.setFont(QFont("Arial", 12))

        # Create a button to open file dialog
        upload_button = QPushButton("Browse", self)
        upload_button.setFont(QFont("Arial", 12))
        upload_button.setStyleSheet(
            """
            QPushButton {
                background-color: #00a8e8;
                color: white;
                border: none;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #0095cc;
            }

            QPushButton:pressed {
                background-color: #007999;
            }
            """
        )
        upload_button.clicked.connect(self.upload_file)

        # Add label and upload button to the layout
        upload_layout.addWidget(label)
        upload_layout.addWidget(upload_button)

        stacked_widget.addWidget(upload_page)

        # Page 2: Scan result page
        scan_page = QWidget()
        scan_layout = QVBoxLayout(scan_page)

        # Create a label for scan result
        scan_result_label = QLabel("Scan Result:", self)
        scan_result_label.setFont(QFont("Arial", 12))

        # Create a QTextEdit widget to display scan result
        self.scan_result_textedit = QTextEdit(self)
        self.scan_result_textedit.setFont(QFont("Courier New", 12))
        self.scan_result_textedit.setStyleSheet("background-color: white;")

        # Add label and QTextEdit widget to the layout
        scan_layout.addWidget(scan_result_label)
        scan_layout.addWidget(self.scan_result_textedit)

        stacked_widget.addWidget(scan_page)

        # Create a button to trigger the page switch to the scan result page
        scan_button = QPushButton("Scan", self)
        scan_button.setFont(QFont("Arial", 12))
        scan_button.clicked.connect(lambda: stacked_widget.setCurrentWidget(scan_page))
        upload_layout.addWidget(scan_button)

        # Create a button for parse
        parse_button = QPushButton("Parse", self)
        parse_button.setFont(QFont("Arial", 12))
        parse_button.clicked.connect(self.parse_file)
        parse_button.setEnabled(False)

        # Add parse button to the layout
        upload_layout.addWidget(parse_button)

        # Create a textbox to display file contents
        self.textbox = QTextEdit(self)
        self.textbox.setFont(QFont("Courier New", 12))
        self.textbox.setStyleSheet("background-color: white;")

        # Add textbox to the layout
        upload_layout.addWidget(self.textbox)

        # Add the stacked widget to the main layout
        layout.addWidget(stacked_widget)

        # Set the layout for the main widget
        self.setLayout(layout)

    def upload_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Upload Text File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r") as file:
                file_contents = file.read()
                self.textbox.setText(file_contents)
                self.textbox.moveCursor(QTextCursor.Start)
                self.textbox.ensureCursorVisible()
                self.textbox.setFocus()
                self.textbox.repaint()
                self.enable_buttons()

    def enable_buttons(self):
        scan_button = self.findChild(QPushButton, "Scan")
        parse_button = self.findChild(QPushButton, "Parse")
        if scan_button and parse_button:
            scan_button.setEnabled(True)
            parse_button.setEnabled(True)

    def scan_file(self):
        text = self.textbox.toPlainText()
        print(str(text))
        scan_result = scan.find_token(str(text))

        # Change text color of specific words
        self.change_text_color(scan_result, "PROGRAM", QColor("#FF0000"))  # Change color of "PROGRAM" to red
        self.change_text_color(scan_result, "IF", QColor("#00FF00"))  # Change color of "IF" to green
        self.change_text_color(scan_result, "END", QColor("#0000FF"))  # Change color of "END" to blue
        self.change_text_color(scan_result, "IMPLICIT", QColor("#FF00FF"))  # Change color of "IMPLICIT" to purple
        self.change_text_color(scan_result, "NONE", QColor("#FFFF00"))  # Change color of "NONE" to yellow
        self.change_text_color(scan_result, "DO", QColor("#FF8000"))  # Change color of "DO" to orange
        self.change_text_color(scan_result, "ELSE", QColor("#0080FF"))  # Change color of "ELSE" to light blue
        self.change_text_color(scan_result, "INTEGER", QColor("#FF0080"))  # Change color of "INTEGER" to pink
        self.change_text_color(scan_result, "REAL", QColor("#00FFFF"))  # Change color of "REAL" to cyan
        self.change_text_color(scan_result, "PARAMETER", QColor("#80FF00"))  # Change color of "PARAMETER" to lime green
        self.change_text_color(scan_result, "COMPLEX", QColor("#FF80FF"))  # Change color of "COMPLEX" to light purple
        self.change_text_color(scan_result, "THEN", QColor("#FFBF00"))  # Change color of "THEN" to gold
        self.change_text_color(scan_result, "CHARACTER", QColor("#FF0080"))  # Change color of "CHARACTER" to pink
        self.change_text_color(scan_result, "READ", QColor("#FF00BF"))  # Change color of "READ" to dark pink
        self.change_text_color(scan_result, "PRINT", QColor("#00FFBF"))  # Change color of "PRINT" to aqua
        self.change_text_color(scan_result, "LOGICAL", QColor("#8000FF"))  # Change color of "LOGICAL" to indigo
        self.change_text_color(scan_result, "TRUE", QColor("#00FF00"))  # Change color of "TRUE" to lime
        self.change_text_color(scan_result, "FALSE", QColor("#808080"))  # Change color of "FALSE" to gray

        self.scan_result_textedit.setText(scan_result)

    def change_text_color(self, text, pattern, color):
        cursor = self.scan_result_textedit.textCursor()
        format = QTextCharFormat()
        format.setForeground(color)
        regex = QRegExp(pattern)
        pos = 0

        index = regex.indexIn(text, pos)
        while index != -1:
            pos = index + regex.matchedLength()
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
            cursor.setCharFormat(format)
            index = regex.indexIn(text, pos)

        self.scan_result_textedit.setTextCursor(cursor)

    def parse_file(self):
        # TODO: Implement the parsing logic for the file contents
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TokenVisualizationWindow()
    window.show()
    sys.exit(app.exec_())

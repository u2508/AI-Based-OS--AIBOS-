import sys
import apis.ai_version_6_ALIAB_backend as backend
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
import multiprocessing
app = QApplication(sys.argv)
window = QWidget()
window.setWindowFlags(Qt.FramelessWindowHint)
window.setAttribute(Qt.WA_TranslucentBackground)
# Styling constants
SEARCH_BAR_STYLE = "QLineEdit { background-color: rgba(0, 0, 0, 0.7); color: white; border: 2px solid transparent; border-radius: 10px; padding: 2px; }"
SEND_BUTTON_STYLE = "QPushButton { background-color: aqua; border: 2px solid transparent; border-radius: 15px; }""QPushButton:hover { background-color: lightcyan;border-radius: 15px; }"

# Create a layout for the search bar and send button
search_layout = QHBoxLayout()

# Search Bar
search_bar = QLineEdit()
search_bar.setPlaceholderText("Search")
search_bar.setFont(QFont("Helvetica", 32))
search_bar.setStyleSheet(SEARCH_BAR_STYLE)
search_layout.addWidget(search_bar)

# Send Button
send_button = QPushButton("Send")
send_button.setStyleSheet(SEND_BUTTON_STYLE)
send_button.setFont(QFont("Helvetica", 32))
# Create a layout for the main window
main_layout = QVBoxLayout()

# Add the search layout to the main layout, aligning to the right
main_layout.addLayout(search_layout)

# Add the send button to the search layout
search_layout.addWidget(send_button)

# Set the layout for the main window
window.setLayout(main_layout)
window.setWindowTitle("Spotlight Search")
window.setGeometry(350, 300, 700, 100)  # Adjust the geometry as needed

def search_clicked():
        send_button.setStyleSheet("background-color: green;border: 2px solid transparent;border-radius: 10px;")
        send_button.show()
        global call_search_process
        call_search_process = multiprocessing.Process(target=backend_class.runloop,args=(search_bar.text(),))
        call_search_process.start()
        # Create a QTimer to trigger a delayed reset of the button style
        timer = QTimer()
        timer.singleShot(2000, reset_button_style)
def reset_button_style():
        send_button.setStyleSheet(
            "QPushButton { background-color: aqua; border: 2px solid transparent; border-radius: 15px; }"
            "QPushButton:hover { background-color: lightcyan; }"
        )

send_button.clicked.connect(search_clicked)

def exec(api_key):
        if "backend_class" not in globals():
                global backend_class
                backend_class=backend.VoiceInteractionHandler(api_key)
        if window.isHidden()==True:
                window.show()
        else:
                window.hide()
        try:
            if call_search_process.is_alive()==True:
                call_search_process.terminate()
        except Exception as e:
            pass
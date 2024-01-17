import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import multiprocessing

class NewsApp(QWidget):
    def __init__(self):
        super().__init__()
        # GUI setup
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(300, 100, 800, 600)
        self.setWindowTitle('News App')
        self.setStyleSheet("background-color: yellow;")

        # Country input
        self.country_label = QLabel('Enter Query:', self)
        self.country_label.setFont(QFont('Arial', 18))
        #self.country_label.setStyleSheet("color: white;")
        self.country_label.move(50, 30)

        self.country_textbox = QLineEdit(self)
        self.country_textbox.setFont(QFont('Arial', 24))
        self.country_textbox.move(300, 25)
        self.country_textbox.resize(350, 45)
        self.country_textbox.setStyleSheet("QLineEdit { background-color: rgba(0, 0, 0, 0.7); color: white; border: 2px solid transparent; border-radius: 10px; padding: 2px; }")

        # Category dropdown
        self.category_label = QLabel('Choose Model:', self)
        self.category_label.setFont(QFont('Arial', 18))
        #self.category_label.setStyleSheet("color: white;")
        self.category_label.move(50, 80)

        self.category_combobox = QComboBox(self)
        self.category_combobox.setFont(QFont('Arial', 24))
        self.category_combobox.setStyleSheet("QComboBox { background-color: cyan; border: 2px solid transparent; border-radius: 15px; }"
                                             "QComboBox::drop-down { image: url(https://cdn-icons-png.flaticon.com/512/226/226188.png);border-radius: 15px; }"
                                             "QComboBox::drop-down-menu { background-color: green; }"
                                      "QComboBox:hover { background-color: lightcyan; border-radius: 15px; }")
        self.category_combobox.move(300, 75)
        self.category_combobox.addItems(['llm', 'llama', 'Opengpt', 'Google_Summarizer', 'Science', 'Technology'])

        # Article display
        self.article_label = QLabel('results:', self)
        self.article_label.setFont(QFont('Arial', 18))
        self.article_label.move(50, 130)

        self.article_textbox = QTextEdit(self)
        self.article_textbox.setFont(QFont('Arial', 14))
        self.article_textbox.setReadOnly(True)
        self.article_textbox.move(50, 170)
        self.article_textbox.resize(700, 300)
        self.article_textbox.setStyleSheet("background-color: green;")
        
        # Fetch button
        self.fetch_button = QPushButton('Fetch results', self)
        self.fetch_button.setFont(QFont('Arial', 18))
        self.fetch_button.move(50, 500)
        self.fetch_button.setStyleSheet("background-color: red;")
        self.fetch_button.clicked.connect(self.fetch_articles)

        # Hide button
        self.hide_button = QPushButton('Close page', self)
        self.hide_button.setFont(QFont('Arial', 18))
        self.hide_button.move(350, 500)
        self.hide_button.setStyleSheet("background-color: green;")
        self.hide_button.clicked.connect(self.hide_article)

        # Speech button
        self.speech_button = QPushButton('Read for me', self)
        self.speech_button.setFont(QFont('Arial', 18))
        self.speech_button.move(600, 500)
        self.speech_button.setStyleSheet("background-color: blue;")
        self.speech_button.clicked.connect(self.speak_article)

    def hide_article(self):
        self.call()
        self.country_textbox.clear()
        self.article_textbox.clear()

    def speak_article(self):
        article_text = self.article_textbox.toPlainText()
        if article_text:
            self.call_search_process = multiprocessing.Process(target=Speech,args=(article_text,))
            self.call_search_process.start()
        else:
            pass

    def fetch_articles(self):
        input = self.country_textbox.text().strip()
        input_category = self.category_combobox.currentText()
        func=getattr(model,input_category)
        Headlines = func(input)

        self.article_textbox.clear()
        if Headlines:
            self.article_textbox.append(Headlines)
        else:
            self.article_textbox.append(
                f"Sorry no output found, Something Wrong!!!")
    def call(self):
        if self.isHidden()==True:
            self.show()
        else:
            if __name__ == '__main__':
                exit()
            else:
                self.hide()
                try:
                        self.call_search_process.terminate()
                except Exception as e:
                    pass


app = QApplication(sys.argv)

if __name__ == '__main__':
    from voice_recognition_module import Speech
    import models_for_chat as model
    news_app = NewsApp()
    news_app.call()
    sys.exit(app.exec_())
else:
    from apis.voice_recognition_module import Speech
    import apis.models_for_chat as model
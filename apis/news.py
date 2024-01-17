import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from newsapi import NewsApiClient
import pycountry,multiprocessing

class NewsApp(QWidget):
    def __init__(self):
        super().__init__()

        # News API setup
        self.newsapi = NewsApiClient(api_key='a33cb45d39cd4287b69271a32ed56092')

        # GUI setup
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(300, 100, 800, 600)
        self.setWindowTitle('News App')
        self.setStyleSheet("background-color: yellow;")

        # Country input
        self.country_label = QLabel('Enter Country:', self)
        self.country_label.setFont(QFont('Arial', 18))
        #self.country_label.setStyleSheet("color: white;")
        self.country_label.move(50, 30)

        self.country_textbox = QLineEdit(self)
        self.country_textbox.setFont(QFont('Arial', 18))
        self.country_textbox.move(300, 25)
        self.country_textbox.resize(150, 30)
        self.country_textbox.setStyleSheet("background-color: white;")

        # Category dropdown
        self.category_label = QLabel('Choose Category:', self)
        self.category_label.setFont(QFont('Arial', 18))
        #self.category_label.setStyleSheet("color: white;")
        self.category_label.move(50, 80)

        self.category_combobox = QComboBox(self)
        self.category_combobox.setFont(QFont('Arial', 18))
        self.category_combobox.setStyleSheet("background-color: white;")
        self.category_combobox.move(300, 75)
        self.category_combobox.addItems(['Business', 'Entertainment', 'General', 'Health', 'Science', 'Technology'])

        # Article display
        self.article_label = QLabel('Article:', self)
        self.article_label.setFont(QFont('Arial', 18))
        self.article_label.move(50, 130)

        self.article_textbox = QTextEdit(self)
        self.article_textbox.setFont(QFont('Arial', 14))
        self.article_textbox.setReadOnly(True)
        self.article_textbox.move(50, 170)
        self.article_textbox.resize(700, 300)
        self.article_textbox.setStyleSheet("background-color: green;")
        
        # Fetch button
        self.fetch_button = QPushButton('Fetch Articles', self)
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
        self.news()
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
        input_country = self.country_textbox.text().strip()
        input_category = self.category_combobox.currentText()

        countries = {}
        for country in pycountry.countries:
            countries[country.name] = country.alpha_2

        codes = [countries.get(input_country.title(), 'Unknown code')]

        top_headlines = self.newsapi.get_top_headlines(
            category=input_category.lower(), language='en', country=codes[0].lower())

        Headlines = top_headlines['articles']

        self.article_textbox.clear()
        if Headlines:
            for articles in Headlines:
                b = articles['title'][::-1].index("-")
                if "news" in (articles['title'][-b+1:]).lower():
                    self.article_textbox.append(
                        f"{articles['title'][-b+1:]}: {articles['title'][:-b-2]}.")
                else:
                    self.article_textbox.append(
                        f"{articles['title'][-b+1:]} News: {articles['title'][:-b-2]}.")
        else:
            self.article_textbox.append(
                f"Sorry no articles found for {input_country}, Something Wrong!!!")
    def news(self):
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
    news_app = NewsApp()
    news_app.show()
    sys.exit(app.exec_())
else:
    from apis.voice_recognition_module import Speech

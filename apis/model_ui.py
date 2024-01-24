import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt5.QtGui import QPixmap, QImage,QFont
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QByteArray, Qt
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
        self.category_combobox.addItems([ 'llama', 'llm','Opengpt','chat_with_ai', "text_to_img"])

        # Article display
        self.article_label = QLabel('results:', self)
        self.article_label.setFont(QFont('Arial', 18))
        self.article_label.move(50, 130)

        self.article_textbox = QTextEdit(self)
        self.article_textbox.setFont(QFont('Arial', 14))
        self.article_textbox.move(50, 170)
        self.article_textbox.resize(700, 300)
        self.article_textbox.setStyleSheet("background-color: green;")
        self.article_img = QLabel(self)
        self.article_img.move(50, 170)
        self.article_img.resize(700, 300)
        self.article_img.setStyleSheet("background-color: yellow;")
        self.article_img.hide()
        self.article_img.setAlignment(Qt.AlignCenter)
        self.article_textbox.setReadOnly(True)
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
        self.down_button = QPushButton('download', self)
        self.down_button.setFont(QFont('Arial', 18))
        self.down_button.move(600, 500)
        self.down_button.setStyleSheet("background-color: blue;")
        self.down_button.clicked.connect(self.speak_article)
        self.down_button.hide()

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
        self.article_textbox.setText("wait compiling output")
        
        Headlines = func(input)

        if Headlines:
            if input_category=="text_to_img":
                self.load_image_from_url(Headlines[0])
            else:    
                self.article_textbox.clear()
                self.article_textbox.append(Headlines)
        else:
            self.article_textbox.clear()
            self.article_textbox.append(
                f"Sorry no output found, Something Wrong!!!")
    def load_image_from_url(self, url):
        manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        print(url)
        manager.finished.connect(self.image_loaded)
        manager.get(request)

    def image_loaded(self, reply):
        try:
            image_data = reply.readAll()
            image = QImage.fromData(QByteArray(image_data))
            
            # Resize the image to fit within the QLabel
            scaled_image = image.scaled(self.article_img.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)

            pixmap = QPixmap.fromImage(scaled_image)
            self.show_image(pixmap)
        except Exception as e:
            print("Error loading image:",str(e) )

    def show_image(self, image_path):
        self.article_img.setPixmap(image_path)
        self.article_img.show()
        self.article_textbox.hide()
        self.speech_button.hide()
        self.down_button.show()
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
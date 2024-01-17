import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        # GUI setup
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)    
        self.setGeometry(300, 100, 800, 600)
        self.setWindowTitle('Weather App')
        self.setStyleSheet("background-color: red;")

        # City input
        self.city_label = QLabel('Enter City:', self)
        self.city_label.setFont(QFont('Arial', 18))
        self.city_label.move(50, 30)

        self.city_textbox = QLineEdit(self)
        self.city_textbox.setFont(QFont('Arial', 18))
        self.city_textbox.setStyleSheet("background-color: white;")
        self.city_textbox.move(200, 25)
        self.city_textbox.resize(150, 30)

        # Weather display
        self.weather_label = QLabel('Weather Information:', self)
        self.weather_label.setFont(QFont('Arial', 18))
        self.weather_label.move(50, 80)

        self.weather_textbox = QTextEdit(self)
        self.weather_textbox.setFont(QFont('Arial', 14))
        self.weather_textbox.move(50, 120)
        self.weather_textbox.resize(700, 300)
        self.weather_textbox.setReadOnly(True)

        # Fetch button
        self.fetch_button = QPushButton('Fetch Weather', self)
        self.fetch_button.setFont(QFont('Arial', 18))
        self.fetch_button.move(50, 500)
        self.fetch_button.setStyleSheet("background-color: green;")
        self.fetch_button.clicked.connect(self.fetch_weather)
        self.hide_button = QPushButton('Close page', self)
        self.hide_button.setFont(QFont('Arial', 18))
        self.hide_button.move(350, 500)
        self.hide_button.setStyleSheet("background-color: blue;")
        self.hide_button.clicked.connect(self.weather)


    def fetch_weather(self):
        city_name = self.city_textbox.text().strip()
        api_key = '05846eeec57114c0fa3712580edc90fd'
        # Replace with your actual API key

        weather_info = self.get_weather(city_name, api_key)
        self.weather_textbox.clear()
        self.weather_textbox.append(weather_info)

    def get_weather(self, city, api_key):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
        }

        response = requests.get(base_url, params=params)
        weather_data = response.json()
        
        if response.status_code == 200:
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            feels_like=weather_data['main']['feels_like']
            humidity=weather_data['main']['humidity']
            return f"The weather in {city} is {description} with a temperature of {temperature} Kelvin or {round((temperature-273.15),2)}°C with humidity of {humidity}%.The Weather feels like {round((feels_like-273.15),2)}°C"
        else:
            return f"Unable to fetch weather data. Error: {response.status_code}"
    def weather(self):
        if self.isHidden()==True:
                self.show()
        else:
            if __name__ == '__main__':
                exit()
            else:
                self.hide()
        self.city_textbox.clear()
app = QApplication(sys.argv)

if __name__ == '__main__':
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

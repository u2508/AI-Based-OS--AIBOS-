import sys,json,os
import apis.spotlight_search as Spotlight,apis.news as news,apis.weather as weather
import apis.appLOOK as applook,apis.heathbot as healthgpt,apis.model_ui as edugpt,apis.notepad as notes
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
from apis.ai_version_6_ALIAB_backend import VoiceInteractionHandler

from screeninfo import get_monitors
"""AI operating system 
    version 1.0
    Code Name:ALIAB"""
def get_resolution():
    monitors = get_monitors()
    if monitors:
        primary_monitor = monitors[0]
        return primary_monitor.width, primary_monitor.height
    else:
        return None
api = "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"
class SettingsDialog(QDialog):
    def __init__(self, ai):
        super().__init__()
        self.ai = ai
        self.setWindowTitle("Settings")
        self.setGeometry(430, 220, 500, 300)
        self.init_ui()
        self.setStyleSheet("background-color: blue; color: white; border: 15px; padding:8px ")
        

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)    
        # Create a group box for temperature settings
        temperature_group_box = QGroupBox("Temperature Settings")
        temperature_layout = QFormLayout()
        # Label and input field for adjusting temperature
        temperature_label = QLabel("AI Temperature:")
        self.temperature_input = QLineEdit()
        self.temperature_input.setStyleSheet("background-color: red; color: white; border: none;")
        self.temperature_input.setText(str(self.ai.gpt3_temperature))

        # Slider for adjusting temperature
        temperature_slider = QSlider(Qt.Horizontal)
        temperature_slider.setMinimum(0)
        temperature_slider.setMaximum(100)
        
        temperature_slider.setValue(int(self.ai.gpt3_temperature * 100))
        temperature_slider.valueChanged.connect(self.update_temperature_input)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)

        # Add the elements to the temperature layout
        temperature_layout.addRow(temperature_label, self.temperature_input)
        temperature_layout.addRow("Adjust Temperature:", temperature_slider)

        temperature_group_box.setLayout(temperature_layout)

        # Add the temperature group box and save button to the main layout
        layout.addWidget(temperature_group_box)
        layout.addWidget(save_button)
        layout.setAlignment(Qt.AlignCenter)  # Align the center of the layout

        self.setLayout(layout)
    def update_temperature_input(self, value):
        # Update the temperature input field when the slider value changes
        self.temperature_input.setText(str(value / 100.0))

    def save_settings(self):
        # Save the settings when the "Save" button is clicked
        try:
            new_temperature = float(self.temperature_input.text())
            if 0.0 <= new_temperature <= 1.0:
                self.ai.gpt3_temperature = new_temperature
                self.close()
            else:
                QMessageBox.warning(self, "Invalid Input", "Temperature must be between 0.0 and 1.0")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Invalid temperature value")




class VoiceBotGUI(QMainWindow):
    def __init__(self, voice):
        super().__init__()
        self.setWindowTitle("Voice Bot GUI")
        self.news=news.NewsApp()
        self.weather=weather.WeatherApp()
        self.health=healthgpt.DiseasePredictionApp()
        self.applook=applook.AppSearchApp()
        self.education=edugpt.NewsApp()
        self.notes=notes.MainWindow()
        self.interaction_history = ['\n\n',]
        self.init_ui()
        self.count=0
        self.voice_handler=voice
    def gettext(self):
        try:
            with open(r'knowledge_base.json', 'r') as file:
                self.knowledge_base = json.load(file)
                self.interaction_history.extend(list(map(lambda a: str(a+": "+self.knowledge_base[a]), self.knowledge_base)))
        except FileNotFoundError:
            pass
    def settext(self):
        self.gettext()
        history_text = "\n".join(self.interaction_history)
        #self.history_text.setPlainText(history_text)
    def init_ui(self):
        label = QLabel(self)
        if getattr(sys, 'frozen', False):
            self.base_path = sys._MEIPASS
        else:
    # Running as a regular Python script
            self.base_path = os.path.abspath(".")
        resolution = get_resolution()
        if resolution[0]in range(1080,1560) and resolution[1]in range(710,1080):
            image_path = os.path.join(self.base_path, "C:\\Users\\utkar\\OneDrive\\vscode\\bot\\ai_bg.jpg")
        elif resolution[0]==1920 and resolution[1]==1080:
            image_path = os.path.join(self.base_path, "C:\\Users\\utkar\\OneDrive\\vscode\\bot\\ai_bg1.jpg")      
        else :
            image_path = os.path.join(self.base_path, "C:\\Users\\utkar\\OneDrive\\vscode\\bot\\ai_bg.jpg")
        pixmap_bg = QPixmap(image_path)
        label.setPixmap(pixmap_bg)
        self.setCentralWidget(label)
        self.feedback_label = QLabel("Click 'Start' to begin voice interaction", self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(QFont("Helvetica", 24))
        self.feedback_label.setStyleSheet("color: white;")
        self.feedback_label.setGeometry(382, 0, 600, 100)
        self.resize(pixmap_bg.width(), pixmap_bg.height())
        self.indicator = QLabel(self)
        self.indicator.setGeometry(530, 230, 300, 300)
        mic_image_path = os.path.join(self.base_path, "C:\\Users\\utkar\\OneDrive\\vscode\\bot\\mic00.png")
        pixmap_mic0 = QPixmap(mic_image_path)
        self.indicator.setStyleSheet("background-color:white ; border-radius: 150px;")
        self.indicator.setPixmap(pixmap_mic0)
        self.indicator.setAlignment(Qt.AlignCenter)
        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(450, 550, 150, 80)
        self.start_button.setFont(QFont("Helvetica", 32))
        self.start_button.setStyleSheet("background-color: green; color: white; border: none;")
        self.start_button.clicked.connect(self.start_voice_interaction)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(750, 550, 150, 80)
        self.stop_button.setFont(QFont("Helvetica", 32))
        self.stop_button.setStyleSheet("background-color: red; color: white; border: none;")
        self.stop_button.setDisabled(True)
        self.stop_button.clicked.connect(self.stop_voice_interaction)
        #godmod.exe
        self.setting_button = QPushButton("Settings for Models",self)
        self.setting_button.setGeometry(430, 120, 480, 80)
        self.setting_button.setFont(QFont("Helvetica", 42))
        self.setting_button.setStyleSheet("background-color: red; color: white; border: none;")
        self.setting_button.clicked.connect(self.open_settings)
        # Create a text area for interaction history
        self.history_text = QFrame(self)
        self.history_text.setGeometry(950, 80, 350, 650)
        self.history_text.setStyleSheet("background-color: rgba(0,0,0, 208);color: white;")
        self.history=QLabel("More Options".upper(), self.history_text)
        self.history.setAlignment(Qt.AlignCenter)
        self.history.setFont(QFont("Helvetica", 28))
        self.history.setStyleSheet("background-color: rgba(0,0,0, 0);color: red;")
        self.history.setGeometry(0, 10, 350, 100)
        settings_frame = QFrame(self)
        settings_frame.setGeometry(50, 80, 350, 650)
        settings_frame.setStyleSheet("background-color: rgba(0, 0, 0, 208);")
        self.options=QLabel("options".upper(), settings_frame)
        self.options.setAlignment(Qt.AlignCenter)
        self.options.setFont(QFont("Helvetica", 28))
        self.options.setStyleSheet("color: red;background-color: rgba(0, 0, 0, 00);")
        self.options.setGeometry(15, 10, 300, 80)
        # Create a settings button
        self.notes_button = QPushButton("Chat Notes",settings_frame)
        self.notes_button.setGeometry(50, 120, 240, 80)
        self.notes_button.setFont(QFont("Helvetica", 32))
        self.notes_button.setStyleSheet("background-color: orange; color: white; border: none;")
        self.notes_button.clicked.connect(self.show_notes)
        self.keyboard_button = QPushButton("Keyboard \nChat",settings_frame)
        self.keyboard_button.setGeometry(50, 240, 240, 140)
        self.keyboard_button.setFont(QFont("Helvetica", 32))
        self.keyboard_button.setStyleSheet("background-color: cyan; color: white; border: none;")
        self.keyboard_button.clicked.connect(self.SP_Search)
        self.settings_button1 = QPushButton("Show News",self.history_text)
        self.settings_button1.setGeometry(50, 120, 240, 80)
        self.settings_button1.setFont(QFont("Helvetica", 32))
        self.settings_button1.setStyleSheet("background-color: orange; color: white; border: none;")
        self.settings_button1.clicked.connect(self.show_news)
        self.news_button = QPushButton("Show \nWeather",self.history_text)
        self.news_button.setGeometry(50, 240, 240, 140)
        self.news_button.setFont(QFont("Helvetica", 32))
        self.news_button.setStyleSheet("background-color: cyan; color: white; border: none;")
        self.news_button.clicked.connect(self.show_weather)
        health_button = QPushButton("HealthGpt", self.history_text)
        health_button.setGeometry(50,420, 240, 80)
        health_button.setFont(QFont("Helvetica", 32))
        health_button.setStyleSheet("background-color: #240254; color: white; border: none;")
        health_button.clicked.connect(self.on_health_button_click)
        education_button = QPushButton("EduGpt", self.history_text)
        education_button.setGeometry(50,540, 240, 80)
        education_button.setFont(QFont("Helvetica", 32))
        education_button.setStyleSheet("background-color: Orchid; color: white; border: none;")
        education_button.clicked.connect(self.on_education_button_click)
        exit_button = QPushButton("APP Lookup", settings_frame)
        exit_button.setGeometry(50,420, 240, 80)
        exit_button.setFont(QFont("Helvetica", 32))
        exit_button.setStyleSheet("background-color: #240254; color: white; border: none;")
        exit_button.clicked.connect(self.on_applook_button_click)
        exit_button = QPushButton("Exit", settings_frame)
        exit_button.setGeometry(50,540, 240, 80)
        exit_button.setFont(QFont("Helvetica", 32))
        exit_button.setStyleSheet("background-color: Orchid; color: white; border: none;")
        exit_button.clicked.connect(self.on_exit_button_click)
        if resolution[0]in range(1200,1440) and resolution[1]in range(710,800):
                self.showFullScreen()
        elif resolution[0]==1920 and resolution[1]==1080:
            self.showFullScreen()
    def on_health_button_click(self):
        self.health.call()
    def on_applook_button_click(self):
        self.applook.call()
    def on_education_button_click(self):
        self.education.call()
    def SP_Search(self):
        Spotlight.exec(api)
    def show_notes(self):
        self.notes.call()
    def show_weather(self):
        self.weather.weather()
    def show_news(self):
        self.news.news()
    def open_settings(self):
        settings_dialog = SettingsDialog(self.voice_handler)
        settings_dialog.exec()
    def on_exit_button_click(self):
        self.stop_voice_interaction()
        exit()
    def start_voice_interaction(self):
        if not self.voice_handler.is_listening:
            
            self.update_feedback("Listening... Speak now")
            self.start_button.setDisabled(True)
            self.stop_button.setEnabled(True)
            mic_image_path = os.path.join(self.base_path, "C:\\Users\\utkar\\OneDrive\\vscode\\bot\\mic01.png")
            self.update_indicator(mic_image_path)
            self.voice_handler.start_listening(self.count)
            
            

    def stop_voice_interaction(self):
        if self.voice_handler.is_listening:
            self.update_feedback("Voice interaction stopped")
            self.start_button.setEnabled(True)
            self.stop_button.setDisabled(True)
            mic_image_path = os.path.join(self.base_path, "C:\\Users\\utkar\\OneDrive\\vscode\\bot\\mic02.png")
            self.update_indicator(mic_image_path)
            self.voice_handler.stop_listening()

    def update_feedback(self, message):
        self.feedback_label.setText(message)

    def update_indicator(self, pixpath):
        self.indicator.setPixmap(QPixmap(pixpath))

def voice_interaction():
        
        app = QApplication(sys.argv)
        window = VoiceBotGUI(VoiceInteractionHandler(api))
        window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    voice_interaction()  
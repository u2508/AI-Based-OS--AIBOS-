import sys, os, cv2
import threading,json,ALIAB as portal
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QStackedWidget, QFileDialog, QLineEdit)
from PyQt5.QtGui import QImage, QPixmap, QFont, QColor, QPalette, QBrush, QLinearGradient,QGradient
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from deepface import DeepFace

class FaceRecognitionThread(QThread):
    result_signal = pyqtSignal(bool)
    name_signal= pyqtSignal(str)

    def __init__(self, frame, images):
        super().__init__()
        self.frame = frame
        self.images = images

    def run(self):
        for label in self.images.keys():
            for img in self.images[label]:
                try:
                    result = DeepFace.verify(self.frame.copy(), img.copy())
                    if result['verified']:
                        self.result_signal.emit(True)
                        self.name_signal.emit(label)
                        return
                except Exception as e:
                    pass
                    #print(f"Error in DeepFace.verify: {e}")
        self.result_signal.emit(False)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EDITH - Stark Industries")
        self.setGeometry(100, 100, 900, 700)
        self.showFullScreen()
        self.setStyleSheet("background-color: #2c3e50;")

        # Create a gradient background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor(58, 123, 213))
        gradient.setColorAt(1.0, QColor(58, 213, 178))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Main layout
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_main_page())
        self.stacked_widget.addWidget(self.create_login_page())
        self.stacked_widget.addWidget(self.create_register_page())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def create_main_page(self):
        page = QWidget()

        title_label = QLabel("EDITH", page)
        title_label.setFont(QFont("Orbitron", 40, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)

        login_button = QPushButton("Login", page)
        register_button = QPushButton("Register", page)
        exit_button=QPushButton("Exit",page)
        self.style_button(login_button)
        self.style_button(register_button)
        self.style_button(exit_button)

        login_button.clicked.connect(self.login)
        register_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        exit_button.clicked.connect(exit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)
        button_layout.addWidget(exit_button)
        button_layout.setSpacing(20)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(button_layout)
        layout.setAlignment(Qt.AlignCenter)
        page.setLayout(layout)

        return page
    def login(self):
        self.stacked_widget.setCurrentIndex(1) 
        self.video_capture_widget.start_video()
    def create_login_page(self):
        page = QWidget()

        back_button = QPushButton("< Back", page)
        self.style_button(back_button)
        exit_button = QPushButton("Exit", page)
        self.style_button(exit_button)
        exit_button.clicked.connect(exit)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        self.video_capture_widget = VideoCaptureWidget()
        buttons=QHBoxLayout()
        buttons.addWidget(back_button)
        buttons.addSpacing(6)
        buttons.addWidget(exit_button)
        layout = QVBoxLayout()
        layout.addLayout(buttons)
        layout.addWidget(self.video_capture_widget)
        layout.setAlignment(Qt.AlignTop)
        page.setLayout(layout)

        return page
    def back(self):
        try:
            self.stacked_widget.setCurrentIndex(0)
            self.capture_dialog.close()  
        except AttributeError :
            self.stacked_widget.setCurrentIndex(0)
    def create_register_page(self):
        page = QWidget()
        back_button = QPushButton("< Back", page)
        self.style_button(back_button)
        exit_button = QPushButton("Exit", page)
        self.style_button(exit_button)
        exit_button.clicked.connect(exit)
        back_button.clicked.connect(self.back)

        buttons=QHBoxLayout()
        buttons.addWidget(back_button)
        buttons.addSpacing(6)
        buttons.addWidget(exit_button)
        layout = QVBoxLayout()
        layout.addLayout(buttons)

        name_label = QLabel("Name:", page)
        name_label.setFont(QFont("Orbitron", 16, QFont.Bold))
        name_label.setStyleSheet("color: white;")

        self.name_input = QLineEdit(page)
        self.name_input.setFixedSize(200, 30)
        self.name_input.setStyleSheet("font-size: 16px; padding: 5px;")

        self.upload_buttons = []
        self.uploaded_images = [None, None, None]
        for i in range(3):
            upload_button = QPushButton(f"Upload Picture {i+1}", page)
            self.style_button(upload_button)
            upload_button.clicked.connect(lambda checked, idx=i: self.upload_image(idx))
            self.upload_buttons.append(upload_button)

        capture_button = QPushButton("Capture Using Camera", page)
        self.style_button(capture_button)
        capture_button.clicked.connect(self.capture_images)

        register_button = QPushButton("Register", page)
        self.style_button(register_button)
        register_button.clicked.connect(self.register_user)

        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        for button in self.upload_buttons:
            layout.addWidget(button)
        layout.addWidget(capture_button)
        layout.addWidget(register_button)
        layout.setAlignment(Qt.AlignTop)
        page.setLayout(layout)

        return page

    def style_button(self, button):
        button.setFixedSize(200, 50)
        button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; 
                color: white; 
                font-size: 16px; 
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)

    def upload_image(self, index):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.upload_buttons[index].setText(f"Uploaded: {os.path.basename(file_name)}")
            self.upload_buttons[index].setStyleSheet("background-color: #2980b9; color: white;")
            self.uploaded_images[index] = cv2.imread(file_name)

    def capture_images(self):
        self.capture_dialog = CaptureDialog(self)
        self.capture_dialog.finished.connect(self.on_capture_finished)
        self.capture_dialog.show()

    def on_capture_finished(self, images):
        for i, img in enumerate(images):
            self.upload_buttons[i].setText(f"Captured Image {i+1}")
            self.upload_buttons[i].setStyleSheet("background-color: #2980b9; color: white;")
            self.uploaded_images[i] = img
        QTimer.singleShot(5000,self.register_user)
    def save_data(self,data):
        with open('details.json', 'w') as file:
            json.dump(data, file)
    
    def register_user(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a name.")
            return

        if any(img is None for img in self.uploaded_images):
            QMessageBox.warning(self, "Input Error", "Please upload or capture three images.")
            return
        
        dir=os.path.dirname(os.path.abspath(__file__))
        print(dir)
        directory = dir+"\\registered_users"
        user_dir = os.path.join(directory, name)
        os.makedirs(user_dir, exist_ok=True)
        for i, img in enumerate(self.uploaded_images):
            save_path = os.path.join(user_dir, f'image_{i+1}.jpg')
            cv2.imwrite(save_path, img)

        QMessageBox.information(self, "Success", "User registered successfully.")
        self.name_input.clear()
        for button in self.upload_buttons:
            button.setText(f"Upload Picture {self.upload_buttons.index(button) + 1}")
            button.setStyleSheet("background-color: #27ae60; color: white;")
        self.uploaded_images = [None, None, None]
        self.capture_dialog = DetailCaptureDialog(self)
        self.capture_dialog.finished.connect(self.save_data)
        self.capture_dialog.show()

class DetailCaptureDialog(QWidget):
    finished = pyqtSignal(dict)

    def __init__(self,name):
        super().__init__()
        self.name=name
        self.setWindowTitle("details dialog")
        self.setGeometry(250, 20, 900, 700)
        self.setStyleSheet("background-color: #2c3e50;")

        # Create a gradient background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor(58, 123, 213))
        gradient.setColorAt(1.0, QColor(58, 213, 178))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        self.phone_label = QLabel("phone:")
        self.phone_label.setFont(QFont("Orbitron", 16, QFont.Bold))
        self.phone_label.setStyleSheet("color: white;")
        
        self.address_label = QLabel("address:")
        self.address_label.setFont(QFont("Orbitron", 16, QFont.Bold))
        self.address_label.setStyleSheet("color: white;")
        self.pin_label = QLabel("pin:")
        self.pin_label.setFont(QFont("Orbitron", 16, QFont.Bold))
        self.pin_label.setStyleSheet("color: white;")
        self.phone_input = QLineEdit()
        self.phone_input.setFixedSize(200, 30)
        self.phone_input.setStyleSheet("font-size: 16px; padding: 5px;")
        self.address_input = QLineEdit()
        self.address_input.setFixedSize(200, 30)
        self.address_input.setStyleSheet("font-size: 16px; padding: 5px;")
        self.pin_input = QLineEdit()
        self.pin_input.setFixedSize(200, 30)
        self.pin_input.setStyleSheet("font-size: 16px; padding: 5px;")
        self.finish_button = QPushButton("Finish",self)
        self.style_button(self.finish_button)
        self.finish_button.clicked.connect(self.finish_capture)

        self.data = {}

        layout = QVBoxLayout()
        layout1=QHBoxLayout()
        layout1.addWidget(self.phone_label)
        layout1.addWidget(self.phone_input)
        layout2=QHBoxLayout()
        layout2.addWidget(self.address_label)
        layout2.addWidget(self.address_input)
        layout.addLayout(layout1,1)
        layout3=QHBoxLayout()
        layout3.addWidget(self.pin_label)
        layout3.addWidget(self.pin_input)
        layout.addLayout(layout2,1)
        layout.addLayout(layout3,1)
        
        layout.addWidget(self.finish_button)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def style_button(self, button):
        button.setFixedSize(200, 50)
        button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; 
                color: white; 
                font-size: 16px; 
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
    def finish_capture(self):
        self.data[self.name]={"phone":self.phone_input.text().strip(),"address":self.address_input.text().strip(),"pin":self.pin_input.text().strip()}
        self.finished.emit(self.data)
        self.close()
class CaptureDialog(QWidget):
    finished = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Capture Images")
        self.setGeometry(250, 20, 900, 700)
        self.setStyleSheet("background-color: #2c3e50;")

        # Create a gradient background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor(58, 123, 213))
        gradient.setColorAt(1.0, QColor(58, 213, 178))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(720, 600)
        self.video_label.setStyleSheet("border: 1px solid #ffffff; border-radius: 15px;")

        self.capture_button = QPushButton("Capture Image",self)
        self.style_button(self.capture_button)
        self.capture_button.clicked.connect(self.capture_image)

        self.finish_button = QPushButton("Finish",self)
        self.finish_button.hide()
        self.style_button(self.finish_button)
        self.finish_button.clicked.connect(self.finish_capture)

        self.images = []
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.finish_button)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def style_button(self, button):
        button.setFixedSize(200, 50)
        button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; 
                color: white; 
                font-size: 16px; 
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(720, 600, Qt.KeepAspectRatio)
            self.video_label.setPixmap(QPixmap.fromImage(p))

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret and len(self.images) < 3:
            self.images.append(frame)
            QMessageBox.information(self, "Captured", f"Captured image {len(self.images)}.")
        if len(self.images)==3:
            self.capture_button.hide()
            self.finish_button.show()
            
    def finish_capture(self):
        if len(self.images) != 3:
            QMessageBox.warning(self, "Capture Incomplete", "Please capture three images.")
            return

        self.cap.release()
        self.timer.stop()
        self.finished.emit(self.images)
        self.close()

class VideoCaptureWidget(QWidget):
    def __init__(self):
        super().__init__()
        dir=os.path.dirname(os.path.abspath(__file__))
        print(dir)
        directory = dir+"\\registered_users"
        self.images = {}
        for subdir in os.listdir(directory):
            user_dir = os.path.join(directory, subdir)
            print(subdir)
            images_list=[]
            if os.path.isdir(user_dir):
                for file in os.listdir(user_dir):
                    if file.endswith(('jpg', 'png', 'bmp')):
                        file_path = os.path.join(user_dir, file)
                        img = cv2.imread(file_path)
                        images_list.append(img)
                self.images[subdir]=images_list
        if not self.images:
            QMessageBox.critical(self, "Image Error", "Could not load reference images.")
            sys.exit(1)
        
        self.face_match = False
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.lock = threading.Lock()
        self.frame_skip = 60  # Configurable parameter for frame skipping
        self.count = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Face Recognition")
        
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(720, 500)
        self.video_label.setStyleSheet("border: 1px solid #ffffff; border-radius: 15px;")

        self.status_label = QLabel("", self)
        self.status_label.setGeometry(800,300,400,150)
        self.status_label.setFont(QFont("Orbitron", 20, QFont.Bold))
        self.status_label.setStyleSheet("background-color: red;color: white; padding: 10px;")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.status_indicator = QLabel("", self)
        self.status_indicator.setFixedSize(30, 30)
        self.status_indicator.setStyleSheet("background-color: gray; border-radius: 15px;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.status_indicator)
        layout.addWidget(self.status_label)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)


    def start_video(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "Camera Error", "Could not open camera.")
            sys.exit(1)
        self.timer.start(30)  # Update every 30 ms
        self.status_label.setText("Video started")
        self.status_indicator.setStyleSheet("background-color: gray; border-radius: 15px;")

    def stop_video(self):
        self.timer.stop()
        self.cap.release()
        self.video_label.clear()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.setText("Failed to capture frame, retrying please wait.")
            self.cap.release()
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            ret, frame = self.cap.read()
            if not ret:
                self.status_label.setText("Failed to access camera! Access Denied. Exiting Program.")
                sys.exit(1)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if self.count % self.frame_skip == 0 and len(faces) > 0:
            x, y, w, h = faces[0]  # Use the first detected face
            face_frame = frame[y:y+h, x:x+w]

            self.thread = FaceRecognitionThread(face_frame, self.images)
            self.thread.result_signal.connect(self.update_face_match)
            self.thread.name_signal.connect(self.proceding)
            self.thread.start()

        self.count += 1

        with self.lock:
            match_text = "MATCH!" if self.face_match else "NO MATCH!"
            color = (0, 255, 0) if self.face_match else (0, 0, 255)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        cv2.putText(frame, match_text, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
        self.display_image(frame)
    def proceding(self,data=""):
        self.name=data
        self.status_label.setText("welcome you are "+data)
        app.exit()
        #connectivity to other programs
        #by exit or hide of this program 
        # or imports of main program
    def next(self):
        landing_page = portal.MainWindow(self.name)
        landing_page.show()
        
    def display_image(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(720, 600, Qt.KeepAspectRatio)
        self.video_label.setPixmap(QPixmap.fromImage(p))

    def update_face_match(self, result):
        with self.lock:
            self.face_match = result
        self.status_label.setText("MATCH!" if result else "NO MATCH!")
        self.status_indicator.setStyleSheet(f"background-color: {'green' if result else 'red'}; border-radius: 15px;")

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        cv2.destroyAllWindows()
        QTimer.singleShot(5000,self.next)
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWidget()
    window.video_capture_widget.next()
    window.show()
    sys.exit(app.exec_())

import sys,shutil,shlex,os,psutil
from PyQt5.QtCore import Qt,QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QListWidget, QListWidgetItem,QHBoxLayout,QPushButton
from PyQt5.QtGui import QFont
import subprocess,platform
class WorkerThread(QThread):
    friendly_names_signal = pyqtSignal((list,dict))
    app_signal=pyqtSignal(str)
    def run(self):
        installed_apps = self.get_installed_apps()
        friendly_names = self.get_friendly_names(installed_apps)
        self.friendly_names_signal.emit(friendly_names,installed_apps)

    def get_friendly_names(self, apps):
        #friendly_names = ["Meteor Rush","Tic Tac Toe AI","Text to Speech","Opera Browser"]
        friendly_names=[]
        try:
            [self.app_signal.emit(i) for i in  friendly_names]
            for app_name in apps.keys():
                            friendly_names.append(app_name)
                            self.app_signal.emit(app_name)
            return sorted(friendly_names)
        except Exception as e:
            print(f"Error retrieving process information: {str(e)}")
            return []

    def get_installed_apps(self):
        processes= {
                "nearby share.exe": r"C:\Program Files\NearbyShare\nearby_share",
                "meteor rush.exe": r"C:\\Users\\utkar\\OneDrive\\vscode\\output\\Meteor Rush",
                "tic tac toe ai.exe": r"C:\\Users\\utkar\OneDrive\vscode\output\\Tic Tac Toe AI Version",
                "text to speech.exe": r"C:\\Users\\utkar\\AppData\\Local\\Programs\\Opera\\launcher",
            }
        for proc in psutil.process_iter(attrs=['name','exe']):
            if proc.info:
                processes[proc.info['name']]=proc.info['exe'] 
        return (processes)

class AppSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker_thread = WorkerThread()
        self.worker_thread.friendly_names_signal.connect(self.task_finished)
        self.worker_thread.app_signal.connect(self.display_info)
        self.worker_thread.start()

    def task_finished(self, friendly_names,dict):
        self.apps=friendly_names
        self.app_dict=dict
        self.status_label.setText(f"program initialisation complete")
        self.status_label.setStyleSheet("background-color: yellow;color: green;")
        self.entry_app.setEnabled(True)
        self.app_list_widget.setEnabled(True)
        self.entry_app.setPlaceholderText("enter app to search :-")
        self.app_list_widget.scrollToTop()
        
        
    def init_ui(self):
        # Labels and Entry
        self.entry_app = QLineEdit()
        self.entry_app.textChanged.connect(self.update_app_list)
        self.entry_app.setPlaceholderText("List of Installed Processes")

        # List widget for displaying information
        self.app_list_widget = QListWidget()
        
        self.app_list_widget.itemClicked.connect(self.open_app)

        # Status Label
        self.status_label = QLabel()
        self.status_label.setText("Please wait for program initialisation:-\nFetching installed processes")
        self.status_label.setFixedHeight(70)
        self.status_label.setStyleSheet("background-color: yellow ;color: red;")
        
        self.hide_button = QPushButton('Close \nPage', self)
        self.hide_button.setFont(QFont('Arial', 18))
        self.hide_button.setStyleSheet("background-color: green;")
        self.hide_button.clicked.connect(self.call)

        # Layout setup
        vbox = QVBoxLayout()
        vbox.addWidget(self.entry_app)
        vbox.addWidget(self.app_list_widget)
        self.entry_app.setEnabled(False)
        self.app_list_widget.setEnabled(False)
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(self.hide_button)

        vbox_main = QVBoxLayout(self)
        vbox_main.addLayout(hbox)
        vbox_main.addWidget(self.status_label)

        self.setWindowTitle("App Info Lookup")
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(200, 100, 1000, 600)
        
        
        # Apply styling
        self.setStyleSheet(
            "QWidget { background-color: yellow; }"
            "QLabel { font-size: 22px; color: white; margin-bottom: 5px; }"
            "QLineEdit { font-size: 26px; background-color: #282828; border: 1px solid #1E1E1E; padding: 20px; color: white; }"
            "QPushButton { font-size: 36px; background-color: #4CAF50; color: white; border: none; padding: 10px 20px; margin-top: 10px; }"
            "QPushButton:hover { background-color: #45a049; }"
            "QFrame { background-color: #ccc; }"
            "QListWidget { font-size: 20px; background-color: #1E1E1E; border: 1px solid #282828; margin-top: 10px; color: white; }"
        )

    def call(self):
        if self.isHidden()==True:
            self.show()
        else:
            if __name__ == '__main__':
                exit()
            else:
                self.hide()
    def update_app_list(self):
        keyword = self.entry_app.text().strip().lower()
        self.installed_apps=self.search(keyword)
        self.display_app_list(self.installed_apps)

    def clear_display(self):
        self.app_list_widget.clear()
        self.status_label.clear()
    def search(self,keyword=None):
        if keyword:
            return [app for app in self.apps if keyword in app.lower()]
        else:
            return self.apps
    def display_info(self, app):
        if app!="":
            item = QListWidgetItem(app)
            self.app_list_widget.addItem(item)
            self.app_list_widget.scrollToBottom()
    def display_app_list(self, apps):
        self.app_list_widget.clear()
        for app in apps:
            item = QListWidgetItem(app)
            self.app_list_widget.addItem(item)
    def open_app(self, item):
        app_name = item.text()
        path=self.app_dict[app_name]
        print (path)
        try:            
            subprocess.Popen([path])
            self.status_label.setText(f"Successful Opening of App Name :- {app_name}")
            
        except FileNotFoundError as e:
            
                # Fallback: Try to open the application with its name directly
                try:
                    app_path_direct = shutil.which(os.path.basename(app_name))
                    if app_path_direct is not None:
                        subprocess.Popen([app_path_direct])
                    else:
                        raise FileNotFoundError("2")
                except FileNotFoundError as e:
                    if int(str(e)) == 2:
                        # Fallback: Try to open the application with its name directly
                        try:
                            if platform.system().lower() == "windows":
                                subprocess.Popen(["start", "", shlex.quote(app_name)], shell=True)
                            else:
                                subprocess.Popen([app_name], shell=True)
                        except Exception as e:
                            self.status_label.setText(f"Error opening {app_name}: {str(e)}")
                            self.status_label.setStyleSheet("color: red;")
                    else:
                        self.status_label.setText(f"Error opening {app_name}: {str(e)}")
                        self.status_label.setStyleSheet("color: red;")
            
                except Exception as e:
                    self.status_label.setText(f"Error opening {app_name}: {str(e)}")
                    self.status_label.setStyleSheet("color: red;")
        except Exception as e:
            self.status_label.setText(f"Error opening {app_name}: {str(e)}")
            self.status_label.setStyleSheet("color: red;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppSearchApp()
    ex.call()
    
    sys.exit(app.exec_())

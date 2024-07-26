from PyQt5.QtGui import QFontDatabase,QFont,QImage,QPixmap,QPalette,QBrush,QPainter,QColor
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QMessageBox,QHBoxLayout,QSpacerItem,
    QToolBar, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton,QStatusBar, QStyleFactory)
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrintDialog
import sys,os
class WatermarkPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super(WatermarkPlainTextEdit, self).__init__(parent)
        #self.setReadOnly(True)
        #self.setAttribute(Qt.WA_TranslucentBackground)
    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        ironman_image = QPixmap('iron-man1.jpg').scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, ironman_image)
        
        super(WatermarkPlainTextEdit, self).paintEvent(event)
    def hidden(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(100, 20, 600, 600)
        self.path = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Create the editor
        layout = QVBoxLayout()
        self.editor = WatermarkPlainTextEdit()
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPointSize(12)
        self.editor.setFont(fixed_font)
        layout.addWidget(self.editor)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        # Create status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Create file toolbar
        file_toolbar = QToolBar("File")
        self.addToolBar(file_toolbar)

        # Create edit toolbar
        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setOrientation(Qt.Vertical) 
        self.addToolBar(Qt.LeftToolBarArea, edit_toolbar)

        # Create actions
        self.create_actions(file_toolbar, edit_toolbar)

        # Call update title method
        self.update_title()
        
        self.setStyleSheet(open('note_style.css').read())
        # Set Fusion style for a modern look
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        
    
    def create_actions(self, file_toolbar, edit_toolbar):
        """
        Create actions and add them to the specified toolbars.
        """
        container_widget = QWidget()
        container_layout = QHBoxLayout(container_widget)
        spacer = QSpacerItem(100, 50) 
        self.create_action(container_layout, "Open file", self.file_open,True)
          # Adjust the width and height of the spacer as needed
        # Adjust the width and height of the spacer as needed
        container_layout.addSpacerItem(spacer)
        self.create_action(container_layout, "Save As", self.file_saveas,True)
        container_layout.addSpacerItem(spacer)
        self.create_action(container_layout, "Print", self.file_print,True) 
        container_layout.addSpacerItem(spacer)
        self.create_action(container_layout, "Close", exit,True)
        container_layout.addSpacerItem(spacer)
        self.create_action(container_layout, "Close APP", self.call)
        container_layout.addSpacerItem(spacer)
        file_toolbar.addWidget(container_widget)
        # Edit Actions
        
        container_widget1 = QWidget()
        container_layout1 = QVBoxLayout(container_widget1) 
        self.create_action(container_layout1, "Undo", self.editor.undo)
        container_layout1.addSpacerItem(spacer)
        self.create_action(container_layout1, "Redo", self.editor.redo)
        container_layout1.addSpacerItem(spacer)
        self.create_action(container_layout1, "Cut", self.editor.cut,False)
        container_layout1.addSpacerItem(spacer)
        self.create_action(container_layout1, "Copy", self.editor.copy,False)
        container_layout1.addSpacerItem(spacer)
        self.create_action(container_layout1, "Paste", self.editor.paste,False)
        container_layout1.addSpacerItem(spacer)
        self.create_action(container_layout1, "Select all", self.editor.selectAll,False)
        container_layout1.addSpacerItem(spacer)
        edit_toolbar.addWidget(container_widget1)
        # Wrap text action
        self.wrap_action = self.create_action(container_layout, "Wrap text to window", self.edit_toggle_wrap)
        self.wrap_action.setCheckable(True)
        self.wrap_action.setChecked(True)

    def create_action(self, toolbar, text, slot,font_flag=False):
        """
        Create an action and add it to the specified toolbar, and connect it to the specified slot.
        """
        action = QPushButton(text, self)
        
        action.clicked.connect(slot)
        
        if font_flag==True:
            action.setFont(QFont("Century Schoolbook",25))
        else:
            action.setFont(QFont("arial",20))
        action.clicked.connect(slot)
        
        toolbar.addWidget(action)

        return action

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self, file=None):
        if file:
            path = file
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "All files (*);;PDF files (*.pdf);;DOCX files (*.docx);;DOC files (*.doc)")

        if path:
            try:
                with open(path, 'r',encoding='utf-8') as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()
                self.status.showMessage(f"Opened: {path}")
    def file_close(self,path=None):
        if path:
            self.editor.setPlainText("")
            self.status.showMessage(f"Closed: {path}")
        else:
            self.editor.setPlainText("")
            self.status.showMessage(f"NO File Opened: Error")
    def file_save(self):
        if self.path is None:
            return self.file_saveas()
        self._save_to_path(self.path)
        self.status.showMessage(f"Saved: {self.path}")

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "text files (*.txt);;DOCX files (*.docx);;DOC files (*.doc);;All files (*)")
        if not path:
            return
        self._save_to_path(path)
        self.status.showMessage(f"Saved As: {path}")

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - PyQt5 Notepad" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)

    def closeEvent(self, event):
        """
        Overridden close event to prompt the user if there are unsaved changes.
        """
        if self.editor.document().isModified():
            response = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you really want to quit?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if response == QMessageBox.Save:
                self.file_save()
            elif response == QMessageBox.Cancel:
                event.ignore()
    def call(self):
        if self.isHidden()==True:
                self.show()
        else:
            if __name__ == '__main__':
                exit()
            else:
                print('bt')
                self.editor.hidden()
                self.hide()
if __name__ == '__main__':
    app1 = QApplication(sys.argv)
    app1.setApplicationName("PyQt5-Note")
    window = MainWindow()
    window.call()
    sys.exit(app1.exec_())
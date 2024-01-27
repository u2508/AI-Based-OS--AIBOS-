from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QFileDialog, QMessageBox,
    QToolBar, QPlainTextEdit, QVBoxLayout, QWidget, QAction,
    QStatusBar, QStyleFactory)
from PyQt5.QtPrintSupport import QPrintDialog
import sys,os

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(100, 100, 800, 600)
        self.path = None

        # Create the editor
        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()
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
        self.addToolBar(edit_toolbar)

        # Create actions
        self.create_actions(file_toolbar, edit_toolbar)

        # Call update title method
        self.update_title()

        # Set Fusion style for a modern look
        QApplication.setStyle(QStyleFactory.create("Fusion"))


    def create_actions(self, file_toolbar, edit_toolbar):
        """
        Create actions and add them to the specified toolbars.
        """
        # File Actions
        self.create_action(file_toolbar, "Open file", self.file_open)
        self.create_action(file_toolbar, "Save", self.file_save)
        self.create_action(file_toolbar, "Save As", self.file_saveas)
        self.create_action(file_toolbar, "Print", self.file_print)
        self.create_action(file_toolbar, "Close file", self.file_close)
        self.create_action(file_toolbar, "Close APP", self.call)
        
        

        # Edit Actions
        self.create_action(edit_toolbar, "Undo", self.editor.undo)
        self.create_action(edit_toolbar, "Redo", self.editor.redo)
        self.create_action(edit_toolbar, "Cut", self.editor.cut)
        self.create_action(edit_toolbar, "Copy", self.editor.copy)
        self.create_action(edit_toolbar, "Paste", self.editor.paste)
        self.create_action(edit_toolbar, "Select all", self.editor.selectAll)

        # Wrap text action
        self.wrap_action = self.create_action(edit_toolbar, "Wrap text to window", self.edit_toggle_wrap)
        self.wrap_action.setCheckable(True)
        self.wrap_action.setChecked(True)

    def create_action(self, toolbar, text, slot):
        """
        Create an action and add it to the specified toolbar, and connect it to the specified slot.
        """
        action = QAction(text, self)
        action.triggered.connect(slot)
        toolbar.addAction(action)
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
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "PDF files (*.pdf);;DOCX files (*.docx);;DOC files (*.doc);;All files (*)")
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
                self.hide()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("PyQt5-Note")
    window = MainWindow()
    window.call()

    sys.exit(app.exec_())

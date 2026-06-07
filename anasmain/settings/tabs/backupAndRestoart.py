import guiTools, gui, gettext, zipfile
import sys
import os, shutil
from settings import settings_handler, app
from settings import language
import win32com.client
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
class GUIForThread(qt.QDialog):
    def __init__(self, p, path, choice):
        super().__init__(p)
        self.resize(500, 500)
        self.setWindowTitle(_("The process is being completed. Please wait..."))
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #e0e0e0;
                font-family: Arial;
            }
        """)
        self.thread = Thread(path, choice)
        self.thread.objects.finish.connect(self.onFinished)
        qt2.QThreadPool(self).start(self.thread)
        self.choice = choice
    def onFinished(self, state):
        if state:
            if self.choice == 0:
                qt.QMessageBox.information(self,_("Done"),_("The settings have been copied successfully."))
            else:
                mb=qt.QMessageBox(self)
                mb.setWindowTitle(_("settings updated"))
                mb.setText(_("you must restart the program to apply changes \n do you want to restart now?"))
                rn=mb.addButton(qt.QMessageBox.StandardButton.Yes)
                rn.setText(_("restart now"))
                rl=mb.addButton(qt.QMessageBox.StandardButton.No)
                rl.setText(_("restart later"))
                mb.exec()
                ex=mb.clickedButton()
                if ex==rn:
                    os.execl(sys.executable, sys.executable, *sys.argv)
                elif ex==rl:
                    self.close()
class Thread(qt2.QRunnable):
    def __init__(self, path, choice):
        super().__init__()
        self.path = path
        self.choice = choice
        self.objects = Objects()
    def run(self):
        if self.choice == 0:
            with zipfile.ZipFile(os.path.join(self.path, settings_handler.appName + ".zip"), "w") as zipf:
                for root, dirs, files in os.walk(os.path.join(os.getenv('appdata'), settings_handler.appName)):
                    for filename in files:
                        filePath = os.path.join(root, filename)
                        zipf.write(filePath, os.path.relpath(filePath, os.path.join(os.getenv('appdata'), settings_handler.appName)))
        else:
            shutil.rmtree(os.path.join(os.getenv('appdata'), settings_handler.appName))
            with zipfile.ZipFile(self.path) as zfile:
                zfile.extractall(os.path.join(os.getenv('appdata'), settings_handler.appName))
        self.objects.finish.emit(True)
class Objects(qt2.QObject):
    finish = qt2.pyqtSignal(bool)
class Restoar(qt.QWidget):
    def __init__(self, p):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
                font-family: Arial;
            }
            QPushButton {
                background-color: #0000AA; /* استخدام اللون الأزرق كما في شاشة الموت */
                color: #e0e0e0;
                padding: 6px;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #0000CC;
            }
        """)
        layout = qt.QVBoxLayout(self)
        self.createCopy = qt.QPushButton(_("Backup"))
        layout.addWidget(self.createCopy)
        self.createCopy.clicked.connect(self.onbackup)
        self.restoar = qt.QPushButton(_("Restore settings"))
        layout.addWidget(self.restoar)
        self.restoar.clicked.connect(self.onrestoar)
        self.p = p
    def onbackup(self):
        fileDialog = qt.QFileDialog(self.p)
        fileDialog.setFileMode(qt.QFileDialog.FileMode.Directory)
        if fileDialog.exec() == qt.QFileDialog.DialogCode.Accepted:
            GUIForThread(self, fileDialog.selectedFiles()[0], 0).exec()
    def onrestoar(self):
        fileDialog = qt.QFileDialog(self.p)
        if fileDialog.exec() == qt.QFileDialog.DialogCode.Accepted:
            GUIForThread(self, fileDialog.selectedFiles()[0], 1).exec()
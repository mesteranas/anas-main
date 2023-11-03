import guiTools
import sys
import os
from . import settings_handler
from . import language
import PyQt6.QtWidgets as qt
import sys
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
language.init_translation()
class settings (qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("settings"))
        layout=qt.QVBoxLayout()
        self.sectian=guiTools.listBook(layout,_("select sectian"))
        label=qt.QLabel(_("language"))
        self.language=qt.QComboBox()
        self.language.setAccessibleName(_("language"))
        self.language.addItems(language.lang().keys())
        languages = {index:language for language, index in enumerate(language.lang().values())}
        try:
            self.language.setCurrentIndex(languages[settings_handler.get("g","lang")])
        except Exception as e:
            self.language.setCurrentIndex(0)
        self.ExitDialog=qt.QCheckBox(_("Show exit dialog when exiting the program"))
        self.ExitDialog.setChecked(self.cbts(settings_handler.get("g","exitDialog")))
        self.ok=qt.QPushButton(_("OK"))
        self.ok.clicked.connect(self.fok)
        self.cancel=qt.QPushButton(_("cancel"))
        self.cancel.clicked.connect(self.fcancel)
        layout1=qt.QVBoxLayout()
        layout1.addWidget(label)
        layout1.addWidget(self.language)
        layout1.addWidget(self.ExitDialog)
        self.sectian.add(_("general"),layout1)
        layout.addWidget(self.ok)
        layout.addWidget(self.cancel)
        self.setLayout(layout)
    def fok(self):
        settings_handler.set("g","lang",str(language.lang()[self.language.currentText()]))
        settings_handler.set("g","exitDialog",str(self.ExitDialog.isChecked()))
        mb=qt.QMessageBox()
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
    def fcancel(self):
        self.close()
    def cbts(self,string):
        if string=="True":
            return True
        else:
            return False



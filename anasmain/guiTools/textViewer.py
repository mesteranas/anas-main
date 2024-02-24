import PyQt6.QtWidgets as qt
class TextViewer(qt.QDialog):
    def __init__(self,p,title,text):
        super().__init__(p)
        self.setWindowTitle(title)
        self.text=qt.QPlainTextEdit()
        self.text.setPlainText(text)
        self.text.setReadOnly(True)
        layout=qt.QVBoxLayout(self)
        layout.addWidget(self.text)
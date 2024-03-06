from MainWindow import *
import os

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'RoccoPyGUI.RFI.Interruzioni.1.0'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

app = QApplication([])
app.setWindowIcon(QIcon(os.path.join(basedir, "ICON.ico")))

wind = MainWindow()
wind.show()

app.exec()
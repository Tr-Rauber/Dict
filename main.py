import sys
from PySide6.QtWidgets import QApplication
from entrance import AuthWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    app.exec()
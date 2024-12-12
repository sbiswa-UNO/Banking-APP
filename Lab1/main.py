import sys
from PyQt6.QtWidgets import *
from screens import create_gui

def main():
    """creates the window for the app"""
    app = QApplication(sys.argv)
    window = create_gui()
    app.aboutToQuit.connect(window.saveData)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
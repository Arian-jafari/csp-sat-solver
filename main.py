import sys
from PyQt6.QtWidgets import QApplication
from ui import UI


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec())
    
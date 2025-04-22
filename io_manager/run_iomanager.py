from ui.iomanager_ui import IOManagerMainWindow
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication()
    window = IOManagerMainWindow()
    window.resize(600, 400)
    window.show()
    app.exec()
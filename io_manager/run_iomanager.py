from ui.iomanager_ui import IOManagerMainWindow
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication()
    window = IOManagerMainWindow()
    window.resize(1400, 800)
    window.show()
    app.exec()
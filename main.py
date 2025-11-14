import sys
import os
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("gayy-nft-factory")
    app.setApplicationVersion("1.0.0")

    # Create main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
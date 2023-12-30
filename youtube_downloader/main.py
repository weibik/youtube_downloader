import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QFileDialog
from GUI import YouTubeDownloaderApp
from downloader import download_file, download_with_progress
import os
import logging

# Set up logging
logging.basicConfig(filename='download.log', level=logging.INFO)


def main():
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

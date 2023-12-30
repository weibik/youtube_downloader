from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QFileDialog
from downloader import download_file, download_with_progress
from threading import Thread


class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YouTube Downloader")

        self.link_label = QLabel("YouTube Video URL:")
        self.link_entry = QLineEdit()

        self.option_label = QLabel("Download Option:")
        self.options = ['Video', 'Audio']
        self.option_combobox = QComboBox()
        self.option_combobox.addItems(self.options)

        self.output_label = QLabel("Output Folder:")
        self.output_entry = QLineEdit()
        self.output_button = QPushButton("Select Folder")
        self.output_button.clicked.connect(self.select_folder)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download)

        layout = QVBoxLayout()
        layout.addWidget(self.link_label)
        layout.addWidget(self.link_entry)
        layout.addWidget(self.option_label)
        layout.addWidget(self.option_combobox)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_entry)
        layout.addWidget(self.output_button)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.output_entry.setText(folder)

    def download(self):
        link = self.link_entry.text()
        selected_option = self.option_combobox.currentText()
        output_folder = self.output_entry.text()

        download_thread = Thread(target=download_file, args=(link, selected_option, output_folder))
        download_thread.start()

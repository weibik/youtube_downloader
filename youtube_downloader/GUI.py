from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
)
from downloader import download_file, download_with_progress, get_available_resolutions
from threading import Thread


class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("YouTube Downloader")

        self.link_label = QLabel("YouTube Video URL:")
        self.link_entry = QLineEdit()
        self.link_entry.editingFinished.connect(self.show_resolution_dialog)

        self.option_label = QLabel("Download Option:")
        self.options = ["Video", "Audio"]
        self.option_combobox = QComboBox()
        self.option_combobox.addItems(self.options)

        self.output_label = QLabel("Output Folder:")
        self.output_entry = QLineEdit()
        self.output_button = QPushButton("...", self)
        self.output_button.clicked.connect(self.select_folder)

        self.output_layout = QHBoxLayout()
        self.output_layout.addWidget(self.output_entry)
        self.output_layout.addWidget(self.output_button)

        self.resolutions_label = QLabel("Available Resolutions:")
        self.resolutions_list = QListWidget()

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_with_resolution)

        layout = QVBoxLayout()
        layout.addWidget(self.link_label)
        layout.addWidget(self.link_entry)
        layout.addWidget(self.option_label)
        layout.addWidget(self.option_combobox)
        layout.addWidget(self.output_label)
        layout.addLayout(self.output_layout)
        layout.addWidget(self.resolutions_label)
        layout.addWidget(self.resolutions_list)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.output_entry.setText(folder)

    def update_resolutions_list(self, resolutions):
        if resolutions:
            self.resolutions_list.clear()
            self.resolutions_label.setText("Available Resolutions:")

            for resolution in resolutions:
                item = QListWidgetItem(resolution)
                self.resolutions_list.addItem(item)
        else:
            self.resolutions_label.setText("No resolutions available.")

    def show_resolution_dialog(self):
        link = self.link_entry.text()
        selected_option = self.option_combobox.currentText()

        resolutions = [get_available_resolutions(link, selected_option)]

        fetcher_thread = Thread(target=self.update_resolutions_list, args=resolutions)
        fetcher_thread.start()

    def download_with_resolution(self):
        link = self.link_entry.text()
        selected_option = self.option_combobox.currentText()
        output_folder = self.output_entry.text()
        selected_resolution = self.resolutions_list.itemClicked

        download_thread = Thread(
            target=download_file,
            args=(link, selected_option, output_folder, selected_resolution),
        )
        download_thread.start()

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QFileDialog
from pytube import YouTube
from tqdm import tqdm
import os
import logging
from threading import Thread

# Set up logging
logging.basicConfig(filename='download.log', level=logging.INFO)


def download_with_progress(stream, output):
    with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc="Downloading") as progress_bar:
        stream.download(output, filename=stream.default_filename)
        progress_bar.update(progress_bar.total - progress_bar.n)


def download_video(link, selected_option, output_folder):
    try:
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Download video
        yt = YouTube(link)
        stream = None
        if selected_option == 'Video':
            stream = yt.streams.get_highest_resolution()
        elif selected_option == 'Audio':
            stream = yt.streams.filter(only_audio=True).first()
        else:
            logging.error("Invalid selection")

        if stream:
            # Download with progress bar
            download_with_progress(stream, output_folder)
            logging.info(f"Downloaded: {yt.title}")
        else:
            logging.error(f"No available stream for {selected_option}")

    except Exception as e:
        logging.error(f"Error downloading {link}: {str(e)}")


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

        download_thread = Thread(target=download_video, args=(link, selected_option, output_folder))
        download_thread.start()


def main():
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

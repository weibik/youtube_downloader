from tkinter import ttk

from pytube import YouTube
from tqdm import tqdm
from threading import Thread
import tkinter as tk
import logging
import click
import os

logging.basicConfig(filename='download.log', level=logging.INFO)


def download_with_progress(stream, output):
    with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc="Downloading") as progress_bar:
        stream.download(output, filename=stream.default_filename)
        progress_bar.update(progress_bar.total - progress_bar.n)


# Commented code allows to use command line instead of GUI.
# @click.command()
# @click.argument("link", required=True)
# @click.option("--file_format", default="audio", help="Specify the format (audio, video). Default is audio.")
# @click.option('--output', default='Download', help='Specify the output folder.')
def download_youtube(link, file_format, output):
    try:
        os.makedirs(output, exist_ok=True)

        yt = YouTube(link)
        print(f"Title: {yt.title}")
        print(f"Views: {yt.views}")

        if file_format == "audio":
            stream = yt.streams.filter(only_audio=True).first()
        elif file_format == "video":
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.first()

        print("Downloading...")
        download_with_progress(stream, output)
        logging.info(f"Downloaded: {yt.title}")
        click.echo("Download complete.")

    except Exception as e:
        logging.error(f"Error downloading {link}: {str(e)}")
        click.echo(f"Error: {str(e)}")


class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Downloader")

        self.link_label = tk.Label(master, text="YouTube Video URL:")
        self.link_label.pack()

        self.link_entry = tk.Entry(master, width=50)
        self.link_entry.pack()

        self.option_label = tk.Label(master, text="Download Option:")
        self.option_label.pack()

        self.options = ['Video', 'Audio']
        self.selected_option = tk.StringVar()
        self.option_combobox = ttk.Combobox(master, textvariable=self.selected_option, values=self.options)
        self.option_combobox.set(self.options[0])  # Set default value
        self.option_combobox.pack()

        self.output_label = tk.Label(master, text="Output Folder:")
        self.output_label.pack()

        self.output_entry = tk.Entry(master, width=50)
        self.output_entry.insert(0, "Download")
        self.output_entry.pack()

        self.download_button = tk.Button(master, text="Download", command=self.download)
        self.download_button.pack()

    def download(self):
        link = self.link_entry.get()
        selected_option = self.selected_option.get()
        output = self.output_entry.get()

        download_thread = Thread(target=download_youtube, args=(link, selected_option, output))
        download_thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

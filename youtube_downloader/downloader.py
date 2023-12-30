from tqdm import tqdm
import logging
from pytube import YouTube
import os


def download_with_progress(stream, output):
    with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc="Downloading") as progress_bar:
        stream.download(output, filename=stream.default_filename)
        progress_bar.update(progress_bar.total - progress_bar.n)


def download_file(link, selected_option, output_folder):
    try:
        os.makedirs(output_folder, exist_ok=True)
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

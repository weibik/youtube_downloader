from tqdm import tqdm
import logging
from pytube import YouTube
import os


def download_with_progress(stream, output):
    with tqdm(total=stream.filesize, unit="B", unit_scale=True, desc="Downloading") as progress_bar:
        stream.download(output, filename=stream.default_filename)
        progress_bar.update(progress_bar.total - progress_bar.n)


def download_file(link, selected_option, output_folder, resolution):
    try:
        os.makedirs(output_folder, exist_ok=True)
        yt = YouTube(link)
        stream = None

        if selected_option == "Video":
            stream = yt.streams.filter(type="video", resolution=resolution, file_extension="mp4").first()
        elif selected_option == "Audio":
            stream = yt.streams.filter(only_audio=True).first()
        else:
            logging.error("Invalid selection")

        if stream:
            download_with_progress(stream, output_folder)
            logging.info(f"Downloaded: {yt.title}")
        else:
            logging.error(f"No available stream for {selected_option} and resolution {resolution}")
    except Exception as e:
        print(f"Error getting available resolutions: {str(e)}")
        return []


def get_available_resolutions(link, selected_option):
    try:
        yt = YouTube(link)
        resolutions = set()

        if selected_option == "Video":
            for stream in yt.streams.filter(type="video"):
                if stream.resolution:
                    resolutions.add(stream.resolution)
        elif selected_option == "Audio":
            resolutions.add("Audio")

        return list(resolutions)
    except Exception as e:
        print(f"Error getting available resolutions: {str(e)}")
        return []

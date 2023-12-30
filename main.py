from pytube import YouTube
from tqdm import tqdm
import logging
import click
import os

logging.basicConfig(filename='download.log', level=logging.INFO)


def download_with_progress(stream, output):
    with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc="Downloading") as progress_bar:
        stream.download(output, filename=stream.default_filename)
        progress_bar.update(progress_bar.total - progress_bar.n)


@click.command()
@click.argument("link", required=True)
@click.option("--file_format", default="audio", help="Specify the format (audio, video). Default is audio.")
@click.option('--output', default='Download', help='Specify the output folder.')
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


if __name__ == "__main__":
    download_youtube()

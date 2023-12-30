**Prerequisites**
- poetry

**How to install poetry on windows?**
1. Install poetry (on windows powershell)\
      (Invoke-WebRequest -Uri ht<span>tps://install.python-poetry.org -UseBasicParsing).Content | py -)
2. add path to the windows environmental variables:\
      %APPDATA%\Python\Scripts

**Installation:**
1. Clone the repository:
  https://github.com/weibik/youtube_downloader.git
2. Navigate to project directory 
  cd youtube_downloader
3. Run program
   **poetry run python main.py --link {link} --file_format {format} --output {output}**
   link = link to the youtube video
   format = audio/video
   output = target folder for downloaded file

**Example**
poetry run python main.py --file_format video --output test_folder "https://www.youtube.com/watch?v=79V37mWV6nM&ab_channel=MagiaNatury"

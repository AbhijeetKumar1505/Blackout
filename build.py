import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'app.py',
    '--name=BlackoutPrank',
    '--onefile',
    '--windowed',
    f'--add-data={os.path.join(current_dir, "static/your-sound-file.mp3")};static/your-sound-file.mp3',
    '--icon=NONE'
]) 
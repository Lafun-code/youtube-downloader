import os
import yt_dlp
from datetime import datetime
import pickle

# FFmpeg path constant
FFMPEG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg.exe')

# Constants for quality selections
QUALITY_SELECTIONS = {
    "1": 'bestvideo+bestaudio/best',  # Highest quality
    "2": '18',  # SD quality
    "3": 'bestaudio'  # Audio only (MP3)
}

# Load the last used folder
def load_last_folder():
    try:
        with open('last_folder.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return ""  # Return empty if file is not found

# Save the last used folder
def save_last_folder(folder_path):
    with open('last_folder.pkl', 'wb') as f:
        pickle.dump(folder_path, f)

# Validate if the quality selection is valid
def validate_quality_selection(kalite_secimi):
    return QUALITY_SELECTIONS.get(kalite_secimi)

# Create the output file path
def create_output_path(kaydetme_yolu, dosya_adi):
    return os.path.join(kaydetme_yolu, dosya_adi)

# Start the download and return result message
def download_video(video_link, format_secimi, output_path, progress_hook, update_date_hook):
    # Add a timestamp to the start of the download if a hook is provided
    if update_date_hook:
        download_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_date_hook(download_start_time)

    ydl_opts = {
        'format': format_secimi,
        'outtmpl': output_path,
        'merge_output_format': 'mp4' if format_secimi != 'bestaudio' else 'mp3',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}
        ] if format_secimi == 'bestaudio' else [],
        'ffmpeg_location': FFMPEG_PATH,
        'progress_hooks': [progress_hook] if progress_hook else []
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])
        return "✅ İndirme tamamlandı!"
    except Exception as e:
        return f"❌ Bir hata oluştu: {str(e)}"

# Main function: Handles video download based on user input
def youtube_video_indir_gui(video_link, kalite_secimi, kaydetme_yolu, progress_hook=None, update_date_hook=None):
    if not video_link or not kaydetme_yolu:
        return "Hata: Eksik bilgi!"

    format_secimi = validate_quality_selection(kalite_secimi)
    if not format_secimi:
        return "Hata: Geçerli bir kalite seçimi yapmadınız!"

    dosya_adi = '%(title)s.%(ext)s'  # Template for the file name (video title + extension)
    output_path = create_output_path(kaydetme_yolu, dosya_adi)

    # Start the video download
    return download_video(video_link, format_secimi, output_path, progress_hook, update_date_hook)

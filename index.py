from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    download_format = request.form['format']  # Get the selected format (video or audio)
    
    try:
        # Set download options based on the selected format
        if download_format == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',  # Extract the audio and convert to mp3
                    'preferredquality': '192',
                }],
            }
        else:
            # Default to video download
            ydl_opts = {
                'format': 'best',
                'outtmpl': '%(title)s.%(ext)s',
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info_dict)
            # If audio is selected, change extension to '.mp3'
            if download_format == 'audio':
                video_file = video_file.rsplit('.', 1)[0] + '.mp3'

            return send_file(video_file, as_attachment=True)
    
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)

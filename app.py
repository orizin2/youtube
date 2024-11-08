import os
import uuid
from flask import Flask, render_template, request, send_file
import yt_dlp

app = Flask(__name__)

# ダウンロード先のディレクトリ
DOWNLOAD_FOLDER = './downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


# 動画ダウンロードの設定
def download_video(url, output_path, quality):
    # 画質設定のマッピング
    if quality == 'best':
        format_option = 'bestvideo+bestaudio/best'
    elif quality == '1080p':
        format_option = 'bestvideo[height<=1080]+bestaudio/best'
    elif quality == '720p':
        format_option = 'bestvideo[height<=720]+bestaudio/best'
    elif quality == '480p':
        format_option = 'bestvideo[height<=480]+bestaudio/best'
    elif quality == '360p':
        format_option = 'bestvideo[height<=360]+bestaudio/best'
    else:
        format_option = 'bestvideo+bestaudio/best'

    ydl_opts = {
        'format': format_option,
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'ffmpeg_location': r'C:\Users\takut\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin',
        # FFmpeg のフルパスを指定
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    if request.method == 'POST':
        video_url = request.form.get('url')
        quality = request.form.get('quality')

        if not video_url:
            error_message = "URLを入力してください。"
        else:
            video_name = f"{uuid.uuid4()}.mp4"
            output_path = os.path.join(DOWNLOAD_FOLDER, video_name)

            try:
                # 動画のダウンロード
                download_video(video_url, output_path, quality)
                return send_file(output_path, as_attachment=True)

            except Exception as e:
                error_message = f"エラーが発生しました: {str(e)}"

    return render_template('index.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)

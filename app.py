import os
from io import BytesIO
from pytube import YouTube
from youtubesearchpython import VideosSearch
from flask import Flask,render_template, url_for, request, send_file, redirect


app = Flask(__name__)

@app.route('/',methods = ["GET","POST"])
def index():
    if request.method == 'POST':
        link = request.form.get('query')
        ytsearch = VideosSearch(link,limit=20).result()['result']
        if len(ytsearch) == 0:
            print('Error')

        return render_template('result.html',data=ytsearch)

    else:
        return render_template('index.html')


@app.route('/download',methods = ['POST'])
def download():
    if request.method == 'POST':
        link = request.form.get('dmusic')
        title = request.form.get('judul')
        yt = YouTube(link)
        buffer = BytesIO()
        out = title + ".mp3"
        video = yt.streams.filter(only_audio=True).first()
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        send = send_file(buffer,as_attachment=True,download_name=out,mimetype='audio/mp3')

        return send


    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

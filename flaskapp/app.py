from flask import Flask, render_template, Response
from util import interview, audio_transcript_complete, getTranscript

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(interview(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/transcript_complete')
def transcript_complete():
    if audio_transcript_complete():
        return Response("Audio transcript complete", status=201)
    else:
        return Response("Audio transcript in progress", status=102)


@app.route('/transcription')
def transcription():
    return getTranscript()


if __name__ == "__main__":
    app.run(debug=True)

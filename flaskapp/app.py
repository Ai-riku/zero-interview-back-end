from flask import Flask, render_template, Response
from flask_mysqldb import MySQL
from util import interview, audio_transcript_complete, getTranscript

import config

app = Flask(__name__)

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)


@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        print(user)
    cursor.close()
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

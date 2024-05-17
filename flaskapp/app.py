from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from util import getTranscript, convert_to_mp4, extract_audio
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']

app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

mysql = MySQL(app)

# Allow all origins
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('message')
def handle_message(message):
    print('Received message: ' + message)
    if message == 'Transcript requested':
        transcript = getTranscript()
        emit('transcript', transcript)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    try:
        # Generate and emit transcript
        convert_to_mp4(os.environ["TEMP_VIDEO_PATH"], os.environ["VIDEO_PATH"])
        extract_audio(os.environ["VIDEO_PATH"], os.environ["AUDIO_PATH"])
        transcript = getTranscript()
        socketio.emit('transcript', transcript)
        return jsonify({
            "message": "File uploaded and converted to mp4 successfully",
            "file": os.environ["VIDEO_PATH"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in {'webm', 'mp4'}


if __name__ == "__main__":
    app.run(debug=True, port=5000)

from __future__ import print_function, division
from moviepy.editor import VideoFileClip, AudioFileClip

import cv2
import pyaudio
import wave
import threading
import time
import os
import config

class VideoRecorder():  
    def __init__(self, name=config.temp_video_path, camindex=0, fourcc="MJPG"):
        self.open = True
        self.device_index = camindex
        self.video_filename = name
        self.video_cap = cv2.VideoCapture(self.device_index)
        self.frame_width = int(self.video_cap.get(3))
        self.frame_height = int(self.video_cap.get(4)) 
        self.frameSize = (self.frame_width, self.frame_height) 
        self.current_frame = None
        self.fps = self.video_cap.get(cv2.CAP_PROP_FPS)
        self.video_writer = cv2.VideoWriter_fourcc(*fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.frame_counts = 1
        self.start_time = time.time()

    def record(self):
        while self.open:
            ret, video_frame = self.video_cap.read()
            if not ret: break
            self.video_out.write(video_frame)
            self.current_frame = video_frame
            self.frame_counts += 1
                
    def stop(self):
        if self.open:
            self.open=False
            self.video_out.release()
            self.video_cap.release()
            cv2.destroyAllWindows()

    def start(self):
        video_thread = threading.Thread(target=self.record)
        video_thread.start()

class AudioRecorder():
    def __init__(self, filename=config.audio_path, rate=44100, fpb=1024, channels=2):
        self.open = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.audio_filename = filename
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []

    def record(self):
        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer) 
            self.audio_frames.append(data)
            if not self.open:
                break

    def stop(self):
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

def start_AVrecording():
    global video_thread
    global audio_thread
    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()
    audio_thread.start()
    video_thread.start()
    return video_thread

def start_video_recording(filename="test"):
    global video_thread
    video_thread = VideoRecorder()
    video_thread.start()
    return filename

def start_audio_recording(filename="test"):
    global audio_thread
    audio_thread = AudioRecorder()
    audio_thread.start()
    return filename

def stop_AVrecording(filename="test"):
    audio_thread.stop() 
    frame_counts = video_thread.frame_counts
    elapsed_time = time.time() - video_thread.start_time
    recorded_fps = frame_counts / elapsed_time
    print("total frames " + str(frame_counts))
    print("elapsed time " + str(elapsed_time))
    print("recorded fps " + str(recorded_fps))
    video_thread.stop() 

    # Makes sure the threads have finished
    while threading.active_count() > 3:
        time.sleep(1)
    
    # Merging audio and video signal    
    video_file_path = config.temp_video_path
    audio_file_path = config.audio_path
    video_clip = VideoFileClip(video_file_path).set_fps(recorded_fps)
    audio_clip = AudioFileClip(audio_file_path)
    synchronized_clip = video_clip.set_audio(audio_clip)
    synchronized_clip.write_videofile(filename, codec="libx264", audio_codec="aac")

def file_manager(filepath="test"):
    if os.path.exists(config.temp_video_path):
        os.remove(config.temp_video_path)

def video_capture():
    record_duration = 5.0
    start_AVrecording()
    start_time = time.time()
    while (time.time() - start_time) < record_duration:
        frame = video_thread.current_frame
        if frame is not None:
            ret, buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    stop_AVrecording(config.video_path)
    file_manager()



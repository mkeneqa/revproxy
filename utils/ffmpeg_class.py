import subprocess


class FFMpeg:
    def __init__(self, file_in, file_out):
        self.file_in = file_in
        self.file_out = file_out

    def run(self, start_time, time_duration):
        process = subprocess.Popen([
            "/usr/local/bin/ffmpeg",
            "-ss", str(start_time),
            "-i", self.file_in,
            "-vcodec prores -profile:v 0",
            "-acodec pcm_s16le",
            "-to", str(time_duration),
            "-c", "copy", self.file_out
        ])

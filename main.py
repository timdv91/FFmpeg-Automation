from myModules.FFmpeg import FFmpeg

ffmpeg = FFmpeg("ultrafast")
isSuccess = ffmpeg.runTranscoding("test_1.mp4", "output.mkv")
print(isSuccess)
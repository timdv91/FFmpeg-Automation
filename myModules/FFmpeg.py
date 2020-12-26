import subprocess
import pexpect

class FFmpeg():
    def __init__(self, pPreset = "slow", pCrf = 22, pInFile = None, pOutFile = None):
        self.preset = pPreset
        self.crf = str(pCrf)
        self.inFile = pInFile
        self.outFile = pOutFile

    def runTranscoding(self, pInFile = None, pOutFile = None):
        if(pInFile == None): pInFile = self.inFile
        if(pOutFile == None): pOutFile = self.outFile

        if(pInFile == None or pOutFile == None):
            print("ERROR")
            return False

        # Get the amount of frames inside this video file:
        totalFrameCount = self._getVideofileFrameCount(pInFile)
        if totalFrameCount == -1:
            return False            # when framecount is -1 transcoding is aborted, False is returned to prevent file deletion.

        # start transcoding the video file.
        retValue = self._setVideofileTranscoding(pInFile, pOutFile, totalFrameCount)
        return retValue

    def _getVideofileFrameCount(self, pInFile):
        cmdArr_ffprobe = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames", "-of", "default=nokey=1:noprint_wrappers=1", pInFile]

        # ffprobe is the default way to determine the amount of frames in a file, if it doesn't work fall back to ffmpeg.
        try:
            result = subprocess.run(cmdArr_ffprobe, stdout=subprocess.PIPE)
            if (result.stdout.decode('utf-8') == "N/A"):
                framesTotal = int(result.stdout.decode('utf-8'))
                return framesTotal

            # ffmpeg fallback for frame counting
            else:
                result = subprocess.getoutput("ffmpeg -i " + pInFile + " -map 0:v:0 -c copy -f null -")

                # ffmpeg returns a huge amount of text, we need the frame count after the "frame=" text.
                # The "frame=" text is printed multiple times when ffmpeg is calculating the amount of frames, we need the
                # last print with largest number for processing.

                while "frame=" in result:
                    i = result.find("frame=")
                    result = result[i+1:]
                result = result.split(" ")[0].split("=")[1]
                return int(result)

        except Exception:
            return -1



    def _setVideofileTranscoding(self, pInFile, pOutFile, pTotalFrameCount):
        cmd = "ffmpeg -i " + pInFile + " -c:v libx265 -preset " + self.preset + " -x265-params crf=" + self.crf + " -c:a aac -b:a 128k " + pOutFile
        thread = pexpect.spawn(cmd)
        print("started %s" % cmd)
        cpl = thread.compile_pattern_list([pexpect.EOF, "frame= *\d+", '(.+)'])

        try:
            isSuccess = False
            while True:
                i = thread.expect_list(cpl, timeout=None)
                if i == 0:  # EOF
                    print(pTotalFrameCount, "/", pTotalFrameCount, "|", "100%")
                    print("Conversion completed. the sub process exited")
                    isSuccess = True
                    break
                elif i == 1:
                    frame_number = thread.match.group(0).decode('utf-8')

                    perc = round(float(float(int(frame_number.split('=')[1]) / pTotalFrameCount) * 100), 2)
                    print(frame_number, "/", pTotalFrameCount, "|", perc, "%")
                    thread.close
                elif i == 2:
                    # unknown_line = thread.match.group(0)
                    # print unknown_line
                    pass
            return isSuccess

        except Exception:
            return False


# Example:
'''
ffmpeg = FFmpeg("ultrafast")
isSuccess = ffmpeg.runTranscoding("test_1.mp4", "output.mkv")
print(isSuccess)
'''
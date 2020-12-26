import subprocess
import pexpect

class FFmpeg():
    def __init__(self, pPreset = "slow", pInFile = None, pOutFile = None):
        self.preset = pPreset
        self.inFile = pInFile
        self.outFile = pOutFile

    def runTranscoding(self, pInFile = None, pOutFile = None):
        if(pInFile == None): pInFile = self.inFile
        if(pOutFile == None): pOutFile = self.outFile

        if(pInFile == None or pOutFile == None):
            print("ERROR")
            return False

        totalFrameCount = self._getVideofileFrameCount(pInFile)
        retValue = self._setVideofileTranscoding(pInFile, pOutFile, totalFrameCount)
        return retValue

    def _getVideofileFrameCount(self, pInFile):
        cmdArr = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames", "-of", "default=nokey=1:noprint_wrappers=1", pInFile]
        result = subprocess.run(cmdArr, stdout=subprocess.PIPE)
        print(result.stdout)
        framesTotal = int(result.stdout.decode('utf-8'))
        return framesTotal

    def _setVideofileTranscoding(self, pInFile, pOutFile, pTotalFrameCount):
        cmd = "ffmpeg -i " + pInFile + " -c:v libx265 -preset " + self.preset + " -x265-params crf=22 -c:a aac -b:a 128k " + pOutFile
        thread = pexpect.spawn(cmd)
        print("started %s" % cmd)
        cpl = thread.compile_pattern_list([pexpect.EOF, "frame= *\d+", '(.+)'])

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


# Example:
'''
ffmpeg = FFmpeg("ultrafast")
isSuccess = ffmpeg.runTranscoding("test_1.mp4", "output.mkv")
print(isSuccess)
'''
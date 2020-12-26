from myModules.FolderCrawler import FolderCrawler
from myModules.FFmpeg import FFmpeg
import os

class main():
    def __init__(self):
        videoFileList = self.runFolderCrawler()
        self.runFFmpeg(videoFileList)

    def runFolderCrawler(self):
        fc = FolderCrawler()
        fc.setFolderStructureScan('/home/tim/Desktop/Avenue.5')

        print("\nScanning folderstructure for video files: ")
        print("==================================================================")
        filteredFileList = fc.getFolderStructureOnFilesize(100000)
        for video in filteredFileList:
            print(video)

        print("Crawler detected ", len(filteredFileList), " video files.")
        return filteredFileList


    def runFFmpeg(self, pVideoFileList):
        ffmpeg = FFmpeg("ultrafast")
        for videoFilePath in pVideoFileList:
            isSuccess = ffmpeg.runTranscoding(videoFilePath, videoFilePath[:-4] + "__TDV-H265__.mkv")
            if (isSuccess):
                print("Transcoding of file completed, removing original file. ", end=" ")
                #os.remove(videoFilePath)
                print("Done.")

        print("FFmpeg completed running. ")


main()
from myModules.FolderCrawler import FolderCrawler
from myModules.FFmpeg import FFmpeg
import os

class main():
    def __init__(self):
        videoFileList = self.runFolderCrawler()
        #self.runFFmpeg(videoFileList)

    def runFolderCrawler(self):
        # scan folderstructure for all files (also in subdirs)
        fc = FolderCrawler()
        fc.setFolderStructureScan('/home/tim/Desktop/Avenue.5')

        # scan folderstructure for video files (all files larger than 100MB):
        print("\nScanning folderstructure for video files: ")
        print("==================================================================")
        filteredFileList = fc.getFolderStructureOnFilesize(100000)
        for video in filteredFileList:
            print("\t ", video)
        print("\nCrawler detected ", len(filteredFileList), " video files.")

        # remove files containing __TDV-H265__ in filename as these have previously been transcoded.
        print("Scanning previously detected video files for non transcoded video files: ")
        print("==================================================================")
        fc.setFolderStructureVar(filteredFileList)
        filteredFileList = fc.getFolderStructureFilteredOnString("__TDV-H265__")
        for video in filteredFileList:
            print("\t ", video)
        print("Crawler detected ", len(filteredFileList) , " non transcoded video files. ")

        return filteredFileList


    def runFFmpeg(self, pVideoFileList):
        ffmpeg = FFmpeg(pPreset="ultrafast", pCrf=22)
        for videoFilePath in pVideoFileList:
            isSuccess = ffmpeg.runTranscoding(videoFilePath, videoFilePath[:-4] + "__TDV-H265__.mkv")
            if (isSuccess):
                print("Transcoding of file completed, removing original file. ", end=" ")
                os.remove(videoFilePath)
                print("Done.")

        print("FFmpeg completed running. ")


main()
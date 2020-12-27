from myModules.FolderCrawler import FolderCrawler
from myModules.FFmpeg import FFmpeg
import os
import sys

class main():
    def __init__(self, pArgs):
        self.setArguments(pArgs)
        videoFileList = self.runFolderCrawler()
        self.runFFmpeg(videoFileList)

    def setArguments(self, pArgs):
        self.path = ""
        self.crf = "0"
        self.preset = "medium"
        self.minFileSizeKB = 100000 #100MB
        self.maxFileSizeKB = None

        for arg in pArgs:
            arg = str(arg)
            if ("--path=" in arg):
                self.path = arg[7:]
            if ("--preset=" in arg):
                self.preset = arg[9:]
            if ("--crf=" in arg):
                self.crf = arg[6:]
            if ("--minfilesize=" in arg):
                self.minFileSizeKB = arg[14:]
            if ("--maxfilesize=" in arg):
                self.maxFileSizeKB = arg[14:]

        if(self.path == ""):
            print("Please provide a folder path!")
            quit()

        print(self.path)
        print(self.crf)
        print(self.preset)
        print(self.minFileSizeKB)
        print(self.maxFileSizeKB)

    def runFolderCrawler(self):
        # scan folderstructure for all files (also in subdirs)
        fc = FolderCrawler()
        fc.setFolderStructureScan(self.path)

        # scan folderstructure for video files (all files larger than 100MB):
        print("\nScanning folderstructure for video files: ")
        print("==================================================================")
        filteredFileList = fc.getFolderStructureOnFilesize(self.minFileSizeKB, self.maxFileSizeKB)
        for video in filteredFileList:
            print("\t ", video)
        print("Crawler detected ", len(filteredFileList), " video files.")

        # remove files containing __TDV-H265__ in filename as these have previously been transcoded.
        print("\nScanning previously detected video files for non transcoded video files: ")
        print("==================================================================")
        fc.setFolderStructureVar(filteredFileList)
        filteredFileList = fc.getFolderStructureFilteredOnString("__TDV-H265__")
        for video in filteredFileList:
            print("\t ", video)
        print("Crawler detected ", len(filteredFileList) , " non transcoded video files. \n")

        return filteredFileList


    def runFFmpeg(self, pVideoFileList):
        ffmpeg = FFmpeg(pPreset=self.preset, pCrf=self.crf)
        counter = 0
        for videoFilePath in pVideoFileList:
            counter += 1
            additionalTextToPrint = "\t||\t\tfile " + str(counter) + "/" + str(len(pVideoFileList)) + " | FilePath: " + videoFilePath
            isSuccess = ffmpeg.runTranscoding(videoFilePath, videoFilePath[:-4] + "__TDV-H265__.mkv", additionalTextToPrint)
            if (isSuccess):
                print("Transcoding of file completed, removing original file. ", end=" ")
                os.remove(videoFilePath)
                print("Done.")

        print("FFmpeg completed running. ")


main(sys.argv)
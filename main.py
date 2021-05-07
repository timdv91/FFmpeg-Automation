from myModules.FolderCrawler import FolderCrawler
from myModules.FFmpeg import FFmpeg
from myModules.cmdColor import bcolors
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
                self.minFileSizeKB = int(arg[14:])
            if ("--maxfilesize=" in arg):
                self.maxFileSizeKB = int(arg[14:])

        if(self.path == ""):
            print("Please provide a folder path!")
            quit()

        print("Path: " + self.path)
        print("CRF: " + self.crf)
        print("Preset: " + self.preset)
        print("Minimum input video filesize: " + str(self.minFileSizeKB))
        print("Maximum input video filesize: " + str(self.maxFileSizeKB))

        print('Continue with these settings? (Y/N)')
        x = input()
        if(x == "N" or x == "n"):
            quit()


    def runFolderCrawler(self):
        # scan folderstructure for all files (also in subdirs)
        fc = FolderCrawler()
        fc.setFolderStructureScan(self.path)

        # scan folderstructure for video files (all files larger than xxxMB):
        print("\nScanning folderstructure for video files: ")
        print("==================================================================")
        filteredFileList = fc.getFolderStructureOnFilesize(self.minFileSizeKB, self.maxFileSizeKB)
        for video in filteredFileList:
            print("\t ", video)
        print("Crawler detected ", len(filteredFileList), " video files.")

        # scan folderstructure for spaces in filepath (spaces make ffmpeg crash apparently):
        fileList = fc.getFolderStructureOnFilesize(self.minFileSizeKB, self.maxFileSizeKB)
        for file in fileList:
            if(" " in file):
                print("\nWarning spaces detected in filepath, software will replace all spaces in filenames and filepaths with '.' ! Continue? (Y/N)")
                x = input()
                if(x == "N" or x == "n"):
                    quit()
                else:
                    fc.setFolderStructureSpacesReplacement('.', self.minFileSizeKB, self.maxFileSizeKB)
                    fc.setFolderStructureScan(self.path)  # rescan folders for files now filenames have changed.
                    filteredFileList = fc.getFolderStructureOnFilesize(self.minFileSizeKB, self.maxFileSizeKB)  # re-filter for files inbetween certain filesizes
                    break

        # remove files containing __TDV-H265__ in filename as these have previously been transcoded.
        print("\nScanning previously detected video files for non transcoded video files: ")
        print("==================================================================")
        fc.setFolderStructureVar(filteredFileList)
        filteredFileList = fc.getFolderStructureFilteredOnString("__TDV-H265__")
        for video in filteredFileList:
            print("\t ", video)
        print("Crawler detected ", len(filteredFileList) , " non transcoded video files. \n")

        print('Continue? (Y/N)')
        x = input()
        if(x == "N" or x == "n"):
            quit()

        return filteredFileList


    def runFFmpeg(self, pVideoFileList):
        ffmpeg = FFmpeg(pPreset=self.preset, pCrf=self.crf)
        counter = 0
        for videoFilePath in pVideoFileList:
            counter += 1
            additionalTextToPrint = bcolors.OKBLUE + "file " + str(counter) + "/" + str(len(pVideoFileList)) + bcolors.ENDC + " | FilePath: " + videoFilePath
            isSuccess = ffmpeg.runTranscoding(videoFilePath, videoFilePath[:-4] + "__TDV-H265__.mkv", additionalTextToPrint)
            if (isSuccess):
                print("Transcoding of file completed, removing original file. ", end=" ")
                os.remove(videoFilePath)
                print("Done.")
            else:
                print("ERROR")

        print("FFmpeg completed running. ")


main(sys.argv)
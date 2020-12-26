from myModules.FolderCrawler import FolderCrawler
from myModules.FFmpeg import FFmpeg

class main():
    def __init__(self):
        self.runFolderCrawler()
        #self.runFFmpeg()

    def runFolderCrawler(self):
        fc = FolderCrawler()
        fc.setFolderStructureScan('/home/tim/Desktop/Avenue.5')

        print("\nScanning folderstructure for video files: ")
        print("==================================================================")
        filteredFileList = fc.getFolderStructureOnFilesize(100000)
        for video in filteredFileList:
            print(video)
        print("Crawler detected ", len(filteredFileList), " video files.")


    def runFFmpeg(self):
        ffmpeg = FFmpeg("ultrafast")
        isSuccess = ffmpeg.runTranscoding("test_1.mp4", "output.mkv")
        print(isSuccess)


main()
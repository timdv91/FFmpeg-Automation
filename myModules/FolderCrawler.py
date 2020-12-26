import os

class FolderCrawler():
    def __init__(self, pMinimumFileSizeKB = 1000):
        self.minimumFileSize = pMinimumFileSizeKB

    # Sets a folder path followed by scanning for all files within this folder (also in subdirectories)
    def setFolderStructureScan(self, pPath):
        # r=root, d=directories, f = files
        self.folderStructure = []
        for r, d, f in os.walk(pPath):
            for file in f:
                if file:
                    self.folderStructure.append(os.path.join(r, file))

    # Returns the complete list scanned by setFolderStructreScan.
    def getFolderStructureAll(self):
        return self.folderStructure

    # Returns a filtered list from setFolderStructureScan based on filesize tresholds.
    def getFolderStructureOnFilesize(self, pFileSizeMinKB = 0, pFileSizeMaxKB = None):
        returnList = []
        for file in self.folderStructure:
            fileSize = (os.stat(file).st_size) / 1000
            if (fileSize >= pFileSizeMinKB):
                if ((pFileSizeMaxKB == None) or (fileSize <= pFileSizeMaxKB)):
                    returnList.append(file)
        return returnList


# Example:
'''
fc = FolderCrawler()
fc.setFolderStructureScan('/home/tim/Desktop/Avenue.5')

print("\nScanning folderstructure for video files: ")
print("==================================================================")
filteredFileList = fc.getFolderStructureOnFilesize(100000)
for video in filteredFileList:
    print(video)
print("Crawler detected ", len(filteredFileList), " video files.")
'''
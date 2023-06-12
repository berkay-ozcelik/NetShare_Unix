class Device:
    def __init__(self, deviceName, OS, IP):
        self.deviceName = deviceName
        self.OS = OS
        self.IP = IP

class File:
    def __init__(self, fileName, fileSize, extension):
        self.fileName = fileName
        self.fileSize = fileSize
        self.extension = extension

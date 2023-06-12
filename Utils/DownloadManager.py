import asyncio
import json
import time
from threading import Thread
from Entity.Command import CommandRequest
from Utils.Communicator import PipeClient

class Observable:
    def register(self, observer):
        pass

    def notify_all(self,is_active,progress,message):
        pass

class Observer:
    def notify(self,is_active,progress,message):
        pass

class Download(Observable):


    def __init__(self,downloadID):
        self.downloadID = downloadID
        self.isActive = True
        self.progress = 0
        self.message = ''
        self.observers = []
        # Start a thread to pool the progress
        Thread(target=self.start_pooling).start()



    def start_pooling(self):
        while self.isActive:
            request = CommandRequest('GetDownloadProgress', str(self.downloadID))
            res = PipeClient.get_instance().send_and_receive(request)

            if res.Type == 1:
                self.isActive = False
                self.message = res.Message
                self.notify_all(self.isActive,self.progress,self.message)
                return

            serialized = res.Message
            self.progress = int(json.loads(serialized))
            if self.progress == 100:
                self.isActive = False

            self.notify_all(self.isActive,self.progress,"")

            time.sleep(.3)

    def register(self, observer):
        self.observers.append(observer)

    def notify_all(self,is_active,progress,message):
        for observer in self.observers:
            observer.notify(is_active,progress,message)

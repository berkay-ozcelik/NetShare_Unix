import os
import time

from multiprocessing import Process
from Entity.Command import CommandRequest
from MainForm import MainForm
from Utils.Communicator import PipeClient

def run_netshare_core():
    os.system('.\\Binary\\NetShare_Core.exe')

def main():
    process = Process(target=run_netshare_core)
    process.start()

    time.sleep(1)
    PipeClient.get_instance()
    request = CommandRequest('StartAcceptor', '')
    res = PipeClient.get_instance().send_and_receive(request)

    if res.Type == 1:
        return
    MainForm()
    PipeClient.get_instance().close()

if __name__ == '__main__':
    main()
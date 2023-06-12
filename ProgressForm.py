# Create progress bar with file name label , 2 buttons (Cancel and Hide) and progress bar
import json
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import MainForm
from Entity.Command import CommandRequest
from Utils.Communicator import PipeClient
from Utils.DownloadManager import Observer, Download


class ProgressForm(Observer):

    def __init__(self, file_name, file_index):
        self.root = Tk()
        self.root.title("Downloading")
        self.root.geometry("210x90")
        self.root.resizable(False, False)

        self.file_name = file_name

        if len(file_name) > 20:
            file_name = "..." + file_name[-20:]

        # Creating the label left top corner of the form
        self.lblFileName = Label(self.root, text=file_name, justify="left")
        self.lblFileName.grid(row=0, column=0, padx=7, pady=5, sticky="w")

        # Creating the label right top corner of the form
        self.lblProgress = Label(self.root, text="0%", justify="right")
        self.lblProgress.grid(row=0, column=0, padx=7, pady=5, sticky="e")

        # Creating the progress bar
        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, length=200, mode='determinate')
        self.progress.grid(row=1, column=0, padx=5, pady=0, sticky="w")

        # Creating the button to Cancel
        self.btnCancel = Button(self.root, text="Cancel", command=self.btnCancel_Click)
        self.btnCancel.grid(row=2, column=0, padx=10, pady=2, sticky="w")

        # Set the button has the half width of the form
        self.btnCancel.config(width=11)

        # Creating the button to Hide
        self.btnHide = Button(self.root, text="Hide", command=self.btnHide_Click)
        self.btnHide.grid(row=2, column=0, padx=10, pady=2, sticky="e")

        # Set the button has the half width of the form
        self.btnHide.config(width=11)

        self.download_id = 0
        self.file_index = file_index

        if self.start_download():
            Download(self.download_id).register(self)
            self.root.mainloop()
        else:
            self.root.destroy()

    def notify(self, is_active, progress, message):
        if is_active:
            self.lblProgress.config(text=str(progress) + "%")
            self.progress['value'] = progress
            return

        if progress == 100:
            # Dialog box to show the download is completed
            self.lblProgress.config(text=str(progress) + "%")
            self.progress['value'] = progress
            messagebox.showinfo(self.file_name, "Download completed")
            self.root.destroy()
            return

        # Dialog box to show the download is failed
        messagebox.showerror(self.file_name, message)
        self.root.destroy()
        return

    def start_download(self):
        # Send download request to server
        request = CommandRequest("StartDownload", str(self.file_index))
        response = PipeClient.get_instance().send_and_receive(request)

        if response.Type == 1:
            # File exists. Ask user to overwrite
            if messagebox.askyesno("File exists", "File exists. Do you want to overwrite?"):
                # Combine path and file name
                file_path = os.path.join(MainForm.get_download_folder_path(), self.file_name)
                os.remove(file_path)
                return self.start_download()
            return False

        serialized = response.Message
        self.download_id = json.loads(serialized)
        return True

    def btnCancel_Click(self):
        request = CommandRequest("StopDownload", str(self.download_id))
        PipeClient.get_instance().send_and_receive(request)




    def btnHide_Click(self):
        self.root.withdraw()

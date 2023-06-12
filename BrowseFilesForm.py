import json
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from Entity.Command import CommandRequest
from ProgressForm import ProgressForm
from Utils.Communicator import PipeClient


class BrowseFilesForm:
    # Constructor
    def __init__(self, deviceName, OS, deviceIndex):
        self.deviceIndex = deviceIndex
        self.root = Tk()
        self.root.title("Browse Files")
        self.root.geometry("225x320")
        self.root.resizable(False, False)

        # Create label top left corner of the form With text "Device Name: DEVICENAME"
        self.lblDeviceName = Label(self.root, text=f"Device Name: {deviceName}", justify="left")
        self.lblDeviceName.grid(row=0, column=0, padx=5, pady=0, sticky="w")

        # Create label top left corner of the form With text "OS: Unix 1.23.4"
        self.lblOS = Label(self.root, text=f"OS: {OS}", justify="left")
        self.lblOS.grid(row=1, column=0, padx=5, pady=0, sticky="w")

        # Creating the label left top corner of the form
        self.lblDevices = Label(self.root, text="Sharing files",justify="left")
        self.lblDevices.grid(row=2, column=0, padx=5, pady=0, sticky="w")

        # Creating the listbox with multicolmns. 1st column is for File name and 2nd column is for file size. 1st col has 60% width and 2nd col has 40% width
        self.lstFiles = ttk.Treeview(self.root, columns=("File", "Size"), show="headings")
        self.lstFiles.column("File", width=135)
        self.lstFiles.column("Size", width=80)

        self.lstFiles.heading("File", text="File")
        self.lstFiles.heading("Size", text="Size")

        self.lstFiles.grid(row=3, column=0, padx=5, pady=0, sticky="w")

        # Allow only one item to be selected at a time
        self.lstFiles.config(selectmode="browse")

        # Creating the button to Download file
        self.btnDownload = Button(self.root, text="Download", command=self.btnDownload_Click)
        self.btnDownload.grid(row=4, column=0, padx=7, pady=2, sticky="w")

        # Set the button has the half width of the form
        self.btnDownload.config(width=7)



        # Creating the button to Refresh
        self.btnRefresh = Button(self.root, text="Refresh", command=self.btnRefresh_Click)
        self.btnRefresh.grid(row=4, column=0, padx=(120,6), pady=2, sticky="w")

        # Set the button has the half width of the form
        self.btnRefresh.config(width=7)

        self.btnRefresh_Click()

        # Start the form
        self.root.mainloop()

    def btnDownload_Click(self):
        # If no file is selected, show the error message
        if len(self.lstFiles.selection()) == 0:
            messagebox.showerror("Error", "Please select a file to download.")
            return

        index = self.lstFiles.index(self.lstFiles.selection()[0])

        file_name = self.lstFiles.item(self.lstFiles.selection()[0])["values"][0]
        # Allow max file name length of 20 characters, select the last 20 characters and add "..." to the end


        ProgressForm(file_name,index)

    def btnRefresh_Click(self):
        # Clear the listbox properly
        self.lstFiles.delete(*self.lstFiles.get_children())

        request = CommandRequest("SelectDevice", str(self.deviceIndex))
        response = PipeClient.get_instance().send_and_receive(request)

        if response.Type == 1:
            messagebox.showerror("Error", response.Message)
            self.root.destroy()
            return

        request = CommandRequest("GetSharingFiles", "")
        response = PipeClient.get_instance().send_and_receive(request)

        if response.Type == 1:
            messagebox.showerror("Error", response.Message)
            return

        serialized = response.Message
        files = json.loads(serialized)

        # Add the files to the listbox
        for file in files:
            file_size = int(file["FileSize"]) / 1024 / 1024
            file_size = "{:.2f}".format(file_size)
            self.lstFiles.insert("", "end", values=(file["FileName"], file_size))



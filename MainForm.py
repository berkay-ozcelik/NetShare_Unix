import json
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from BrowseFilesForm import BrowseFilesForm
from Entity.Command import CommandRequest
from Entity.Logic import Device
from ManageFilesForm import ManageFilesForm
from Utils.Communicator import PipeClient

# Get cwd
import os

downloadFolderPath = path = os.path.join(os.getcwd(), "Downloads")


def get_download_folder_path():
    return downloadFolderPath
def set_download_folder_path(path):
    global downloadFolderPath
    downloadFolderPath = path

class MainForm:
    # Constructor
    def __init__(self):
        self.devices = None
        self.root = Tk()
        self.root.title("NetShare")
        self.root.geometry("210x390")
        self.root.resizable(False, False)

        # Creating the label left top corner of the form
        self.lblDevices = Label(self.root, text="Active devices", justify="left")
        self.lblDevices.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Creating the listbox with multicolmns. 1st column is for device name and 2nd column is for device Endponint. 1st col has 40% width and 2nd col has 60% width
        self.lstDevices = ttk.Treeview(self.root, columns=("Device", "Endpoint"), show="headings")
        self.lstDevices.column("Device", width=80)
        self.lstDevices.column("Endpoint", width=120)
        self.lstDevices.heading("Device", text="Device")
        self.lstDevices.heading("Endpoint", text="Endpoint")
        self.lstDevices.grid(row=1, column=0, padx=5, pady=0)

        # Allow only one item to be selected at a time
        self.lstDevices.config(selectmode="browse")

        # Creating the button to select the device
        self.btnSelect = Button(self.root, text="Select", command=self.btnSelect_Click)
        self.btnSelect.grid(row=2, column=0, padx=6, pady=2, sticky="w")
        # Set the button has the half width of the form
        self.btnSelect.config(width=12)

        # Creating the button to refresh the list of devices
        self.btnRefresh = Button(self.root, text="Refresh", command=self.search_devices)
        self.btnRefresh.grid(row=2, column=0, padx=6, pady=2, sticky="e")
        # Set the button has the half width of the form
        self.btnRefresh.config(width=12)

        # Add Manage Sharing Files button to the 3rd row
        self.btnManageSharingFiles = Button(self.root, text="Manage Sharing Files",
                                            command=self.btnManageSharingFiles_Click)
        self.btnManageSharingFiles.grid(row=3, column=0, padx=5, pady=2)
        # Set the button has the full width of the form
        self.btnManageSharingFiles.config(width=27)

        # Add Set Download Folder button to the 4th row
        self.btnSetDownloadFolder = Button(self.root, text="Set Download Folder",
                                           command=self.btnSetDownloadFolder_Click)
        self.btnSetDownloadFolder.grid(row=4, column=0, padx=5, pady=2)
        # Set the button has the full width of the form
        self.btnSetDownloadFolder.config(width=27)



        self.btnAbout = Button(self.root, text="About", command=self.btnAbout_Click)
        self.btnAbout.grid(row=5, column=0, padx=5, pady=2)
        # Set the button has the full width of the form
        self.btnAbout.config(width=27)

        self.root.mainloop()

    def btnAbout_Click(self):
        messagebox.showinfo("About",
                            "NetShare Client Unix v1.0.0\n\nDeveloped by Berkay Ozcelik\n\nGraduation Project II\n\nCelal Bayar University")

    # Method to set download folder
    def btnSetDownloadFolder_Click(self):
        folder = filedialog.askdirectory()

        if folder == "":
            return

        # Send a request to the server to set the download folder
        request = CommandRequest("SetDownloadDirectory", folder)

        response = PipeClient.get_instance().send_and_receive(request)

        if response.Type == 1:
            messagebox.showerror("Error", response.Message)
            return

        set_download_folder_path(folder)

        messagebox.showinfo("Success", "Download folder is set successfully")

    def btnRefresh_Click(self):
        self.search_devices()

    def search_devices(self):

        # Clear the listbox
        self.lstDevices.delete(*self.lstDevices.get_children())

        # Send a request to the server to get the list of devices

        request = CommandRequest("DiscoverDevices", "")

        response = PipeClient.get_instance().send_and_receive(request)



        if response.Type == 1:
            # Show error dialog
            messagebox.showerror("Error", response.Data)
            return

        serialized = response.Message

        devices = json.loads(serialized)

        self.devices = devices

        # Add devices to the listbox
        for device in devices:
            self.lstDevices.insert("", "end", values=(device["DeviceName"], device["EndPoint"]))

    def btnSelect_Click(self):
        # If no device is selected show a message box
        if len(self.lstDevices.selection()) == 0:
            messagebox.showerror("Error", "Please select a device")
            return

        index = self.lstDevices.index(self.lstDevices.selection()[0])

        device = self.devices[index]

        BrowseFilesForm(device["DeviceName"], device["DeviceOS"], index)

    def btnManageSharingFiles_Click(self):
        ManageFilesForm()

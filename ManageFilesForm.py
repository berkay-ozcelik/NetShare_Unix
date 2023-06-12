# This form has one label indicates that "Sharing files" left up corner of the form.
# Bottom of the label one list box with 2 columns. First column is the file name and second column is the file size.
# 2 buttons side by side one is for "Share File" and another is for "Stop Share".
import json
# Creating the form layout
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from Entity.Command import CommandRequest
from Utils.Communicator import PipeClient


class ManageFilesForm:
    # Constructor
    def __init__(self):
        self.root = Tk()
        self.root.title("Manage Files")
        self.root.geometry("210x290")
        self.root.resizable(False, False)

        # Creating the label left top corner of the form
        self.lblDevices = Label(self.root, text="Sharing files",justify="left")
        self.lblDevices.grid(row=0, column=0, padx=5, pady=5, sticky="w")


        # Creating the listbox with multicolmns. 1st column is for File name and 2nd column is for file size. 1st col has 60% width and 2nd col has 40% width
        self.lstFiles = ttk.Treeview(self.root, columns=("File", "Size"), show="headings")
        self.lstFiles.column("File", width=120)
        self.lstFiles.column("Size", width=80)

        self.lstFiles.heading("File", text="File")
        self.lstFiles.heading("Size", text="Size")
        self.lstFiles.grid(row=1, column=0, padx=5, pady=0)

        # Add OnSelectedIndexChanged event to the listbox
        self.lstFiles.bind("<<TreeviewSelect>>", self.lstFiles_OnSelectedIndexChanged)
        # Allow only one item to be selected at a time
        self.lstFiles.config(selectmode="browse")

        # Add dummy data to the listbox 100 times
        for i in range(100):

            self.lstFiles.insert("", "end", values=("File " + str(i), "Size " + str(i)))

        # Creating the button to add file
        self.btnAdd = Button(self.root, text="Add", command=self.btnAdd_Click)
        self.btnAdd.grid(row=2, column=0, padx=6, pady=2, sticky="w")
        # Set the button has the half width of the form
        self.btnAdd.config(width=12)

        # Creating the button to remove file
        self.btnRemove = Button(self.root, text="Remove", command=self.btnRemove_Click)
        self.btnRemove.grid(row=2, column=0, padx=6, pady=2, sticky="e")
        # Set the button has the half width of the form
        self.btnRemove.config(width=12)

        self.update_lstFiles()

        # Start the form
        self.root.mainloop()

    def update_lstFiles(self):

        self.lstFiles.delete(*self.lstFiles.get_children())

        # Send the request to the server to get the list of files

        request = CommandRequest("GetSharingFilesOfCurrentDevice", "")
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

    def btnAdd_Click(self):
        # Open the file dialog to select the file
        file_path = filedialog.askopenfilename()
        if file_path == "":
            return

        # Send the request to the server to add the file
        request = CommandRequest("ShareFile", file_path)
        response = PipeClient.get_instance().send_and_receive(request)

        if response.Type == 1:
            messagebox.showerror("Error", response.Message)
            return

        self.update_lstFiles()

    def btnRemove_Click(self):
        # If no file is selected, show the error message
        if len(self.lstFiles.selection()) == 0:
            messagebox.showerror("Error", "Please select a file to remove.")
            return

        index = self.lstFiles.index(self.lstFiles.selection()[0])
        # Send the request to the server to remove the file
        request = CommandRequest("StopShareFile", str(index))
        response = PipeClient.get_instance().send_and_receive(request)

        if response.Type == 1:
            messagebox.showerror("Error", response.Message)
            return

        self.update_lstFiles()



    def lstFiles_OnSelectedIndexChanged(self, e):
        pass








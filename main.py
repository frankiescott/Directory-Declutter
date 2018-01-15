import tkinter as tk
import tkinter.ttk as ttk
import os
import shutil
import configparser
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Directory Declutter")

        self.config = configparser.ConfigParser()
        self.config.read('C:\\Users\\Frankie\\Documents\\Coding Projects\\Downloads\\folders.ini')

        self.downloads_dir = tk.StringVar(self, value=self.config['folders']['downloads'])
        self.pictures_dir = tk.StringVar(self, value=self.config['folders']['pictures'])
        self.documents_dir = tk.StringVar(self, value=self.config['folders']['documents'])
        self.audio_dir = tk.StringVar(self, value=self.config['folders']['audio'])
        self.pictures_ext = self.config['extensions']['pictures'].split(";")
        self.documents_ext = self.config['extensions']['documents'].split(";")
        self.audio_ext = self.config['extensions']['audio'].split(";")

        self.entries = []
        self.entries.append(tk.Entry(self, textvariable=self.downloads_dir))
        self.entries[0].grid(row=1, column=1, padx=5, pady=1, sticky="we")
        self.entries.append(tk.Entry(self, textvariable=self.pictures_dir))
        self.entries[1].grid(row=3, column=1, padx=5, pady=1, sticky="we")
        self.entries.append(tk.Entry(self, textvariable=self.documents_dir))
        self.entries[2].grid(row=4, column=1, padx=5, pady=1, sticky="we")
        self.entries.append(tk.Entry(self, textvariable=self.audio_dir))
        self.entries[3].grid(row=5, column=1, padx=5, pady=1, sticky="we")
        self.columnconfigure(1, minsize=350)

        self.buttons = []
        self.buttons.append(tk.Button(self, text="...", command=lambda:self.getPath(0)))
        self.buttons[0].grid(row=1, column=2, padx=5, pady=1, sticky="e")
        self.buttons.append(tk.Button(self, text="...", command=lambda:self.getPath(1)))
        self.buttons[1].grid(row=3, column=2, padx=5, pady=1, sticky="e")
        self.buttons.append(tk.Button(self, text="...", command=lambda:self.getPath(2)))
        self.buttons[2].grid(row=4, column=2, padx=5, pady=1, sticky="e")
        self.buttons.append(tk.Button(self, text="...", command=lambda:self.getPath(3)))
        self.buttons[3].grid(row=5, column=2, padx=5, pady=1, sticky="e")

        self.labels = []
        self.labels.append(tk.Label(self, text="Origin Folder:"))
        self.labels[0].grid(row=0, column=0, padx=5, pady=1, sticky="w")
        self.labels.append(tk.Label(self, text="Downloads"))
        self.labels[1].grid(row=1, column=0, padx=5, pady=1, sticky="e")
        self.labels.append(tk.Label(self, text="Target Folders:"))
        self.labels[2].grid(row=2, column=0, padx=5, pady=1, sticky="w")
        self.labels.append(tk.Label(self, text="Pictures"))
        self.labels[3].grid(row=3, column=0, padx=5, pady=1, sticky="e")
        self.labels.append(tk.Label(self, text="Documents"))
        self.labels[4].grid(row=4, column=0, padx=5, pady=1, sticky="e")
        self.labels.append(tk.Label(self, text="Audio"))
        self.labels[5].grid(row=5, column=0, padx=5, pady=1, sticky="e")

        okcancelframe = tk.Frame(self)

        self.okbtn = tk.Button(okcancelframe, text="Organize", width=10, command=self.organize)
        self.okbtn.grid(row=0, column=0, pady=15, padx=15)
        self.cancelbtn = tk.Button(okcancelframe, text="Close", width=10, command=self.saveandclose)
        self.cancelbtn.grid(row=0, column=1, pady=15, padx=15)
        okcancelframe.grid(row=6, column=0, columnspan=3)

        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=7, column=0, columnspan=3, padx=10, pady=5, sticky="we")

        #self.bar = ttk.Progressbar(self, orient=HORIZONTAL, mode='determinate')
        #self.bar.grid(row=8, column=0, columnspan=3, sticky="we")

    def saveandclose(self):
        file = open('C:\\Users\\Frankie\\Documents\\Coding Projects\\Downloads\\folders.ini', 'w')
        self.config.set('folders', 'downloads', self.entries[0].get())
        self.config.set('folders', 'pictures', self.entries[1].get())
        self.config.set('folders', 'documents', self.entries[2].get())
        self.config.set('folders', 'audio', self.entries[3].get())
        self.config.write(file)
        file.close()
        quit()

    def movefiles(self, filelist):
        self.bar = ttk.Progressbar(self, orient=HORIZONTAL, mode='determinate')
        self.bar.grid(row=8, column=0, columnspan=3, sticky="we")
        self.bar['maximum'] = int(len(filelist))
        index = 0
        for f in filelist:
            self.bar.step()
            self.update()
            shutil.move(f[0], f[1])
            self.listbox.insert(index, "[" + str(index + 1) + "] " + f[2] + " -> " + f[3])
            self.listbox.yview(END) #autoscroll the listbox
            index += 1
        self.bar.destroy()

    def organize(self):
        downloads_dir = self.entries[0].get()
        pictures_dir = self.entries[1].get()
        documents_dir = self.entries[2].get()
        audio_dir = self.entries[3].get()

        filelist = []
        count = 0
        for filename in os.listdir(downloads_dir):
            extension = os.path.splitext(filename)[1][1:]

            #ignore folders
            if os.path.isdir(downloads_dir + "/" + filename):
                continue

            if extension in self.pictures_ext:
                filelist.append([downloads_dir + "/" + filename, pictures_dir + "/" + filename, filename, pictures_dir])
                count += 1
            if extension in self.documents_ext:
                filelist.append([downloads_dir + "/" + filename, documents_dir + "/" + filename, filename, documents_dir])
                count += 1
            if extension in self.audio_ext:
                filelist.append([downloads_dir + "/" + filename, audio_dir + "/" + filename, filename, audio_dir])
                count += 1


        if count == 0:
            messagebox.showinfo("File Organizer", "No eligible files found.")
        else:
            result = messagebox.askquestion("File Organizer", str(count) + " files found in " + downloads_dir + ". Continue?", icon="warning")
            if result == "yes":
                self.movefiles(filelist)
            else:
                filelist = []

    def run(self):
        self.mainloop()

    def getPath(self, indx):
        directory = filedialog.askdirectory(initialdir="C:\\")
        self.entries[indx].insert(0, directory)

if __name__ == '__main__':
    MainApp().run()

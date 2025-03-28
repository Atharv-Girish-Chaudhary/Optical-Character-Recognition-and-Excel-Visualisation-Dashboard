import customtkinter as ctk
from PIL import Image
import os
from modules import file_pdf_conv
from modules import image_table_conv
import tkinter as tk
from modules import dashboard
from data import gui
class MainSoftware(ctk.CTk):
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    def DashboardButton(self):
        dashboard.main()

    def HomeButton(self):
        self.var = self.ProgressSwitchVar.get()
        if self.var == 'on':
            if self.Progress_state == 1:
                tk.messagebox.showerror('Software error', 'Error: wait for the current process to be completed')
            else:
                self.switch.deselect()
                self.progressbar.destroy()
                self.Progresslabel.destroy()
                self.MainbuttonAdd()
        else:
            try:
                self.FolderButton.destroy()
                self.MainbuttonAdd()
            except:
                try:
                    self.Mainbutton.destroy()
                    self.MainbuttonAdd()
                except:
                    self.MainbuttonAdd()

    def FilesButton2(self):

        self.files = os.listdir(r"data\raw")
        dir_list = '\n'.join(map(str, self.files))
        self.font = self.font = ctk.CTkFont(size=20)

        self.file_title.configure(text="Uploded Files", anchor='n', font=self.font)
        self.label.configure(text=dir_list, anchor='center', font=self.font)

    def SelectFilebutton(self):

        self.FolderButton.destroy()
        self.MainbuttonsAdd()

    def MainbuttonAdd(self):
        self.FolderButton = ctk.CTkButton(self.FolderFrame, image=self.FolderImage, text='', width=600, height=440,
                                          command=self.SelectFilebutton, fg_color='transparent')
        self.FolderButton.grid(padx=10, pady=10)

    def MainbuttonsAdd(self):
        self.Mainbutton = ctk.CTkButton(self.MainFrame, text='From Device', width=50, command=self.FromDevice)
        self.Mainbutton.place(relx=0.5, rely=0.5, anchor='center')

    def MainbuttonsRemove(self):
        self.Mainbutton.destroy()

    def AddProgressBar(self):
        self.progressbar = ctk.CTkProgressBar(master=self.FolderFrame, width=600)
        self.progressbar.grid(pady=20, padx=20)
        self.progressbar.set(0, 5)
        self.progressbar.start()

    def RemoveProgress(self):
        self.var = self.ProgressSwitchVar.get()
        if self.var == 'on':
            if self.Progress_state == 1:
                tk.messagebox.showerror('Software error', 'Error: wait for the current process to be completed')
            else:
                self.switch.deselect()
                self.progressbar.destroy()
                self.Progresslabel.destroy()

    def ChangeAppearanceModeEvent(self):
        if self.mode == 'light':
            ctk.set_appearance_mode("dark")
            self.mode = 'dark'
        elif self.mode == 'dark':
            ctk.set_appearance_mode("light")
            self.mode = 'light'

    def FromDevice(self):
        file_pdf_conv.upload_file()
        # self.Button2()
    def Progress_Label(self):
        self.Progresslabel = ctk.CTkLabel(self.FolderFrame, text="Your progress  ::", anchor='n')
        self.Progresslabel.grid(padx=5, pady=20)

    def Progress(self):
        self.var = self.ProgressSwitchVar.get()
        print("switch toggled, current value:", self.var)
        if self.var == 'on':
            try:
                self.MainbuttonsRemove()
                self.Progress_Label()
                self.AddProgressBar()
                tk.messagebox.showinfo("Success!", f"File Processing has started")
                image_table_conv.iterate_files(root_input_dir= 'Files', root_output_dir='Files')
                tk.messagebox.showinfo("Success!", f"File has been converted to Excel file")
                self.RemoveProgress()
                self.switch.deselect()
                self.FolderFrame.destroy()
                self.FolderFrame = ctk.CTkFrame(self.MainFrame, width=600, height=440, corner_radius=10,border_color='blue')
                self.FolderFrame.grid(padx=(50, 0), pady=100)
                os.startfile(r'Files\CreatedCsvFile.csv')


            except:
                self.switch.deselect()
                tk.messagebox.showerror('File not found', 'Error: Please upload the file')
        elif self.var == 'off':
            self.switch.select()
            tk.messagebox.showerror('Incompleted', 'Error: process not completed')

    def Root_Frame(self):
        self.RootFrame = ctk.CTkFrame(self, corner_radius=10, border_color='blue')
        self.title("Excel Dashboard Automation")
        self.geometry(f"{1040}x{720}")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def Frames(self):
        self.title_text = ""
        self.font = ctk.CTkFont(size=50)
        self.MainFrame = ctk.CTkFrame(self.RootFrame, width=700, height=640, corner_radius=10, border_color='blue')
        self.SideFrame = ctk.CTkFrame(self.RootFrame, width=320, height=640, corner_radius=10, border_color='blue')
        self.SideFrame1 = ctk.CTkFrame(self.SideFrame, width=50, height=600, corner_radius=10, border_color='blue',
                                       fg_color='transparent')
        self.SideFrame2 = ctk.CTkFrame(self.SideFrame, width=250, height=600, corner_radius=10, border_color='blue')
        self.FolderFrame = ctk.CTkFrame(self.MainFrame, width=600, height=440, corner_radius=10, border_color='blue')
        self.TitleFrame = ctk.CTkFrame(self, width=1040, height=50)
        self.TitleFrame.grid_propagate(False)
        self.SideFrame.grid_propagate(False)
        self.MainFrame.grid_propagate(False)

    def Images(self):
        self.SideImage1 = ctk.CTkImage(light_image=Image.open('data\gui/Home.png'), size=(30, 30))
        self.SideImage2 = ctk.CTkImage(light_image=Image.open('data\gui/Files.png'), size=(30, 30))
        self.SideImage3 = ctk.CTkImage(light_image=Image.open('data\gui/Graph.png'), size=(30, 30))
        self.FolderImage = ctk.CTkImage(light_image=Image.open('data\gui/MainFolder.png'), size=(600, 430))
        self.SwitchImage = ctk.CTkImage(light_image=Image.open('data\gui/Home.png'), size=(30, 30))
        self.ModeImage = ctk.CTkImage(light_image=Image.open('data\gui/Dark Mode.png'), size=(30, 30))
        self.TitleImage = ctk.CTkImage(light_image=Image.open('data\gui/TitleImage.png'), size=(1040, 70))

    def Buttons(self):
        self.button1 = ctk.CTkButton(self.SideFrame1, image=self.SideImage1, text='', width=30, command=self.HomeButton)
        self.button2 = ctk.CTkButton(self.SideFrame1, image=self.SideImage2, text='', width=30,
                                     command=self.FilesButton2)
        self.button3 = ctk.CTkButton(self.SideFrame1, image=self.SideImage3, text='', width=30,
                                     command=self.DashboardButton)
        self.AppearanceModeButton = ctk.CTkButton(self.SideFrame1, image=self.ModeImage, text='', width=30, height=30,
                                                  command=self.ChangeAppearanceModeEvent, fg_color='transparent')

    def AddFrames(self):
        self.TitleFrame.grid(row=0, column=0, sticky='nsew')
        self.RootFrame.grid(row=1, column=0)
        self.SideFrame.grid(row=0, column=0, padx=2)
        self.MainFrame.grid(row=0, column=1, padx=2)
        self.SideFrame1.grid(row=0, column=0, padx=20)
        self.SideFrame2.grid(row=0, column=1, padx=2, pady=20)
        self.FolderFrame.grid(padx=(50, 0), pady=100)

    def Addbuttons(self):
        self.button1.grid(row=1, column=0, pady=5)
        self.button2.grid(row=2, column=0, pady=5)
        self.button3.grid(pady=5)
        self.AppearanceModeButton.grid(pady=5)

 

    def Variables(self):
        self.Progress_state = 0
        self.toplevel_window = None

    def labels(self):
        self.file_title = ctk.CTkLabel(self.SideFrame2, text="", width=200, anchor='n')
        self.label = ctk.CTkLabel(self.SideFrame2, text="", height=450, width=200, anchor='n')
        self.title_label = ctk.CTkLabel(self.TitleFrame, text=self.title_text, width=1040, font=self.font, height=80,
                                        image=self.TitleImage)

    def Widgets(self):

        self.switch = ctk.CTkSwitch(self.SideFrame2, text="", command=self.Progress, variable=self.ProgressSwitchVar,
                                    onvalue="on", switch_height=20, switch_width=50, offvalue="off")
        self.file_title.grid(padx=5, pady=20)
        self.label.grid(padx=5, pady=20)

        self.title_label.grid(row=0, column=0)
        self.switch.grid(padx=5, pady=10)

    def __init__(self):
        super().__init__()
        self.Root_Frame()
        self.window = None
        self.ProgressSwitchVar = ctk.StringVar(value="off")
        self.mode = 'dark'
        self.Variables()
        self.Frames()
        self.Images()
        self.labels()
        self.Buttons()
        self.AddFrames()
        self.Addbuttons()
        self.Widgets()
        self.MainbuttonAdd()


if __name__ == "__main__":
    MainSoftware = MainSoftware()
    MainSoftware.mainloop()

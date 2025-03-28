import modules.file_pdf_conv as file_pdf_conv
import tkinter as tk
from tkinter import filedialog
import webbrowser


google_drive_url = "https://drive.google.com/drive/my-drive"


def getfilepath_drive() -> None:
    """This Function opens web Google Drive and prompts the user to download required file to system download folder
    and then prompts the user to select the file from downloads folder """

    webbrowser.open_new_tab(google_drive_url)  # Opens Google Drive in a new browser tab
    option_text = "option clicked : --From Google Drive"
    print(option_text)
    # Prompt the user to select the file they just downloaded
    downloaded_file_path = tk.filedialog.askopenfilename(title="Select the downloaded Google Drive file",
                                                         # filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
                                                         )

    if downloaded_file_path:
        file_pdf_conv.conversion(downloaded_file_path)  # Converts accepted file type into PDF


if __name__ == "__main__":
    getfilepath_drive()

"""Pending : Increase the font size"""

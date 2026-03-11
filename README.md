# Workflow Overview

* GUI to accept files from the user.
* Supports multiple file types.
* Converts all files to PDFs.
* Stores them in a designated directory.

For each stored PDF:

* **Pillow** - Opens and processes images.
* **OpenCV** - Applies image transformations.
* **PyTesseract** - Extracts text from images.
* Stores extracted text in CSV format.
* Combines CSV files into Excel (Work in Progress).

## Required Libraries

Install the following libraries using `pip` or appropriate package managers:

1. **Pillow** - `pip install pillow`
2. **OpenCV** - `pip install opencv-python`
3. **Tesseract** - `brew install tesseract` (For macOS)
4. **PyTesseract** - `pip install pytesseract`
5. **Tkinter** - `pip install tk`
6. **doc2pdf** - `pip install doc2pdf`
7. **customtkinter** - `pip install customtkinter`
8. **pdf2image** - `brew install pdf2image` (For macOS)

## Image Preprocessing Techniques

The following preprocessing techniques are applied to optimize OCR accuracy:

1. Inversion
2. Rescaling
3. Binarization
4. Noise Removal
5. Dilation and Erosion
6. Rotation / De-skewing
7. Border Removal

## Functions Overview

### **Google_drive.py Functions**

1. `webbrowser.open_new_tab()` - Opens a URL in a new browser tab.
2. `tk.filedialog.askopenfilename()` - Opens a file dialog for users to select files.

### **Directories.py Functions**

1. `os.path.exists()` - Checks if a file or directory exists.
2. `os.path.join()` - Joins file paths using the appropriate separator.
3. `os.getcwd()` - Returns the current working directory.
4. `os.mkdir()` - Creates a new directory.

### **FilePdf_conv.py Functions**

1. `os.path.basename()` - Extracts the file name from a path.
2. `os.rename()` - Renames files or directories.
3. `doc2pdf.convert()` - Converts Word documents to PDF using the `doc2pdf` library.
4. `os.path.splitext()` - Splits a file name into name and extension.
5. `tkinter.messagebox.showinfo()` - Displays an informational pop-up.

### **ImageText_conv.py Functions**

1. `pdf2image.convert_from_path()` - Converts PDF pages to images.
2. `enumerate()` - Iterates over items while keeping track of their index.

## Drawbacks

* The system currently does not support handwritten document recognition.
* Limited support for low-quality scans and images with significant noise.

## Future Improvements

* Improve handwriting recognition using additional OCR models.
* Enhance preprocessing for low-quality images.
* Implement better file management for large datasets.

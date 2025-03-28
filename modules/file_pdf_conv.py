import os
import sys
import shutil
from PIL import Image

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from xls2xlsx import XLS2XLSX
    import tkinter as tk
    from tkinter import filedialog, messagebox
    from modules import directories
    import doc2pdf
except ImportError as e:
    print(f"Import Error: {e}. Please ensure all dependencies are installed.")
    sys.exit(1)

# Ensure the destination folder exists
os.makedirs(os.path.join(os.getcwd(), 'data', 'raw'), exist_ok=True)

def MovePdf(file_path: str) -> None:
    destination = os.path.join(os.getcwd(), 'data', 'raw', os.path.basename(file_path))
    try:
        shutil.move(file_path, destination)
        print(f"File moved to {destination}")
    except Exception as e:
        print(f"Error moving file: {e}")

def DocConvertPdf(file_path: str) -> None:
    destination = os.path.join(os.getcwd(), 'data', 'raw', os.path.basename(file_path))
    try:
        doc2pdf.convert(file_path, destination)
        print(f"File converted to PDF and saved to {destination}")
    except Exception as e:
        print(f"Conversion failed: {e}")

def MoveExcel(file_path):
    destination = os.path.join(os.getcwd(), 'data', 'raw', os.path.basename(file_path))
    if file_path.endswith('.xlsx'):
        shutil.move(file_path, destination)
        print(f"File moved to {destination}")
    elif file_path.endswith('.xls'):
        try:
            x2x = XLS2XLSX(file_path)
            output_file_path = os.path.splitext(destination)[0] + ".xlsx"
            x2x.to_xlsx(output_file_path)
            print(f"File converted to XLSX: {output_file_path}")
        except OSError as e:
            print(f"Error converting to XLSX: {e}")

def ImgConvertPdf(file_path: str) -> None:
    try:
        image = Image.open(file_path).convert("RGB")
        pdf_path = os.path.splitext(file_path)[0] + '.pdf'
        image.save(pdf_path, "PDF")
        print(f"Image converted to PDF: {pdf_path}")
        MovePdf(pdf_path)
    except Exception as e:
        print(f"Error converting image to PDF: {e}")

def conversion(file_path: str) -> None:
    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]

    # Supported conversions
    conversion_functions = {
        '.docx': DocConvertPdf,
        '.doc': DocConvertPdf,
        '.xlsx': MoveExcel,
        '.xls': MoveExcel,
        '.jpeg': ImgConvertPdf,
        '.jpg': ImgConvertPdf,
        '.png': ImgConvertPdf,
        '.tif': ImgConvertPdf,
        '.tiff': ImgConvertPdf,
        '.pdf': MovePdf
    }

    if file_type in conversion_functions:
        conversion_functions[file_type](file_path)
        messagebox.showinfo("Success!", f"File {file_name} has been processed.")
    else:
        messagebox.showerror("Error", f"Unsupported file type: {file_type}")

def upload_file() -> None:
    try:
        print("Option clicked: --From device")
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            directories.create_root_folder_dir([r'data\raw'])
            conversion(file_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    upload_file()

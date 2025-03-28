import pdf2image
import os


def create_folder_directory() -> None:
    try:
        # create two directories named "Stored PDFs" and "Converted PDFs" in the current working directory,
        # if they don't already exist.
        for folder_dir in ['Stored PDFs', 'Converted PDFs']:
            if not os.path.exists(os.path.join(os.getcwd(), folder_dir)):
                os.mkdir(folder_dir)
    except OSError as e:
        raise Exception(f"Failed to create Folder director : {e}")


def create_sub_folder_dir(pdf_name: str) -> str:
    try:
        sub_folder_dir = os.path.join(os.getcwd(), 'Converted PDFs', pdf_name)
        if not os.path.exists(sub_folder_dir):
            os.mkdir(sub_folder_dir)
        return sub_folder_dir
    except OSError as e:
        raise Exception(f"Failed to create sub-folder directory for {pdf_name} : {e}")


def iterate_files() -> None:
    try:
        for entry in os.scandir(os.path.join(os.getcwd(), 'Stored PDFs')):
            if entry.is_file() and entry.name.endswith('.pdf'):
                pdf_name = os.path.splitext(os.path.basename(entry.path))[0]
                sub_folder_dir = create_sub_folder_dir(pdf_name)
                convert_pdf_images(pdf_name, entry.path, sub_folder_dir)
    except OSError as e:
        raise Exception(f"Failed to iterate through files : {e}")


def convert_pdf_images(pdf_name: str, pdf_path: str, sub_folder_dir: str) -> None:
    try:
        pages = pdf2image.convert_from_path(pdf_path, 400)
        for page_no, page in enumerate(pages):
            page.save(os.path.join(sub_folder_dir, f"{pdf_name}_{page_no}.jpg"), "JPEG")
    except Exception as e:
        raise RuntimeError(f"Failed to create images : {e}")


def convert_pdf() -> None:
    try:
        create_folder_directory()
        iterate_files()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PDF : {e}")


# used to check whether the script is being run as the main program or being imported as a module
if __name__ == '__main__':
    try:
        convert_pdf()
    except Exception as e:
        raise RuntimeError(f"Error in main : {e}")
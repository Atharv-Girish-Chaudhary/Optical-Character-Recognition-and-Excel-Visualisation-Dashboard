# OCR + Excel Dashboard

A desktop GUI for extracting text and tables from PDFs and images using Tesseract OCR, with a built-in dashboard for visualizing tabular data.

![Dashboard screenshot](data/gui/Desktop.png)

## What it does

- Upload a PDF or image (jpg, jpeg, png, tif, tiff) through the GUI
- The pipeline converts images to PDF, renders pages at 400 DPI, and runs OCR on each page
- Two outputs are produced:
  - **Per-page OCR text** at `data/processed/<doc>/<doc>_page_<N>.txt` — full-page Tesseract output
  - **Extracted table cells** at `data/output/Extracted_Table.csv` — one cell per row, sorted by position, derived from morphological line detection
- A separate dashboard view reads CSV output and plots numeric columns as bar charts, with a column selector

The pipeline uses OpenCV's morphological operations to detect horizontal and vertical lines in tables, find cell contours, and hand each cropped cell to Tesseract for OCR in parallel.

## Requirements

**System dependencies** (install before pip):

- **macOS**: `brew install tesseract poppler`
- **Linux**: `sudo apt install tesseract-ocr poppler-utils`
- **Windows**: install [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and [Poppler](https://github.com/oschwartz10612/poppler-windows), and ensure both binaries are on PATH.

**Python**: tested with 3.13 on macOS Apple Silicon. Other 3.11+ versions likely work but are unverified.

## Install


```bash
git clone https://github.com/Atharv-Girish-Chaudhary/Optical-Character-Recognition-and-Excel-Visualisation-Dashboard.git
cd Optical-Character-Recognition-and-Excel-Visualisation-Dashboard
pip install -r requirements.txt
```



## Run


```bash
python main.py
```



In the GUI:

1. Click **From Device** in the main pane and select a PDF or image. Sample images are bundled at `data/samples/Test_1.png` through `Test_4.png`.
2. Toggle the **progress switch** in the right sidebar to run the OCR pipeline. Status messages appear in the terminal.
3. When the pipeline finishes, the extracted CSV opens automatically.
4. Click the **chart icon** in the left sidebar to launch the dashboard. If the pipeline hasn't been run yet, the dashboard falls back to bundled sample employee data.

## Project structure


```
.
├── main.py                          # Tkinter GUI entry point
├── requirements.txt                 # Python dependencies
├── modules/
│   ├── file_pdf_conv.py             # File upload + format conversion
│   ├── image_table_conv.py          # PDF → PNG rendering, OCR orchestration
│   ├── table_text_conv2.py          # Cell-level OCR via line detection
│   ├── dashboard.py                 # CSV visualization dashboard
│   ├── directories.py               # Runtime folder creation
│   └── roi.py                       # Region-of-interest utility
└── data/
    ├── gui/                         # GUI icons + screenshot
    └── samples/                     # Bundled test images + sample CSV
```


The `data/raw/`, `data/processed/`, and `data/output/` directories are created at runtime and are gitignored.

## Image preprocessing pipeline

OCR cells go through a sequence of OpenCV operations before Tesseract:

1. Grayscale conversion
2. Bitwise inversion
3. Otsu binarization
4. Morphological opening with horizontal and vertical kernels (line detection)
5. Contour extraction on the line mask
6. Per-cell cropping and parallel OCR via `ThreadPoolExecutor`

## Known limitations

- **OCR quality** depends on input image clarity. Small text, low-contrast scans, and stylized fonts produce noisy results.
- **Table structure is partially preserved**. Output is a single-column CSV sorted by cell y-coordinate; full row × column reconstruction is not implemented.
- **No handwriting support**. Tesseract's default English model is used.
- **English only**. Multi-language support is not implemented.
- **CSV output, not Excel**. Despite the project name, results are written as CSV. Direct `.xlsx` export is a planned future improvement.

## Future improvements

- Grid-aware table reconstruction (preserve row × column layout)
- Direct `.xlsx` export with formatting
- Multi-language OCR
- Custom-trained models for handwriting

## License

See [LICENSE](LICENSE).

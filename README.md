# Ultimate PDF

A powerful, dependency-light Python CLI for everyday PDF tasks — merge, split, compress, rotate, encrypt/decrypt, watermark, OCR, convert to/from images, export to Markdown, and inspect PDF files from your terminal.

Built on [pypdf](https://pypi.org/project/pypdf/) and [PyMuPDF](https://pypi.org/project/PyMuPDF/), with a [Typer](https://typer.tiangolo.com/) interface.

## Installation

```bash
pip install ultimate-pdf
```

Requires Python 3.10+.

The `ocr` command additionally needs the [Tesseract](https://github.com/tesseract-ocr/tesseract) engine:

```bash
brew install tesseract       # macOS
apt install tesseract-ocr    # Debian/Ubuntu
```

If OCR reports that tessdata cannot be found, set `TESSDATA_PREFIX` to your Tesseract data directory.

## Usage

After installing, the `ultimate-pdf` command is available:

```bash
ultimate-pdf --help
ultimate-pdf version
```

### Merge

Combine multiple PDFs into one:

```bash
ultimate-pdf merge a.pdf b.pdf c.pdf --output merged.pdf
```

### Split

Split a PDF by page ranges, every N pages, or selected pages:

```bash
# One file per page range (writes into a directory)
ultimate-pdf split input.pdf --pages 1-3 --output out_dir/

# Every 2 pages into a separate file
ultimate-pdf split input.pdf --every 2 --output out_dir/

# Only selected pages
ultimate-pdf split input.pdf --select 1,3,5 --output out_dir/
```

### Compress

Reduce file size:

```bash
ultimate-pdf compress input.pdf --output smaller.pdf
# Omit --output to write '<input>_compressed.pdf'
```

### Rotate

Rotate pages by 90, 180, or 270 degrees:

```bash
ultimate-pdf rotate input.pdf --angle 90 --output rotated.pdf
# Rotate only specific pages
ultimate-pdf rotate input.pdf --angle 180 --pages 1,2 --output rotated.pdf
```

### Encrypt / Decrypt

```bash
ultimate-pdf encrypt input.pdf --password secret --output locked.pdf
ultimate-pdf decrypt locked.pdf --password secret --output unlocked.pdf
```

### Watermark

Stamp a text or image watermark (exactly one of `--text` / `--image`):

```bash
ultimate-pdf watermark input.pdf --text CONFIDENTIAL --opacity 0.15 --output wm.pdf
ultimate-pdf watermark input.pdf --image logo.png --pages 1,2 --output wm.pdf
```

### PDF ↔ Image

```bash
# PDF pages to images (writes into '<input>_images/' by default)
ultimate-pdf pdf-to-image input.pdf --dpi 200 --format png

# Images into a single PDF (one image per page)
ultimate-pdf image-to-pdf a.png b.jpg --output out.pdf
```

### OCR

Make a scanned PDF searchable, or extract recognized text (requires Tesseract):

```bash
ultimate-pdf ocr scan.pdf --output searchable.pdf          # searchable PDF
ultimate-pdf ocr scan.pdf --mode text --language eng       # prints text
```

### Markdown

Export a PDF's text content to Markdown:

```bash
ultimate-pdf markdown input.pdf                 # writes '<input>.md'
ultimate-pdf markdown input.pdf --pages 1-3 -o out.md
```

### Info

Show metadata and page count:

```bash
ultimate-pdf info input.pdf
```

## License

MIT — see [LICENSE](LICENSE).

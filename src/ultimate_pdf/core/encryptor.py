from pathlib import Path

from pypdf import PdfReader, PdfWriter


def encrypt_pdf(
    input_file: Path,
    output_file: Path,
    password: str,
) -> None:
  
  if not input_file.exists():
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

  if not password.strip():
        raise ValueError("Password cannot be empty.")

  reader = PdfReader(input_file)
  writer = PdfWriter()

  for page in reader.pages:
      writer.add_page(page)

  writer.encrypt(password)

  output_file.parent.mkdir(parents=True, exist_ok=True)

  with output_file.open("wb") as f:
      writer.write(f)


def decrypt_pdf(
    input_file: Path,
    output_file: Path,
    password: str,
) -> None:
    
  if not input_file.exists():
        raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

  if not password.strip():
        raise ValueError("Password cannot be empty.")

  reader = PdfReader(input_file)

  if reader.is_encrypted:
        result = reader.decrypt(password)

        # decrypt() returns 0 if the password is incorrect.
        if result == 0:
            raise ValueError("Incorrect password.")
  else:
        raise ValueError("PDF is not encrypted.")

  writer = PdfWriter()

  for page in reader.pages:
        writer.add_page(page)

  output_file.parent.mkdir(parents=True, exist_ok=True)

  with output_file.open("wb") as f:
        writer.write(f)
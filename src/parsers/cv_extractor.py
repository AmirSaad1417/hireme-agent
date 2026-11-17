import os
import tempfile
from pathlib import Path
import pymupdf  # PyMuPDF
from docx import Document


def extract_cv_text(uploaded_file) -> str:
    """
    Extract readable text from a Streamlit uploaded PDF or DOCX file.

    Args:
        uploaded_file: Streamlit UploadedFile object or file-like object with a .name attribute.

    Returns:
        str: Full extracted text as a single string.

    Raises:
        ValueError: If the file type is not PDF or DOCX, or if extraction fails.
    """
    file_name = getattr(uploaded_file, "name", "uploaded_file")
    suffix = Path(file_name).suffix.lower()

    if suffix not in [".pdf", ".docx"]:
        raise ValueError(
            f"Unsupported file type '{suffix}' for file '{file_name}'. "
            "Only PDF (.pdf) and Word (.docx) files are supported."
        )

    # Rewind stream pointer if seekable
    if hasattr(uploaded_file, "seek"):
        try:
            uploaded_file.seek(0)
        except Exception:
            pass

    # Read file content bytes
    if hasattr(uploaded_file, "getbuffer"):
        file_bytes = uploaded_file.getbuffer()
    elif hasattr(uploaded_file, "getvalue"):
        file_bytes = uploaded_file.getvalue()
    elif hasattr(uploaded_file, "read"):
        file_bytes = uploaded_file.read()
    else:
        raise ValueError(f"Cannot read file contents from object: {type(uploaded_file)}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_path = temp_file.name
        temp_file.write(file_bytes)

    try:
        if suffix == ".pdf":
            doc = pymupdf.open(temp_path)
            pages = [page.get_text() for page in doc]
            doc.close()
            text = "\n".join(pages).strip()
        elif suffix == ".docx":
            doc = Document(temp_path)
            lines = [p.text for p in doc.paragraphs if p.text]
            for table in doc.tables:
                for row in table.rows:
                    row_cells = []
                    for cell in row.cells:
                        c_text = cell.text.strip()
                        if c_text and (not row_cells or c_text != row_cells[-1]):
                            row_cells.append(c_text)
                    if row_cells:
                        lines.append(" | ".join(row_cells))
            text = "\n".join(lines).strip()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # Rewind stream pointer after reading if seekable
        if hasattr(uploaded_file, "seek"):
            try:
                uploaded_file.seek(0)
            except Exception:
                pass

    print(f"Extracted {len(text)} characters from {file_name}")
    return text


# Aliases
extract_text = extract_cv_text

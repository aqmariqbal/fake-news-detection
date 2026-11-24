import io
import re
import asyncio
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from image bytes using Windows local native OCR (winocr).
    Works 100% offline with zero cloud latency.
    """
    try:
        import winocr
        pil_img = Image.open(io.BytesIO(image_bytes))
        # Ensure image is in RGB
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")

        async def _run():
            res = await winocr.recognize_pil(pil_img)
            return res.text if hasattr(res, "text") else str(res)

        text = asyncio.run(_run())
        return text.strip()
    except Exception as e:
        return f"[OCR Notice: Could not extract text from image: {e}]"


def extract_text_from_file(file_bytes: bytes, filename: str) -> Tuple[str, str]:
    """
    Parses any uploaded file (Document, Image, Presentation, PDF, TXT)
    and extracts full plaintext for fact-checking and news evaluation.
    Returns: (extracted_text, file_type_description)
    """
    ext = Path(filename).suffix.lower()
    
    # 1. Image Files (PNG, JPG, JPEG, WEBP, BMP)
    if ext in [".png", ".jpg", ".jpeg", ".webp", ".bmp"]:
        text = extract_text_from_image(file_bytes)
        return text, f"Image OCR ({ext.upper()})"

    # 2. Word Documents (.docx)
    elif ext in [".docx", ".doc"]:
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            paragraphs.append(cell.text.strip())
            return "\n\n".join(paragraphs), "Microsoft Word Document (.docx)"
        except Exception as e:
            return f"[Error parsing DOCX: {e}]", "Word Document (Error)"

    # 3. PowerPoint Presentations (.pptx)
    elif ext in [".pptx", ".ppt"]:
        try:
            import pptx
            prs = pptx.Presentation(io.BytesIO(file_bytes))
            slide_texts = []
            for s_idx, slide in enumerate(prs.slides):
                texts = []
                for sh in slide.shapes:
                    if sh.has_text_frame:
                        for p in sh.text_frame.paragraphs:
                            if p.text.strip():
                                texts.append(p.text.strip())
                    if sh.has_table:
                        for row in sh.table.rows:
                            for cell in row.cells:
                                if cell.text.strip():
                                    texts.append(cell.text.strip())
                if texts:
                    slide_texts.append(f"--- Slide {s_idx+1} ---\n" + "\n".join(texts))
            return "\n\n".join(slide_texts), "PowerPoint Presentation (.pptx)"
        except Exception as e:
            return f"[Error parsing PPTX: {e}]", "PowerPoint Presentation (Error)"

    # 4. PDF Documents (.pdf)
    elif ext == ".pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            pages_text = []
            for p_idx, page in enumerate(reader.pages):
                txt = page.extract_text()
                if txt and txt.strip():
                    pages_text.append(f"--- Page {p_idx+1} ---\n{txt.strip()}")
            return "\n\n".join(pages_text), "PDF Document (.pdf)"
        except Exception as e:
            return f"[Error parsing PDF: {e}]", "PDF Document (Error)"

    # 5. Plain Text (.txt, .md, .csv)
    elif ext in [".txt", ".md", ".csv", ".json"]:
        try:
            text = file_bytes.decode("utf-8", errors="replace").strip()
            return text, "Plain Text File"
        except Exception as e:
            return f"[Error decoding text: {e}]", "Text File (Error)"

    else:
        # Fallback attempt text decode
        try:
            text = file_bytes.decode("utf-8", errors="ignore").strip()
            if text:
                return text, f"Generic File ({ext})"
        except Exception:
            pass
        return "[Unsupported file format. Please upload an Image, Word doc, PPT, PDF, or TXT file.]", "Unknown Format"

import io
import docx
from templates_file.minimal_template import build_minimal_template
from templates_file.modern_template import build_modern_template
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


class ResumeGenerator:
    def __init__(self):
        pass

    #PDF
    def generate_pdf(self, data, template="Minimal"):
        """
        Generate a PDF resume based on the given template.
        """
        buffer = io.BytesIO()

        if template == "Minimal":
            build_minimal_template(buffer, data)
        elif template == "Modern":
            build_modern_template(buffer, data)
        else:
            # Default fallback
            build_minimal_template(buffer, data)

        buffer.seek(0)
        return buffer

import io
import docx
from templates_pdf.minimal_template import build_minimal_template
from templates_pdf.modern_template import build_modern_template
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

    #docx
    def generate_docx(self, data, template="Minimal"):
        """
        Generate a DOCX resume (currently only Minimal style).
        """
        buffer = io.BytesIO()
        doc = Document()

        #personal-info
        personal_info = data.get("personalInfo", {})
        name = personal_info.get("name", "Your Name")
        header = doc.add_heading(name, level=0)
        header.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        contact_info = " | ".join(
            filter(None, [
                personal_info.get("email", ""),
                personal_info.get("phone", ""),
                personal_info.get("linkedin", ""),
                personal_info.get("github", "")
            ])
        )
        if contact_info:
            p = doc.add_paragraph(contact_info)
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        doc.add_paragraph()  # spacer

        #summary
        if data.get("summary"):
            doc.add_heading("Professional Summary", level=1)
            doc.add_paragraph(data["summary"])
            doc.add_paragraph()

        #skills
        if data.get("skills"):
            doc.add_heading("Skills", level=1)
            doc.add_paragraph(", ".join(data["skills"]))
            doc.add_paragraph()

        #edu
        if data.get("education"):
            doc.add_heading("Education", level=1)
            for edu in data["education"]:
                edu_text = f"{edu.get('degree', '')} — {edu.get('institution', '')} ({edu.get('year', '')})"
                doc.add_paragraph(edu_text)
            doc.add_paragraph()

        #exp
        if data.get("experience"):
            doc.add_heading("Experience", level=1)
            for exp in data["experience"]:
                role = f"{exp.get('jobTitle','')} - {exp.get('company','')} ({exp.get('duration','')})"
                doc.add_paragraph(role, style="Normal")

                if exp.get("description"):
                    for bullet in exp["description"].split("\n"):
                        if bullet.strip():
                            doc.add_paragraph(bullet.strip(), style="ListBullet")
            doc.add_paragraph()

        #projects
        if data.get("projects"):
            doc.add_heading("Projects", level=1)
            for proj in data["projects"]:
                proj_text = f"{proj.get('title','')} — {proj.get('description','')}"
                doc.add_paragraph(proj_text)
            doc.add_paragraph()

        #certifications
        if data.get("certifications"):
            doc.add_heading("Certifications", level=1)
            for cert in data["certifications"]:
                cert_text = f"{cert.get('title','')} — {cert.get('organization','')} ({cert.get('year','')})"
                doc.add_paragraph(cert_text)
            doc.add_paragraph()

        # Save DOCX to buffer
        doc.save(buffer)
        buffer.seek(0)
        return buffer

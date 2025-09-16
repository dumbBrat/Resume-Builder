from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


def build_minimal_template(buffer, data):
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=40,
        bottomMargin=30,
        leftMargin=50,
        rightMargin=50,
    )

    styles = getSampleStyleSheet()

    # Custom styles (no external fonts)
    styles.add(ParagraphStyle(name="MyHeader", fontName="Helvetica-Bold", fontSize=18, leading=22, spaceAfter=8, textColor=colors.black))
    styles.add(ParagraphStyle(name="MySectionHeader", fontName="Helvetica-Bold", fontSize=12, leading=16, spaceAfter=6, textColor=colors.black, spaceBefore=12))
    styles.add(ParagraphStyle(name="MyBody", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=4))
    styles.add(ParagraphStyle(name="MyBullet", fontName="Helvetica", fontSize=10, leading=12, leftIndent=15, bulletIndent=5))

    elements = []

    # --- Header ---
    personal_info = data.get("personalInfo", {})
    name = personal_info.get("name", "")
    contact_info = " | ".join(filter(None, [
        personal_info.get("email", ""),
        personal_info.get("phone", ""),
        personal_info.get("linkedin", ""),
        personal_info.get("github", "")
    ]))

    if name:
        elements.append(Paragraph(name, styles["MyHeader"]))
    if contact_info:
        elements.append(Paragraph(contact_info, styles["MyBody"]))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))
    elements.append(Spacer(1, 10))

    # --- Summary ---
    if data.get("summary"):
        elements.append(Paragraph("PROFESSIONAL SUMMARY", styles["MySectionHeader"]))
        elements.append(Paragraph(data["summary"], styles["MyBody"]))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))

    # --- Skills ---
    skills = data.get("skills", [])
    if skills:
        elements.append(Paragraph("SKILLS", styles["MySectionHeader"]))
        elements.append(Paragraph(", ".join(skills), styles["MyBody"]))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))

    # --- Education ---
    education = data.get("education", [])
    if education:
        elements.append(Paragraph("EDUCATION", styles["MySectionHeader"]))
        for edu in education:
            text = f"<b>{edu.get('degree','')}</b>, {edu.get('institution','')} ({edu.get('year','')})"
            elements.append(Paragraph(text, styles["MyBody"]))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))

    # --- Experience ---
    experience = data.get("experience", [])
    if experience:
        elements.append(Paragraph("EXPERIENCE", styles["MySectionHeader"]))
        for exp in experience:
            title_line = f"<b>{exp.get('jobTitle','')}</b>, {exp.get('company','')} ({exp.get('duration','')})"
            elements.append(Paragraph(title_line, styles["MyBody"]))
            if exp.get("description"):
                for bullet in exp["description"].split("\n"):
                    if bullet.strip():
                        elements.append(Paragraph(bullet.strip(), styles["MyBullet"]))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))

    # --- Projects ---
    projects = data.get("projects", [])
    if projects:
        elements.append(Paragraph("PROJECTS", styles["MySectionHeader"]))
        for proj in projects:
            elements.append(Paragraph(f"<b>{proj.get('title','')}</b> — {proj.get('description','')}", styles["MyBody"]))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))

    # --- Certifications ---
    certifications = data.get("certifications", [])
    if certifications:
        elements.append(Paragraph("CERTIFICATIONS", styles["MySectionHeader"]))
        for cert in certifications:
            elements.append(Paragraph(f"{cert.get('title','')} — {cert.get('organization','')} ({cert.get('year','')})", styles["MyBody"]))

    doc.build(elements)

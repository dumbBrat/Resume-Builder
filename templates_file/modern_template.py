from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, FrameBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def build_modern_template(buffer, data):
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=40,
        bottomMargin=30,
        leftMargin=40,
        rightMargin=40
    )
    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(name="Name", fontName="Helvetica-Bold", fontSize=18, textColor=colors.HexColor("#1a237e"), spaceAfter=6))
    styles.add(ParagraphStyle(name="SidebarHeader", fontName="Helvetica-Bold", fontSize=11, textColor=colors.white, backColor=colors.HexColor("#3949ab"), leftIndent=4, spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle(name="SidebarText", fontName="Helvetica", fontSize=9, textColor=colors.white, leftIndent=6, leading=12))
    styles.add(ParagraphStyle(name="SectionHeader", fontName="Helvetica-Bold", fontSize=12, textColor=colors.HexColor("#1a237e"), spaceBefore=10, spaceAfter=4))
    styles.add(ParagraphStyle(name="NormalText", fontName="Helvetica", fontSize=10, leading=14))

    # Layout: Sidebar + Main content
    width, height = A4
    sidebar_width = 140
    frames = [
        Frame(doc.leftMargin, doc.bottomMargin, sidebar_width, height - 70, showBoundary=0, leftPadding=6, rightPadding=6),
        Frame(doc.leftMargin + sidebar_width + 20, doc.bottomMargin, width - sidebar_width - 80, height - 70, showBoundary=0)
    ]

    doc.addPageTemplates([PageTemplate(frames=frames)])

    elements = []

    # --- SIDEBAR ---
    personal_info = data.get("personalInfo", {})
    elements.append(Paragraph(personal_info.get("name", "Your Name"), styles["Name"]))

    # Contact
    elements.append(Paragraph("CONTACT", styles["SidebarHeader"]))
    contact_lines = [
        personal_info.get("email", ""),
        personal_info.get("phone", ""),
        personal_info.get("linkedin", ""),
        personal_info.get("github", "")
    ]
    for line in filter(None, contact_lines):
        elements.append(Paragraph(line, styles["SidebarText"]))

    # Skills
    if data.get("skills"):
        elements.append(Paragraph("SKILLS", styles["SidebarHeader"]))
        for skill in data["skills"]:
            elements.append(Paragraph("• " + skill, styles["SidebarText"]))

    elements.append(FrameBreak())

    # --- MAIN AREA ---
    if data.get("summary"):
        elements.append(Paragraph("Professional Summary", styles["SectionHeader"]))
        elements.append(Paragraph(data["summary"], styles["NormalText"]))
        elements.append(Spacer(1, 8))

    if data.get("experience"):
        elements.append(Paragraph("Experience", styles["SectionHeader"]))
        for exp in data["experience"]:
            line = f"<b>{exp.get('jobTitle','')}</b>, {exp.get('company','')} ({exp.get('duration','')})"
            elements.append(Paragraph(line, styles["NormalText"]))
            if exp.get("description"):
                for bullet in exp["description"].split("\n"):
                    if bullet.strip():
                        elements.append(Paragraph("• " + bullet.strip(), styles["NormalText"]))
        elements.append(Spacer(1, 8))

    if data.get("education"):
        elements.append(Paragraph("Education", styles["SectionHeader"]))
        for edu in data["education"]:
            line = f"<b>{edu.get('degree','')}</b>, {edu.get('institution','')} ({edu.get('year','')})"
            elements.append(Paragraph(line, styles["NormalText"]))
        elements.append(Spacer(1, 8))

    if data.get("projects"):
        elements.append(Paragraph("Projects", styles["SectionHeader"]))
        for proj in data["projects"]:
            line = f"<b>{proj.get('title','')}</b> — {proj.get('description','')}"
            elements.append(Paragraph(line, styles["NormalText"]))
        elements.append(Spacer(1, 8))

    if data.get("certifications"):
        elements.append(Paragraph("Certifications", styles["SectionHeader"]))
        for cert in data["certifications"]:
            line = f"{cert.get('title','')} — {cert.get('organization','')} ({cert.get('year','')})"
            elements.append(Paragraph(line, styles["NormalText"]))
        elements.append(Spacer(1, 8))

    doc.build(elements)

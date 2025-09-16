import streamlit as st
import requests
import base64

API_URL = "http://localhost:5000"

st.set_page_config(page_title="AI Resume Builder", layout="wide")
st.title("📄 AI Resume Builder (Streamlit Test UI)")

# Sidebar for template selection
template = st.sidebar.selectbox("Choose Template", ["Minimal", "Modern"])

# --- Initialize session state ---
for key in ["education", "experience", "projects", "resumeData", "pdf_preview"]:
    if key not in st.session_state:
        st.session_state[key] = []

# -------------------- Personal Information --------------------
st.header("Personal Information")
personal_info = {
    "name": st.text_input("Full Name"),
    "email": st.text_input("Email"),
    "phone": st.text_input("Phone"),
    "linkedin": st.text_input("LinkedIn"),
    "github": st.text_input("GitHub"),
}

# -------------------- Career Summary --------------------
st.header("Career Summary")
summary = st.text_area("Summary")
if st.button("✨ Enhance Summary"):
    res = requests.post(f"{API_URL}/api/enhance-summary", json={"personalInfo": personal_info, "summary": summary})
    if res.ok:
        summary = res.json()["summary"]
        st.success("Summary enhanced ✅")

# -------------------- Skills --------------------
st.header("Skills")
skills = st.text_area("Skills (comma-separated)").split(",")
if st.button("✨ Enhance Skills"):
    res = requests.post(f"{API_URL}/api/enhance-skills", json={"skills": skills})
    if res.ok:
        skills = res.json()["skills"]
        st.success("Skills organized ✅")

# -------------------- Education --------------------
st.header("Education")
for i, edu in enumerate(st.session_state.education):
    st.text_input(f"Degree {i+1}", value=edu.get("degree", ""), key=f"degree_{i}")
    st.text_input(f"Institution {i+1}", value=edu.get("institution", ""), key=f"institution_{i}")
    st.text_input(f"Year {i+1}", value=edu.get("year", ""), key=f"year_{i}")

if st.button("+ Add Degree"):
    st.session_state.education.append({"degree": "", "institution": "", "year": ""})

if st.button("✨ Enhance Education"):
    res = requests.post(f"{API_URL}/api/enhance-education", json={"education": st.session_state.education})
    if res.ok:
        st.session_state.education = res.json()["education"]
        st.success("Education enhanced ✅")

# -------------------- Experience --------------------
st.header("Work Experience")
for i, exp in enumerate(st.session_state.experience):
    st.text_input(f"Job Title {i+1}", value=exp.get("jobTitle", ""), key=f"job_{i}")
    st.text_input(f"Company {i+1}", value=exp.get("company", ""), key=f"company_{i}")
    st.text_input(f"Duration {i+1}", value=exp.get("duration", ""), key=f"duration_{i}")
    st.text_area(f"Description {i+1}", value=exp.get("description", ""), key=f"description_{i}")

if st.button("+ Add Experience"):
    st.session_state.experience.append({"jobTitle": "", "company": "", "duration": "", "description": ""})

if st.button("✨ Enhance Experience"):
    res = requests.post(f"{API_URL}/api/enhance-experience", json={"experience": st.session_state.experience})
    if res.ok:
        st.session_state.experience = res.json()["experience"]
        st.success("Experience enhanced ✅")

# -------------------- Projects --------------------
st.header("Projects")
for i, proj in enumerate(st.session_state.projects):
    st.text_input(f"Title {i+1}", value=proj.get("title", ""), key=f"proj_title_{i}")
    st.text_area(f"Description {i+1}", value=proj.get("description", ""), key=f"proj_desc_{i}")
    st.text_input(f"Technologies {i+1}", value=proj.get("technologies", ""), key=f"proj_tech_{i}")

if st.button("+ Add Project"):
    st.session_state.projects.append({"title": "", "description": "", "technologies": ""})

if st.button("✨ Enhance Projects"):
    res = requests.post(f"{API_URL}/api/enhance-projects", json={"projects": st.session_state.projects})
    if res.ok:
        st.session_state.projects = res.json()["projects"]
        st.success("Projects enhanced ✅")

# -------------------- Resume Assembly --------------------
resume_data = {
    "personalInfo": personal_info,
    "summary": summary,
    "skills": [s.strip() for s in skills if s.strip()],
    "education": st.session_state.education,
    "experience": st.session_state.experience,
    "projects": st.session_state.projects,
}

# -------------------- Actions --------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Just Generate Resume"):
        res = requests.post(f"{API_URL}/generate-resume", json={"data": resume_data, "template": template})
        if res.ok:
            st.session_state.resumeData = res.json()["resumeData"]
            st.success("Resume preview ready ✅")

with col2:
    if st.button("✨ Enhance with AI"):
        res = requests.post(f"{API_URL}/api/generate-ai-resume", json={"data": resume_data, "template": template})
        if res.ok:
            st.session_state.resumeData = res.json()["data"]
            st.success("AI-enhanced resume ready ✅")

with col3:
    if st.button("⬇️ Download PDF"):
        res = requests.post(f"{API_URL}/download-resume", json={"data": st.session_state.get("resumeData", resume_data), "template": template, "format": "pdf"})
        if res.ok:
            st.download_button("Download Resume PDF", res.content, file_name="resume.pdf", mime="application/pdf")

# -------------------- PDF Preview --------------------
if "resumeData" in st.session_state:
    st.subheader("📑 Resume Preview (PDF)")
    res = requests.post(f"{API_URL}/download-resume", json={"data": st.session_state["resumeData"], "template": template, "format": "pdf"})
    if res.ok:
        pdf_bytes = res.content
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

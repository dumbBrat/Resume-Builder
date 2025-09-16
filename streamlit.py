import streamlit as st
import requests
import json

# -------------------
# CONFIG
# -------------------
API_BASE = "http://localhost:5000"  # Flask server URL

st.set_page_config(page_title="AI Resume Builder", layout="wide")

st.title("📄 AI Resume Builder (Streamlit + Flask)")

# -------------------
# Sidebar Input
# -------------------
st.sidebar.header("User Information")

name = st.sidebar.text_input("Full Name")
email = st.sidebar.text_input("Email")
phone = st.sidebar.text_input("Phone")
summary = st.sidebar.text_area("Professional Summary")

skills = st.sidebar.text_area("Skills (comma separated)", "Python, Flask, AI, Streamlit")

experience = st.sidebar.text_area(
    "Experience (JSON format)",
    '[{"role":"Software Engineer","company":"ABC Corp","years":"2021-2023","details":"Worked on web apps"}]'
)

education = st.sidebar.text_area(
    "Education (JSON format)",
    '[{"degree":"B.Tech in CSE","institution":"XYZ University","year":"2022"}]'
)

projects = st.sidebar.text_area(
    "Projects (JSON format)",
    '[{"name":"Resume Builder","description":"AI-powered resume builder using Flask & Streamlit"}]'
)

template = st.sidebar.selectbox("Choose Resume Template", ["Minimal", "Professional", "Creative"])
file_format = st.sidebar.selectbox("Download Format", ["pdf", "docx"])


# -------------------
# Helper Functions
# -------------------
def call_api(endpoint, payload):
    try:
        res = requests.post(f"{API_BASE}{endpoint}", json=payload)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"API Error {res.status_code}: {res.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None


# -------------------
# Main UI
# -------------------
st.subheader("Generate or Enhance Resume")

data = {
    "personalInfo": {"name": name, "email": email, "phone": phone},
    "summary": summary,
    "skills": [s.strip() for s in skills.split(",") if s.strip()],
    "experience": json.loads(experience),
    "education": json.loads(education),
    "projects": json.loads(projects),
}

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✨ Enhance Summary"):
        resp = call_api("/api/enhance-summary", data)
        if resp:
            st.success("Enhanced Summary")
            st.write(resp["summary"])

with col2:
    if st.button("🚀 Enhance Experience"):
        resp = call_api("/api/enhance-experience", {"experience": data["experience"]})
        if resp:
            st.success("Enhanced Experience")
            st.json(resp["experience"])

with col3:
    if st.button("🛠 Enhance Skills"):
        resp = call_api("/api/enhance-skills", {"skills": data["skills"]})
        if resp:
            st.success("Enhanced Skills")
            st.write(", ".join(resp["skills"]))


st.markdown("---")

if st.button("🤖 Generate AI Resume (Preview)"):
    resp = call_api("/api/generate-ai-resume", {"data": data, "template": template})
    if resp:
        st.success("AI Resume Preview")
        st.json(resp["data"])


if st.button("📥 Download Resume"):
    try:
        res = requests.post(f"{API_BASE}/download-resume", json={"data": data, "template": template, "format": file_format})
        if res.status_code == 200:
            file_bytes = res.content
            st.download_button(
                label=f"Download {file_format.upper()} Resume",
                data=file_bytes,
                file_name=f"{name.replace(' ', '-')}-Resume.{file_format}",
                mime="application/pdf" if file_format == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.error("Failed to download resume")
    except Exception as e:
        st.error(f"Download error: {e}")
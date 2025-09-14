from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import io
import json

# Import your helpers
from ai_agent import ResumeAIAgent
from doc_generator import ResumeGenerator

app = Flask(__name__)
CORS(app)

# Initialize helpers
ai_agent = ResumeAIAgent()
pdf_generator = ResumeGenerator()

# --- Enhancement Endpoints ---
@app.route("/api/enhance-summary", methods=["POST"])
def enhance_summary():
    try:
        data = request.json
        enhanced = ai_agent.enhance_summary(data)
        return jsonify({"success": True, "summary": enhanced})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/enhance-experience", methods=["POST"])
def enhance_experience():
    try:
        data = request.json
        enhanced = ai_agent.enhance_experience(data.get("experience", []))
        return jsonify({"success": True, "experience": enhanced})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/enhance-skills", methods=["POST"])
def enhance_skills():
    try:
        data = request.json
        organized = ai_agent.organize_skills(data.get("skills", []))
        all_skills = []
        for cat, skills in organized.items():
            all_skills.extend(skills)
        return jsonify({"success": True, "skills": list(set(all_skills))})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/enhance-education", methods=["POST"])
def enhance_education():
    try:
        data = request.json
        enhanced = []
        for edu in data.get("education", []):
            enhanced.append({
                "degree": edu.get("degree", "Diploma / Degree"),
                "institution": edu.get("institution", "Institute Name"),
                "year": edu.get("year", "Year"),
            })
        return jsonify({"success": True, "education": enhanced})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/enhance-projects", methods=["POST"])
def enhance_projects():
    try:
        data = request.json
        enhanced = ai_agent.enhance_projects(data.get("projects", []))
        return jsonify({"success": True, "projects": enhanced})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# --- RAW GENERATE (NO AI, PREVIEW ONLY) ---
@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    try:
        request_data = request.json
        data = request_data.get("data", {})
        template = request_data.get("template", "Minimal")

        if isinstance(data, str):
            data = json.loads(data)

        # Return JSON preview instead of file
        return jsonify({"success": True, "template": template, "resumeData": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- AI ENHANCED GENERATE (PREVIEW ONLY) ---
@app.route("/api/generate-ai-resume", methods=["POST"])
def generate_ai_resume():
    try:
        request_data = request.json
        data = request_data.get("data", {})
        template = request_data.get("template", "Minimal")

        if isinstance(data, str):
            data = json.loads(data)

        # Enhance each section
        data["summary"] = ai_agent.enhance_summary(data)
        data["experience"] = ai_agent.enhance_experience(data.get("experience", []))
        data["skills"] = list(set(sum(ai_agent.organize_skills(data.get("skills", [])).values(), [])))
        data["projects"] = ai_agent.enhance_projects(data.get("projects", []))

        return jsonify({"success": True, "template": template, "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- DOWNLOAD RESUME (PDF/DOCX) ---
@app.route("/download-resume", methods=["POST"])
def download_resume():
    try:
        request_data = request.json
        data = request_data.get("data", {})
        template = request_data.get("template", "Minimal")
        file_format = request_data.get("format", "pdf").lower()

        # Extract candidate name (default fallback)
        personal_info = data.get("personalInfo", {})
        candidate_name = personal_info.get("name", "User").replace(" ", "-")
        filename = f"{candidate_name}-Resume.{file_format}"

        if file_format == "pdf":
            buffer = pdf_generator.generate_pdf(data, template)
            return send_file(
                buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=filename
            )

        elif file_format == "docx":
            buffer = pdf_generator.generate_docx(data, template)
            return send_file(
                buffer,
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                as_attachment=True,
                download_name=filename
            )

        else:
            return jsonify({"error": "Unsupported format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Health/Test Endpoints ---
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/api/test", methods=["POST"])
def test_ai():
    try:
        data = request.json
        msg = data.get("message", "Hello AI")
        result = ai_agent.test_message(msg)
        return jsonify({"input": msg, "output": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Resume Builder AI Agent Server...")
    app.run(debug=True, host="0.0.0.0", port=5000)

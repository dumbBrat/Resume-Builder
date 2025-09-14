from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any, List


class ResumeAIAgent:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2", temperature=0.7)
        self.parser = StrOutputParser()


        #Templates
        #Summary
        self.summary_prompt = ChatPromptTemplate.from_template("""
        Write a short professional summary for {name}.

        Details:
        - Experience: {experience}
        - Skills: {skills}
        - Education: {education}

        Rules:
        - Strictly 2–3 sentences.
        - Tone: formal, concise, resume-appropriate.
        - Use provided experience, skills, and education when available.
        - If little or no information is provided, generate a generic professional summary.
        - Do NOT ask for more information.
        - Do NOT mention missing details.
        - Do NOT output instructions or questions.
        Output only the summary text.
        """)

        # Experience
        self.experience_prompt = ChatPromptTemplate.from_template("""
        Enhance this work experience into exactly 3 concise bullet points.

        Job Title: {job_title}
        Company: {company}
        Duration: {duration}
        Basic Description: {basic_description}

        Rules:
        - Max 15 words per bullet.
        - Begin each bullet with a strong action verb.
        - Use only the provided info.
        - Do NOT invent details.
        - Do NOT add explanations, headers, or prefaces like "Here are...".
        - Output ONLY the 3 bullet points, one per line, starting with "- ".
        """)

        # Skills
        self.skills_prompt = ChatPromptTemplate.from_template("""
        Organize the following skills into categories.

        Skills: {skills_list}

        Rules:
        - Categories: Programming Languages, Frameworks/Tools, Soft Skills.
        - Max 6 skills per category.
        - Only use provided skills (no new ones).
        - Remove duplicates and keep concise wording.
        - If no skills are provided, return "Soft Skills: Communication, Teamwork, Adaptability"

        Format:
        Category: skill1, skill2
        """)

        # Projects
        self.project_prompt = ChatPromptTemplate.from_template("""
        Write a concise description for the project "{title}" using {technologies}.
        - Strictly 1–2 sentences.
        - Highlight functionality or impact only.
        - If no description or technologies are provided, return "{title} was developed to demonstrate practical application of technical skills."
        """)

    #Methods

    def enhance_summary(self, data: Dict[str, Any]) -> str:
        chain = self.summary_prompt | self.llm | self.parser
        result = chain.invoke({
            "name": data.get("personalInfo", {}).get("name", "the candidate"),
            "experience": self._summarize_experience(data.get("experience", [])),
            "skills": ", ".join(data.get("skills", [])) or "general skills",
            "education": self._summarize_education(data.get("education", [])),
        }).strip()

        # --- SAFETY NET ---
        if not result or "i don't have" in result.lower() or "please provide" in result.lower():
            return "Motivated professional eager to contribute skills and grow within a dynamic organization."
        return result

    def enhance_experience(self, experience_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enhanced = []
        chain = self.experience_prompt | self.llm | self.parser

        for exp in experience_list:
            if exp.get("jobTitle") or exp.get("company"):
                desc = chain.invoke({
                    "job_title": exp.get("jobTitle", "Role"),
                    "company": exp.get("company", "Company"),
                    "duration": exp.get("duration", ""),
                    "basic_description": exp.get("description", "") or ""
                }).strip()

                # --- SAFETY NET ---
                if not desc or "please provide" in desc.lower() or "i don't have" in desc.lower():
                    desc = "- Assisted with daily tasks and supported team projects.\n- Contributed to assigned responsibilities.\n- Gained practical exposure in the role."

                exp["description"] = desc
            enhanced.append(exp)

        return enhanced

    def organize_skills(self, skills_list: List[str]) -> Dict[str, List[str]]:
        if not skills_list:
            return {"Soft Skills": ["Communication", "Teamwork", "Adaptability"]}

        chain = self.skills_prompt | self.llm | self.parser
        organized_text = chain.invoke({"skills_list": ", ".join(skills_list)}).strip()

        # --- SAFETY NET ---
        if not organized_text or "please provide" in organized_text.lower() or "i don't have" in organized_text.lower():
            return {"Soft Skills": ["Communication", "Teamwork", "Adaptability"]}

        skills_dict = {}
        for line in organized_text.split("\n"):
            if ":" in line:
                category, skills = line.split(":", 1)
                skills_dict[category.strip()] = [s.strip() for s in skills.split(",") if s.strip()]

        return skills_dict if skills_dict else {"Skills": skills_list}

    def enhance_projects(self, projects_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enhanced = []
        chain = self.project_prompt | self.llm | self.parser

        for proj in projects_list:
            if proj.get("title"):
                desc = chain.invoke({
                    "title": proj.get("title", ""),
                    "technologies": proj.get("technologies", "") or ""
                }).strip()

                # --- SAFETY NET ---
                if not desc or "please provide" in desc.lower() or "i don't have" in desc.lower():
                    desc = f"{proj.get('title', 'Project')} was developed to demonstrate practical application of technical skills."

                proj["description"] = desc
            enhanced.append(proj)

        return enhanced

    #Helpers
    def _summarize_experience(self, experience_list: List[Dict[str, Any]]) -> str:
        if not experience_list:
            return "No work experience provided"
        return "; ".join(
            f"{exp.get('jobTitle', '')} at {exp.get('company', '')}"
            for exp in experience_list if exp.get("jobTitle") and exp.get("company")
        )

    def _summarize_education(self, education_list: List[Dict[str, Any]]) -> str:
        if not education_list:
            return "No education information provided"
        return "; ".join(
            f"{edu.get('degree', '')} from {edu.get('institution', '')}"
            for edu in education_list if edu.get("degree") and edu.get("institution")
        )

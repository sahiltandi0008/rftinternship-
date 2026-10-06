import streamlit as st
import pandas as pd
import re
import io

st.set_page_config(
    page_title="AI Resume Screening Tool",
    layout="wide"
)

st.title("🤖 AI Resume Screening Tool")

st.write("Upload multiple resumes and compare them with a job description.")

job_description = st.text_area(
    "Enter Job Description",
    height=180,
    placeholder="Example: Python, Machine Learning, SQL, Pandas, NumPy, Scikit-learn, Deep Learning, Communication"
)

uploaded_files = st.file_uploader(
    "Upload Resume Files",
    type=["txt", "csv"],
    accept_multiple_files=True
)

skill_database = [
    "Python",
    "Java",
    "C++",
    "C",
    "SQL",
    "Excel",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "TensorFlow",
    "PyTorch",
    "NLP",
    "Computer Vision",
    "Data Science",
    "Data Analysis",
    "Power BI",
    "Tableau",
    "Git",
    "GitHub",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Communication",
    "Leadership"
]

def extract_name(text, filename):
    match = re.search(
        r"(?:Name|Candidate Name)\s*[:\-]\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return filename.rsplit(".", 1)[0]

def extract_experience(text):
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years|year|yrs|yr)",
        text,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    return 0

def extract_education(text):
    education_keywords = [
        "B.Tech",
        "B.E",
        "Bachelor",
        "M.Tech",
        "M.E",
        "Master",
        "MBA",
        "BCA",
        "MCA",
        "B.Sc",
        "M.Sc",
        "PhD"
    ]

    found = []

    for item in education_keywords:
        if re.search(re.escape(item), text, re.IGNORECASE):
            found.append(item)

    if found:
        return ", ".join(dict.fromkeys(found))

    return "Not Specified"

def extract_skills(text):
    found = []

    for skill in skill_database:
        if re.search(
            r"\b" + re.escape(skill) + r"\b",
            text,
            re.IGNORECASE
        ):
            found.append(skill)

    return list(dict.fromkeys(found))

if job_description and uploaded_files:

    job_skills = extract_skills(job_description)

    if not job_skills:
        st.warning("No recognized skills found in the job description.")

    results = []

    for file in uploaded_files:

        if file.name.lower().endswith(".txt"):
            text = file.read().decode("utf-8", errors="ignore")

        else:
            file.seek(0)

            data = pd.read_csv(file)

            text = " ".join(
                data.astype(str).fillna("").values.flatten()
            )

        candidate_name = extract_name(text, file.name)

        candidate_skills = extract_skills(text)

        experience = extract_experience(text)

        education = extract_education(text)

        matched_skills = [
            skill for skill in job_skills
            if skill.lower() in [
                x.lower() for x in candidate_skills
            ]
        ]

        missing_skills = [
            skill for skill in job_skills
            if skill.lower() not in [
                x.lower() for x in candidate_skills
            ]
        ]

        if job_skills:
            skill_score = (
                len(matched_skills) / len(job_skills)
            ) * 70
        else:
            skill_score = 0

        experience_score = min(experience / 5, 1) * 20

        education_score = 10 if education != "Not Specified" else 0

        match_score = min(
            skill_score + experience_score + education_score,
            100
        )

        if match_score >= 70:
            status = "Shortlisted"
        else:
            status = "Not Shortlisted"

        results.append({
            "Name": candidate_name,
            "Skills": ", ".join(candidate_skills),
            "Matched Skills": ", ".join(matched_skills),
            "Missing Skills": ", ".join(missing_skills),
            "Experience": experience,
            "Education": education,
            "Match Score": round(match_score, 2),
            "Status": status
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "Match Score",
        ascending=False
    ).reset_index(drop=True)

    results_df["Rank"] = results_df.index + 1

    results_df = results_df[
        [
            "Rank",
            "Name",
            "Skills",
            "Matched Skills",
            "Missing Skills",
            "Experience",
            "Education",
            "Match Score",
            "Status"
        ]
    ]

    st.subheader("📊 Candidate Ranking")

    st.dataframe(
        results_df,
        use_container_width=True
    )

    st.subheader("🎯 Candidate Details")

    selected_candidate = st.selectbox(
        "Select Candidate",
        results_df["Name"].tolist()
    )

    candidate = results_df[
        results_df["Name"] == selected_candidate
    ].iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rank",
        int(candidate["Rank"])
    )

    col2.metric(
        "Match Score",
        f"{candidate['Match Score']}%"
    )

    col3.metric(
        "Experience",
        f"{candidate['Experience']} years"
    )

    col4.metric(
        "Status",
        candidate["Status"]
    )

    st.write("### 👤 Name")
    st.write(candidate["Name"])

    st.write("### 🎓 Education")
    st.write(candidate["Education"])

    st.write("### 💻 Skills")
    st.write(candidate["Skills"])

    st.write("### ✅ Matched Skills")

    if candidate["Matched Skills"]:
        st.success(candidate["Matched Skills"])
    else:
        st.warning("No matching skills found.")

    st.write("### ❌ Missing Skills")

    if candidate["Missing Skills"]:
        st.error(candidate["Missing Skills"])
    else:
        st.success("No required skills are missing.")

    st.subheader("🏆 Shortlisted Candidates")

    shortlisted = results_df[
        results_df["Status"] == "Shortlisted"
    ]

    st.dataframe(
        shortlisted,
        use_container_width=True
    )

    st.subheader("📥 Export Shortlisted Candidates")

    shortlisted_csv = shortlisted.to_csv(
        index=False
    )

    st.download_button(
        label="Download Shortlisted Candidates",
        data=shortlisted_csv,
        file_name="shortlisted_candidates.csv",
        mime="text/csv"
    )

    st.subheader("📥 Export Complete Screening Report")

    complete_csv = results_df.to_csv(
        index=False
    )

    st.download_button(
        label="Download Complete Report",
        data=complete_csv,
        file_name="resume_screening_report.csv",
        mime="text/csv"
    )

elif not uploaded_files:

    st.info("Please upload one or more TXT or CSV resume files.")

elif not job_description:

    st.info("Please enter a job description.")


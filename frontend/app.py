import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("JobDecode AI 🚀")

tab1, tab2, tab3 = st.tabs(["Upload JD", "Upload Resume", "Analyze"])

# ---------------- JD UPLOAD ----------------
with tab1:
    st.header("Upload Job Description")

    option = st.radio("Choose input type:", ["Paste Text", "Upload PDF"])

    jd_text = ""

    if option == "Paste Text":
        jd_text = st.text_area("Enter Job Description")

        if st.button("Submit Text JD"):
            if jd_text.strip():
                res = requests.post(
                    f"{BASE_URL}/ingest",
                    json={"text": jd_text}
                )
                st.success(res.json())
            else:
                st.error("Please enter text")

    else:
        jd_file = st.file_uploader("Upload JD PDF")

        if st.button("Upload PDF JD"):
            if jd_file:
                files = {
                    "file": (jd_file.name, jd_file.getvalue(), "application/pdf")
                }
                res = requests.post(
                    f"{BASE_URL}/upload-job-description",
                    files=files
                )
                st.success(res.json())
            else:
                st.error("Please upload a file")

# ---------------- RESUME UPLOAD ----------------
with tab2:
    st.header("Upload Resume")

    resume_file = st.file_uploader("Upload Resume PDF")

    if st.button("Upload Resume"):
        if resume_file:
            files = {
                "file": (resume_file.name, resume_file.getvalue(), "application/pdf")
            }
            res = requests.post(f"{BASE_URL}/upload-resume", files=files)
            st.success(res.json())
        else:
            st.error("Please upload a file")

# ---------------- ANALYSIS ----------------
with tab3:
    st.header("Resume Analysis")

    if st.button("Analyze Resume"):
        res = requests.post(f"{BASE_URL}/analyze-resume")
        st.markdown(res.json()["analysis"])
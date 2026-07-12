import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="JobDecode AI",
    page_icon="🚀",
    layout="wide"
)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "jd_uploaded" not in st.session_state:
    st.session_state.jd_uploaded = False

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

st.title("🚀 JobDecode AI")
st.caption("AI-powered Resume Analyzer with ATS Matching")

# Sidebar
st.sidebar.title("📌 Workflow")
if st.session_state.jd_uploaded:
    st.sidebar.success("1️⃣ Job Description Uploaded")
else:
    st.sidebar.warning("1️⃣ Upload Job Description")

if st.session_state.resume_uploaded:
    st.sidebar.success("2️⃣ Resume Uploaded")
else:
    st.sidebar.warning("2️⃣ Upload Resume")

if st.session_state.analysis_done:
    st.sidebar.success("3️⃣ Analysis Complete")
else:
    st.sidebar.warning("3️⃣ Analyze Resume")

st.sidebar.divider()

st.sidebar.info("""
This application compares your resume with a Job Description using:

- 📄 PDF Processing
- 🔍 RAG (FAISS)
- 🤖 LLM Analysis
- 📊 ATS Matching
""")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📄 Job Description", "📄 Resume", "📊 Analysis", "💬 Chat"]
)

# ---------------- JD UPLOAD ----------------
with tab1:
    st.subheader("📄 Upload Job Description")

    option = st.radio(
        "Choose input type:",
        ["Paste Text", "Upload PDF"]
    )

    if option == "Paste Text":

        jd_text = st.text_area("Enter Job Description")

        if st.button("Submit Job Description"):

            if jd_text.strip():

                with st.spinner("Uploading Job Description..."):
                    res = requests.post(
                        f"{BASE_URL}/ingest",
                        json={"text": jd_text}
                    )

                data = res.json()

                if "message" in data:
                    st.success(f"✅ {data['message']}")
                    st.session_state.jd_uploaded = True

                elif "error" in data:
                    st.error(data["error"])

                else:
                    st.error("Unexpected response from server.")

            else:
                st.error("Please enter a Job Description.")
                

    else:

        jd_file = st.file_uploader(
            "Upload JD PDF",
            type=["pdf"]
        )

        if st.button("Upload JD PDF"):

            if jd_file:

                files = {
                    "file": (
                        jd_file.name,
                        jd_file.getvalue(),
                        "application/pdf"
                    )
                }

                with st.spinner("Uploading Job Description..."):
                    res = requests.post(
                        f"{BASE_URL}/upload-job-description",
                        files=files
                    )

                if res.status_code == 200:
                    st.success(f"✅ {res.json()['message']}")
                    st.session_state.jd_uploaded = True
                else:
                    st.error("Upload failed.")

            else:
                st.error("Please upload a PDF.")

# ---------------- RESUME UPLOAD ----------------
with tab2:

    st.subheader("📄 Upload Resume")

    resume_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    if st.button("Upload Resume"):

        if resume_file:

            files = {
                "file": (
                    resume_file.name,
                    resume_file.getvalue(),
                    "application/pdf"
                )
            }

            with st.spinner("Uploading Resume..."):
                res = requests.post(
                    f"{BASE_URL}/upload-resume",
                    files=files
                )

            if res.status_code == 200:
                st.success(f"✅ {res.json()['message']}")
                st.session_state.resume_uploaded = True
            else:
                st.error("Upload failed.")

        else:
            st.error("Please upload a PDF.")

# ---------------- ANALYSIS ----------------
with tab3:

    st.subheader("📊 Resume Analysis")

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing Resume..."):
            res = requests.post(
                f"{BASE_URL}/analyze-resume"
            )

        if res.status_code == 200:

            data = res.json()

            if "analysis" in data:
                st.session_state.analysis_done = True
                st.markdown(data["analysis"])

            elif "error" in data:
                st.error(data["error"])

            else:
                st.error("Unexpected response from server.")

        else:
            st.error("Failed to analyze resume.")
# ---------------- CHAT ----------------
with tab4:

    st.subheader("💬 Ask Questions About the Job Description")

    user_question = st.text_input(
        "Ask a question",
        placeholder="Example: What skills are required?"
    )

    if st.button("Send"):

        if user_question.strip():

            with st.spinner("Thinking..."):

                res = requests.post(
                    f"{BASE_URL}/chat",
                    json={
                        "prompt": user_question
                    }
                )

            if res.status_code == 200:

                answer = res.json()["answer"]

                st.session_state.messages.append(
                    ("You", user_question)
                )

                st.session_state.messages.append(
                    ("AI", answer)
                )

            else:
                st.error("Unable to get a response.")

        else:
            st.warning("Please enter a question.")

    st.divider()

    for sender, message in st.session_state.messages:

        if sender == "You":
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)
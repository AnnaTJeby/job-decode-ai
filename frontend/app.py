import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="JobDecode AI",
    page_icon="🚀",
    layout="wide"
)
st.title("JobDecode AI")
st.write("Welcome to your AI-powered Job Description Assistant!")
if st.button("Connect to Backend"):
    response = requests.get(f"{API_URL}/hello")
    data = response.json()
    st.success(data["message"])
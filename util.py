import streamlit as st
import clipboard


def toast_error(msg):
    st.toast(f":red[{msg}]", icon="🚨")


def generate_prompt(job_title, job_company, job_description):
    prompt = f"Write a cover letter for {job_title} at {job_company} with the following description: {job_description}"
    return prompt


def copy_to_clipboard():
    clipboard.copy(st.session_state.letter)
    st.toast("Cover Letter Copied", icon="✅")

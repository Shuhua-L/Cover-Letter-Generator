import streamlit as st
import clipboard
from pdf import extract_text_from_pdf


def toast_error(msg):
    st.toast(f":red[{msg}]", icon="🚨")


def copy_to_clipboard():
    clipboard.copy(st.session_state.letter)
    st.toast(":green[Cover Letter Copied]", icon="✅")


def generate_prompt(title, description, include_resume, resume):
    prompt = f"Job title: ```{title}```. \nJob description: ```{description}```"
    if include_resume:
        text_resume = extract_text_from_pdf(resume)
        prompt += f". \nResume: ```{text_resume}```"

    return prompt

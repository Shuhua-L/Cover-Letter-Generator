import streamlit as st
import clipboard


def toast_error(msg):
    st.toast(f":red[{msg}]", icon="🚨")


def copy_to_clipboard():
    clipboard.copy(st.session_state.letter)
    st.toast("Cover Letter Copied", icon="✅")

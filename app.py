import os
import streamlit as st

import oai
from util import toast_error, generate_prompt, copy_to_clipboard

# App title
st.set_page_config(
    page_title="Cover Letter Generator", page_icon="📮", layout="centered"
)


def onclick_submit():
    if st.session_state.n_requests >= 5:
        toast_error(
            "Too many requests. Please wait a few seconds before generating another Tweet."
        )
        st.session_state.n_requests = 1
        return

    if not job_title:
        toast_error("Please enter job title")
        return
    elif not job_description:
        toast_error("Please enter job description")
        return

    st.session_state.letter = ""
    prompt = generate_prompt(job_title, job_company, job_description)

    with text_spinner_placeholder:
        with st.spinner("Please wait while your letter is being generated..."):
            openai = oai.Openai()
            flagged = openai.moderate(prompt)
            if flagged:
                toast_error("Input flagged as inappropriate.")
                return

            else:
                st.session_state.n_requests += 1
                st.session_state.letter = (
                    openai.complete(prompt=prompt).strip().replace('"', "")
                )


def initializeState(list):
    for state in list:
        if state not in st.session_state:
            if state == "n_requests":
                st.session_state[state] = 0
            elif state == "api_connection":
                st.session_state[state] = False
            else:
                st.session_state[state] = ""


# def copy_to_clipboard():
#     clipboard.copy(st.session_state.letter)
#     st.toast("Cover Letter Copied", icon="✅")


# Configure Streamlit page and state
initializeState(["letter", "n_requests", "api_connection"])


# Force responsive layout for columns also on mobiles
st.write(
    """<style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>""",
    unsafe_allow_html=True,
)

# Render sidebar
with st.sidebar:
    st.subheader("Settings")
    st.write("This generator is created using the ChatGPT-3.5 model.")
    openai_key = st.text_input(
        "Enter OpenAI API token:", type="password", key="OPENAI_API_KEY"
    )

    try:
        if "OPENAI_API_KEY" in st.secrets and st.secrets["OPENAI_API_KEY"]:
            st.success("API key already provided!", icon="✅")
            openai_key = st.secrets["OPENAI_API_KEY"]
    except FileNotFoundError:
        pass

    if not openai_key:
        st.warning("Please enter your credentials!", icon="⚠️")
        st.write("[Click here to get your OpenAI key](https://openai.com/api)")
    elif openai_key and oai.check_openai_api_key(openai_key):
        st.success("Proceed to entering your prompt message!", icon="👉")
        os.environ["OPENAI_API_KEY"] = openai_key
        st.session_state.api_connection = True
    else:
        st.error("Invalid OpenAI API key.", icon="‼️")

    # st.write("---")
    # st.write("Made with ❤️  by [Shuhua](https://twitter.com/Shuhualll)")

# Render main page
st.title("Cover Letter Generator")

# Render form
job = st.form(key="job_info_form")
job_title = job.text_input(label="Job title :red[*]", key="title")
job_company = job.text_input(label="Company") or "Company"
job_description = job.text_area(label="Job description :red[*]", key="description")
submit = job.form_submit_button(
    label="Generate Cover Letter",
    type="primary",
    disabled=not st.session_state.api_connection,
    help="Please enter your credentials in the sidebar to generate your cover letter."
    if not st.session_state.api_connection
    else None,
)
text_spinner_placeholder = st.empty()
if submit:
    onclick_submit()


if st.session_state.letter:
    ht = int(len(st.session_state.letter) / 100 * 30)
    st.markdown("""---""")
    st.text_area(
        label="Cover Letter", value=st.session_state.letter, height=ht, key="letter"
    )
    st.button(label="Copy", on_click=copy_to_clipboard, key="copy")

import os
import streamlit as st
import clipboard
import oai

# App title
st.set_page_config(
    page_title="Cover Letter Generator", page_icon="📮", layout="centered"
)


def generate_cover_letter(title, company, description):
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another Tweet."
        st.session_state.n_requests = 1
        return

    st.session_state.letter = ""
    st.session_state.text_error = ""
    prompt = f"Write a cover letter for {title} at {company} with the following description: {description}"

    if not description:
        st.session_state.text_error = "Please enter description"
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your letter is being generated..."):
            openai = oai.Openai()
            flagged = openai.moderate(prompt)
            if flagged:
                st.session_state.text_error = "Input flagged as inappropriate."
                return

            else:
                st.session_state.text_error = ""
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


def on_click_copy():
    clipboard.copy(st.session_state.letter)
    st.toast("Cover Letter Copied", icon="✅")


# Configure Streamlit page and state
initializeState(
    [
        "letter",
        "title",
        "company",
        "description",
        "text_error",
        "n_requests",
        "api_connection",
    ]
)


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

    if "OPENAI_API_KEY" in st.secrets and st.secrets["OPENAI_API_KEY"]:
        st.success("API key already provided!", icon="✅")
        openai_key = st.secrets["OPENAI_API_KEY"]

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

title = st.text_input(label="Job title *")
company = st.text_input(label="Company") or "Company"
description = st.text_area(label="Job description *")
st.button(
    label="Generate Cover Letter",
    type="primary",
    key="submit",
    on_click=generate_cover_letter,
    args=(title, company, description),
    disabled=not st.session_state.api_connection,
    help="Please enter your credentials in the sidebar to generate your cover letter.",
)

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.letter:
    ht = int(len(st.session_state.letter) / 100 * 30)
    st.markdown("""---""")
    st.text_area(label="Cover Letter", value=st.session_state.letter, height=ht)
    st.button(label="Copy", type="primary", on_click=on_click_copy)

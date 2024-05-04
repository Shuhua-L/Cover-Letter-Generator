import streamlit as st
import clipboard
import oai

# App title
st.set_page_config(page_title="Cover Letter Generator", page_icon="📮", layout="centered")

def generate_cover_letter(title, company, description):
  if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another Tweet."
        st.session_state.n_requests = 1
        return

  st.session_state.letter = ""
  st.session_state.text_error = ""
  prompt = f"Write a cover letter for {title} at {company} with the following description: {description}"

  if not description:
    st.session_state.text_error = "Please enter a topic"
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
        else:
          st.session_state[state] = ""

def on_click_copy():
    clipboard.copy(st.session_state.letter)
    st.toast("Cover Letter Copied", icon="✅")

# Configure Streamlit page and state
initializeState(['letter', 'title', 'company', 'description', 'text_error', 'n_requests'])


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

# Render Streamlit page
st.title('Cover Letter Generator')

title = st.text_input(label="Job title")
company = st.text_input(label= "Company")
description = st.text_area(label="Job description")
st.button(label="Generate Cover Letter", type="primary",
          on_click=generate_cover_letter, args=(title, company, description))

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.letter:
    ht=int(len(st.session_state.letter) / 100 * 30)
    st.markdown("""---""")
    st.text_area(label="Cover Letter", value=st.session_state.letter, height=ht)
    st.button(label="Copy", type="primary", on_click=on_click_copy)

import os
import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest
from tests.sample_data import job


def test_submit_without_job_description():
    key = None
    if "OPENAI_API_KEY" in st.secrets:
        key = st.secrets["OPENAI_API_KEY"]
    elif "OPENAI_API_KEY" in os.environ:
        key = os.environ["OPENAI_API_KEY"]
    else:
        # Skip test if no API key is provided
        return

    # Initialize app and ensure submit button is enabled
    at = AppTest.from_file("app.py", default_timeout=10)
    at.secrets["OPENAI_API_KEY"] = key
    at.run()
    assert at.button("submit").disabled is False
    assert len(at.success) == 2

    # Submit and verify error
    assert at.text_area("description").value == ""
    at.button("submit").click().run()
    assert len(at.error) == 1
    assert at.error[0].value == "Please enter job description"


@pytest.mark.skip(reason="Skipping test due to API usage")
def test_submit_with_job_description():
    key = None
    if "OPENAI_API_KEY" in st.secrets:
        key = st.secrets["OPENAI_API_KEY"]
    elif "OPENAI_API_KEY" in os.environ:
        key = os.environ["OPENAI_API_KEY"]
    else:
        # Skip test if no API key is provided
        return

    # Initialize app and ensure submit button is enabled
    at = AppTest.from_file("app.py", default_timeout=10)
    at.secrets["OPENAI_API_KEY"] = key
    at.run()
    assert at.button("submit").disabled is False
    assert len(at.success) == 2

    # fill in job description and submit
    at.text_area("description").input(job["description"]).run()
    at.button("submit").click().run()

    assert at.text_area("letter").value is not None
    assert len(at.text_area("letter").value) > 50

    # Verify copy button
    assert at.button("copy").disabled is False
    at.button("copy").click().run()
    assert at.toast[0].value == "Cover Letter Copied"

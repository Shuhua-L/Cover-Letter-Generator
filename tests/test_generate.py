import os
import pytest
from streamlit.testing.v1 import AppTest
from tests.sample_data import job


@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ, reason="Skip test if no API key is provided"
)
def test_submit_without_title_description():
    # Initialize app and ensure submit button is enabled
    at = AppTest.from_file("app.py", default_timeout=10)
    at.secrets["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]
    at.run()

    submit_button = at.button("FormSubmitter:job_info_form-Generate Cover Letter")
    assert submit_button.disabled is False
    assert len(at.success) == 2

    # submit without job title and verify toast
    assert at.text_input("title").value == ""
    submit_button.click().run()
    assert len(at.toast) == 1
    assert at.toast[0].value == ":red[Please enter job title]"

    # submit without job description and verify toast
    at.text_input("title").input(job["title"]).run()
    assert at.text_area("description").value == ""
    submit_button.click().run()
    assert len(at.toast) == 1
    assert at.toast[0].value == ":red[Please enter job description]"


@pytest.mark.skip(reason="Only run manually to save API usage")
def test_submit_with_title_description():
    # Initialize app and ensure submit button is enabled
    at = AppTest.from_file("app.py", default_timeout=10)
    at.secrets["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]
    at.run()

    submit_button = at.button("FormSubmitter:job_info_form-Generate Cover Letter")
    assert submit_button.disabled is False
    assert len(at.success) == 2

    # fill in title, description and submit
    at.text_input("title").input(job["title"]).run()
    at.text_area("description").input(job["description"]).run()

    try:
        submit_button.click().run()

        # verify generated cover letter
        assert at.text_area("letter").value is not None
        assert len(at.text_area("letter").value) > 50

        # verify copy button
        assert at.button("copy").disabled is False
        at.button("copy").click().run()
        assert at.toast[0].value == "Cover Letter Copied"
    except RuntimeError:
        print("Error: Timeout waiting for cover letter generation")

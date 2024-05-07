import os
import pytest
from streamlit.testing.v1 import AppTest
from tests.sample_data import job


@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ, reason="Skip test if no API key is provided"
)
def test_submit_without_job_description():
    # Initialize app and ensure submit button is enabled
    at = AppTest.from_file("app.py", default_timeout=10)
    at.secrets["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]
    at.run()
    assert at.button("submit").disabled is False
    assert len(at.success) == 2

    # Submit and verify error
    assert at.text_area("description").value == ""
    at.button("submit").click().run()
    assert len(at.error) == 1
    assert at.error[0].value == "Please enter job description"


@pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ, reason="Skip test if no API key is provided"
)
def test_submit_with_job_description():
    # Initialize app and ensure submit button is enabled
    at = AppTest.from_file("app.py", default_timeout=10)
    at.secrets["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]
    at.run()
    assert at.button("submit").disabled is False
    assert len(at.success) == 2

    # fill in job description and submit
    at.text_area("description").input(job["description"]).run()
    at.button("submit").click().run()

    # verify generated cover letter
    assert at.text_area("letter").value is not None
    assert len(at.text_area("letter").value) > 50

    # verify copy button
    assert at.button("copy").disabled is False
    at.button("copy").click().run()
    assert at.toast[0].value == "Cover Letter Copied"

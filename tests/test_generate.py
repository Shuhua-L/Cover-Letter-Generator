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

    # submit without job title, description
    assert at.text_input("title").value == ""
    assert at.text_area("description").value == ""
    submit_button.click().run()
    assert len(at.toast) == 1
    assert at.toast[0].value == ":red[Please enter job title]"

    # submit with title, but no description
    at.text_input("title").input(job["title"]).run()
    assert at.text_area("description").value == ""
    submit_button.click().run()
    assert len(at.toast) == 1
    assert at.toast[0].value == ":red[Please enter job description]"

    # submit with description, but no title
    at.text_input("title").input("").run()
    assert at.text_input("title").value == ""
    at.text_area("description").input(job["description"]).run()
    submit_button.click().run()
    assert len(at.toast) == 1
    assert at.toast[0].value == ":red[Please enter job title]"

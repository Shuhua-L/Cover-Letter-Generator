from streamlit.testing.v1 import AppTest
import os


def test_smoke():
    """Basic smoke test"""
    at = AppTest.from_file("app.py", default_timeout=10).run()
    assert not at.exception


def test_no_api_key():
    """If no API key is provided, a warning is displayed and the submit button is disabled"""
    at = AppTest.from_file("app.py", default_timeout=10)
    at.secrets["OPENAI_API_KEY"] = None
    at.run()
    assert len(at.warning) == 1
    assert at.warning[0].value == "Please enter your credentials!"
    assert at.button("submit").disabled is True


def test_invalid_input_api_key():
    """If input key is invalid, an error is displayed and the submit button is disabled"""
    at = AppTest.from_file("app.py", default_timeout=10)
    at.secrets["OPENAI_API_KEY"] = None
    at.run()

    at.text_input("OPENAI_API_KEY").input("this_is_not_a_valid_api_key").run()
    assert len(at.error) == 1
    assert at.error[0].value == "Invalid OpenAI API key."
    assert at.button("submit").disabled is True


def test_invalid_secret_api_key():
    """If API key is provided in environment, the submit button is enabled"""
    try:
        key = os.environ["OPENAI_API_KEY"]
        at = AppTest.from_file("app.py", default_timeout=10)
        at.secrets["OPENAI_API_KEY"] = key
        at.run()
        assert len(at.success) == 2
        assert at.success[0].value == "API key already provided!"
        assert at.success[1].value == "Proceed to entering your prompt message!"
        assert at.button("submit").disabled is False
    except KeyError:
        pass

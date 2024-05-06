from streamlit.testing.v1 import AppTest


def test_smoke():
    """Basic smoke test"""
    at = AppTest.from_file("app.py", default_timeout=10).run()
    assert not at.exception


def test_no_api_key():
    """If no API key is provided, a warning is displayed and the button is disabled"""
    at = AppTest.from_file("app.py", default_timeout=10).run()
    at.secrets["OPENAI_API_KEY"] = None
    assert len(at.warning) == 1
    assert at.warning[0].value == "Please enter your credentials!"
    assert at.button("generate").disabled is True


def test_invalid_input_api_key():
    """If input key is invalid, an error is displayed and the button is disabled"""
    at = AppTest.from_file("app.py", default_timeout=10).run()
    at.text_input("OPENAI_API_KEY").input("this_is_not_a_valid_api_key").run()
    assert len(at.error) == 1
    assert at.error[0].value == "Invalid OpenAI API key."
    assert at.button("generate").disabled is True

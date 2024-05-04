"""OpenAI API connector."""

import openai
import streamlit as st
import os

def check_openai_api_key(key):
    """Check if OpenAI API key is valid"""
    client = openai.OpenAI(api_key=key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True

# Instantiate OpenAI with credentials from streamlit secrets
# openai_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
# openai_key = os.getenv("OPENAI_API_KEY")
# client = openai.OpenAI(api_key=openai_key)

class Openai:
    """OpenAI Connector."""
    def __init__(self):
        openai_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=openai_key)

    def moderate(self, prompt: str) -> bool:
        """Call OpenAI GPT Moderation to check whether text is potentially harmful
        Args:
            prompt: text prompt
        Return: boolean if flagged
        """
        try:
            response = self.client.moderations.create(input=prompt)
            return response.results[0].flagged

        except Exception as e:
            st.session_state.text_error = f"OpenAI API error: {e}"

    def complete(
        self,
        prompt: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.9,
        max_tokens: int = 500,
    ) -> str:
        """Call OpenAI GPT Completion with text prompt.
        Args:
            prompt: text prompt
            model: OpenAI model name, e.g. "gpt-3.5-turbo"
            temperature: float between 0 and 1
            max_tokens: int between 1 and 2048
        Return: predicted response text
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                # max_tokens=max_tokens,
            )
            return response.choices[0].message.content

        except Exception as e:
            st.session_state.text_error = f"OpenAI API error: {e}"
            return ''

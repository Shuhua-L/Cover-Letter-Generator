"""OpenAI API connector."""

import openai
import streamlit as st

# Instantiate OpenAI with credentials from streamlit secrets
openai_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=openai_key)

class Openai:
    """OpenAI Connector."""

    @staticmethod
    def moderate(prompt: str) -> bool:
        """Call OpenAI GPT Moderation to check whether text is potentially harmful
        Args:
            prompt: text prompt
        Return: boolean if flagged
        """
        try:
            response = client.moderations.create(input=prompt)
            return response.results[0].flagged

        except Exception as e:
            st.session_state.text_error = f"OpenAI API error: {e}"

    @staticmethod
    def complete(
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
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                # max_tokens=max_tokens,
            )
            return response.choices[0].message.content

        except Exception as e:
            st.session_state.text_error = f"OpenAI API error: {e}"
            return ''

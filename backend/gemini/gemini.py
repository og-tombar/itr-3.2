"""
This module contains the Gemini class, which is used to query the Gemini API.
"""

import asyncio
import os
import time
from pathlib import Path
from string import Template

from google import genai
from google.genai.errors import ClientError, ServerError


class Gemini:
    """
    A class for querying the Gemini API.
    """

    CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    MODEL = "gemini-2.5-flash-preview-04-17"
    CALL_FRIEND_TPL_PATH = Path(__file__).parent / "call_friend.txt"

    @staticmethod
    def query(prompt: str) -> str:
        """Query the Gemini API with a prompt.

        Args:
            prompt (str): The prompt to query the Gemini API with.

        Returns:
            str: The response from the Gemini API.
        """
        retries = 30
        for i in range(retries):
            try:
                response = Gemini.CLIENT.models.generate_content(
                    model=Gemini.MODEL,
                    contents=[prompt],
                    config={"response_mime_type": "text/plain"}
                )
                break
            except ServerError as e:
                msg = f"Server error: {str(e)}"
                remaining = retries - i - 1
                if remaining > 0:
                    msg += f" {remaining} retries left."
                print(msg)
            except ClientError as e:
                msg = f"Client error: {str(e)}"
                remaining = retries - i - 1
                if remaining > 0:
                    msg += f" {remaining} retries left."
                print(msg)
                print("Waiting 60 seconds before retrying...")
                time.sleep(60)
        return response.text

    @staticmethod
    async def query_async(prompt: str) -> str:
        """Queries the Gemini API with a prompt in a background task.

        Args:
            prompt (str): The prompt to query the Gemini API with.

        Returns:
            str: The response from the Gemini API.
        """
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, Gemini.query, prompt)
        return response

    @staticmethod
    def call_friend_prompt(question: str, options: list[str]) -> str:
        """Generates a prompt for calling a friend for help.

        Args:
            question (str): The question to call a friend for.
            options (list[str]): The options for the question.

        Returns:
            str: The prompt for calling a friend for help.
        """
        tpl = Template(Gemini.CALL_FRIEND_TPL_PATH.read_text())
        return tpl.substitute(question=question, options=options)

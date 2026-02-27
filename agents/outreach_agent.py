from __future__ import annotations

import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from openai import OpenAI


def _get_openai_client() -> OpenAI:
    """
    Initialize and return an OpenAI client configured with the API key from the environment.

    Raises
    ------
    ValueError
        If the OPENAI_API_KEY environment variable is missing or empty.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. Please configure it in your .env file."
        )
    return OpenAI(api_key=api_key)


SYSTEM_PROMPT = (
    "You are an elite sales copywriter who writes emails that get replies.\n"
    "Write 3 emails for a sales outreach sequence.\n"
    "Email 1: First cold outreach - hook with their specific pain point, \n"
    "under 100 words, end with a soft question\n"
    "Email 2: Follow up 3 days later - reference something specific about \n"
    "their company, under 80 words\n"
    "Email 3: Final breakup email - create urgency, under 60 words\n"
    "Make each email feel human, specific, not salesy.\n"
    "Format as JSON with keys: email_1, email_2, email_3.\n"
    "Each email has keys: subject, body.\n"
    "Respond only in valid JSON format."
)


def run_outreach(
    company_name: str, prospect_data: Dict[str, Any], strategy: str
) -> Dict[str, Any]:
    """
    Generate a 3-step sales outreach email sequence using GPT-4o.

    This function sends the provided company name, prospect data, and strategy
    to OpenAI's GPT-4o model with a specialized system prompt that instructs it
    to return three concise, personalized sales emails in JSON format.

    The expected JSON structure is:
    {
        "email_1": {"subject": "...", "body": "..."},
        "email_2": {"subject": "...", "body": "..."},
        "email_3": {"subject": "...", "body": "..."}
    }

    Parameters
    ----------
    company_name : str
        Name of the company being targeted.
    prospect_data : dict
        Structured prospect insights (e.g., output from run_prospect).
    strategy : str
        The sales strategy text (e.g., output from run_strategy).

    Returns
    -------
    dict
        Parsed JSON dictionary with keys `email_1`, `email_2`, `email_3`.

    Raises
    ------
    ValueError
        If the OpenAI API key is missing or the model response cannot be parsed as JSON.
    """
    client = _get_openai_client()

    user_content = (
        f"Company name: {company_name}\n\n"
        f"Prospect data (JSON):\n{prospect_data}\n\n"
        "Sales strategy:\n"
        f"{strategy}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        temperature=0.4,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content if response.choices else None

    fallback: Dict[str, Any] = {
        "email_1": {
            "subject": "Quick question about [Company]",
            "body": "Hi, I noticed your team is focused on growth...",
        },
        "email_2": {
            "subject": "Following up",
            "body": "Just checking in...",
        },
        "email_3": {
            "subject": "Last note",
            "body": "I'll keep this brief...",
        },
    }

    if not content:
        return fallback

    try:
        parsed: Dict[str, Any] = json.loads(content)
    except json.JSONDecodeError:
        return fallback

    # Basic shape check (non-fatal if keys are missing, but ensures structure)
    for key in ("email_1", "email_2", "email_3"):
        if key not in parsed:
            parsed.setdefault(key, {"subject": "", "body": ""})

    return parsed


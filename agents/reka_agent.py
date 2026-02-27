from __future__ import annotations

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
    "You are a world class sales strategist. Given a company profile and prospect data,\n"
    "create a personalized sales strategy including:\n"
    "1. The perfect hook for this company\n"
    "2. Key value propositions to lead with\n"
    "3. Objections they will likely raise and how to handle them\n"
    "4. The ideal meeting agenda for a first call\n"
    "Be specific, sharp, and actionable."
)


def _build_user_message(
    company_name: str, prospect_data: Dict[str, Any], research_context: str
) -> str:
    """
    Build the user message content combining company, prospect, and research data.
    """
    return (
        f"Company name: {company_name}\n\n"
        f"Prospect data (JSON):\n{prospect_data}\n\n"
        "Research context:\n"
        f"{research_context}"
    )


def run_strategy(
    company_name: str, prospect_data: Dict[str, Any], research_context: str
) -> str:
    """
    Generate a personalized sales strategy using OpenAI GPT-4o.

    The strategy includes:
      1. The perfect hook for the company.
      2. Key value propositions to lead with.
      3. Likely objections and how to handle them.
      4. An ideal first-call meeting agenda.

    Parameters
    ----------
    company_name : str
        Name of the target company.
    prospect_data : dict
        Structured prospect insights (e.g., output from run_prospect).
    research_context : str
        Research text about the company (e.g., output from run_research).

    Returns
    -------
    str
        The generated sales strategy as a string.

    Raises
    ------
    ValueError
        If the OpenAI API key is missing or the model call fails.
    """
    user_message = _build_user_message(company_name, prospect_data, research_context)

    # Use OpenAI GPT-4o with the same strategy prompt (simpler + safer for hackathons)
    client = _get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content if response.choices else None
    if not content:
        raise ValueError("Failed to generate a sales strategy using OpenAI.")

    return content


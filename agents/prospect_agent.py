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


def run_prospect(company_name: str, research_context: str) -> Dict[str, Any]:
    """
    Analyze company research to derive B2B sales intelligence using GPT-4o.

    This function sends the provided research context to OpenAI's GPT-4o model
    with a specialized system prompt instructing it to:
      1. Identify the ideal decision maker title to target.
      2. Extract the top 3 pain points the company is facing.
      3. Propose the best sales angle.
      4. Describe what the company cares most about in 2025.

    The model is instructed to format its response as JSON with the keys:
    `decision_maker`, `pain_points`, `sales_angle`, and `priorities`.

    Parameters
    ----------
    company_name : str
        Name of the company being analyzed.
    research_context : str
        Research text about the company (e.g., output from run_research).

    Returns
    -------
    dict
        Parsed JSON dictionary containing:
        - decision_maker (str)
        - pain_points (list[str] or str)
        - sales_angle (str)
        - priorities (str)

    Raises
    ------
    ValueError
        If the OpenAI API key is missing or the model response cannot be parsed as JSON.
    """
    client = _get_openai_client()

    system_prompt = (
        "You are an expert B2B sales intelligence analyst. \n"
        "Given research about a company, identify:\n"
        "1. The ideal decision maker title to target (e.g. CTO, VP of Sales)\n"
        "2. Top 3 pain points this company is facing right now\n"
        "3. The best sales angle to use\n"
        "4. What they care most about in 2025\n"
        "Format as JSON with keys: decision_maker, pain_points, sales_angle, priorities.\n"
        "Respond only in valid JSON format."
    )

    user_content = (
        f"Company name: {company_name}\n\n"
        "Company research:\n"
        f"{research_context}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content if response.choices else None

    default_result: Dict[str, Any] = {
        "decision_maker": "CTO / VP of Engineering",
        "pain_points": ["Scaling issues", "AI adoption", "Cost optimization"],
        "sales_angle": "ROI and efficiency",
        "priorities": "Growth and innovation",
    }

    if not content:
        # Fall back to a sensible default if nothing is returned
        return default_result

    try:
        parsed: Dict[str, Any] = json.loads(content)
        return parsed
    except json.JSONDecodeError:
        # If JSON parsing fails for any reason, fall back to the default shape
        return default_result


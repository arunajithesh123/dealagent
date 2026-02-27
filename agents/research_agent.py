from __future__ import annotations

from typing import Any, Dict, List, Tuple

from dotenv import load_dotenv
import os

from tavily import TavilyClient


def _get_tavily_client() -> TavilyClient:
    """
    Initialize and return a TavilyClient configured with the API key from the environment.

    Raises
    ------
    ValueError
        If the TAVILY_API_KEY environment variable is missing or empty.
    """
    load_dotenv()
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is not set. Please configure it in your .env file."
        )
    return TavilyClient(api_key=api_key)


def run_research(company_name: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Run a set of Tavily searches to gather research about a company.

    This function performs three advanced-depth searches to collect:
    - Company overview and recent news
    - Challenges, problems, and pain points
    - Decision makers and leadership team

    The results are combined into a single formatted context string with
    sections: COMPANY OVERVIEW, CHALLENGES, and LEADERSHIP.

    Parameters
    ----------
    company_name : str
        Name of the company to research.

    Returns
    -------
    tuple
        A tuple of:
        - formatted_context (str): Combined human-readable summary string.
        - raw_results_list (list[dict]): List of raw Tavily responses for each query.

    Raises
    ------
    ValueError
        If the Tavily API key is missing.
    """
    client = _get_tavily_client()

    queries = [
        f"{company_name} company overview recent news 2025",
        f"{company_name} challenges problems pain points",
        f"{company_name} decision makers leadership team",
    ]

    raw_results: List[Dict[str, Any]] = []

    for query in queries:
        result = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
        )
        raw_results.append(result)

    overview_section = []
    challenges_section = []
    leadership_section = []

    if raw_results:
        overview = raw_results[0]
        if isinstance(overview, dict):
            overview_section.append("Company overview and recent news:")
            for item in overview.get("results", []):
                snippet = item.get("content") or item.get("snippet") or ""
                if snippet:
                    overview_section.append(f"- {snippet}")

    if len(raw_results) > 1:
        challenges = raw_results[1]
        if isinstance(challenges, dict):
            challenges_section.append("Key challenges, problems, and pain points:")
            for item in challenges.get("results", []):
                snippet = item.get("content") or item.get("snippet") or ""
                if snippet:
                    challenges_section.append(f"- {snippet}")

    if len(raw_results) > 2:
        leadership = raw_results[2]
        if isinstance(leadership, dict):
            leadership_section.append("Decision makers and leadership team:")
            for item in leadership.get("results", []):
                snippet = item.get("content") or item.get("snippet") or ""
                if snippet:
                    leadership_section.append(f"- {snippet}")

    formatted_parts: List[str] = []

    formatted_parts.append("COMPANY OVERVIEW")
    formatted_parts.append("-" * len("COMPANY OVERVIEW"))
    formatted_parts.append("\n".join(overview_section) if overview_section else "No overview data available.")
    formatted_parts.append("")

    formatted_parts.append("CHALLENGES")
    formatted_parts.append("-" * len("CHALLENGES"))
    formatted_parts.append("\n".join(challenges_section) if challenges_section else "No challenges data available.")
    formatted_parts.append("")

    formatted_parts.append("LEADERSHIP")
    formatted_parts.append("-" * len("LEADERSHIP"))
    formatted_parts.append("\n".join(leadership_section) if leadership_section else "No leadership data available.")

    formatted_context = "\n".join(formatted_parts)

    return formatted_context, raw_results


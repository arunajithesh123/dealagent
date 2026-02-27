from __future__ import annotations

import os
from datetime import datetime
from typing import Any, List, Optional, Tuple

import requests
from dotenv import load_dotenv


def _get_airbyte_credentials() -> Optional[Tuple[str, str]]:
    """
    Load and return the Airbyte OAuth2 client credentials from the environment.

    Returns
    -------
    tuple[str, str] | None
        (client_id, client_secret) if both are present, otherwise ``None``.
    """
    load_dotenv()
    client_id = os.getenv("AIRBYTE_CLIENT_ID")
    client_secret = os.getenv("AIRBYTE_CLIENT_SECRET")
    if not client_id or not client_secret:
        return None
    return client_id, client_secret


def _get_airbyte_access_token() -> Optional[str]:
    """
    Retrieve an OAuth2 access token for the Airbyte Cloud API.

    Returns
    -------
    str | None
        The access token if the call succeeds, otherwise ``None``.
    """
    creds = _get_airbyte_credentials()
    if creds is None:
        print("AIRBYTE_CLIENT_ID or AIRBYTE_CLIENT_SECRET is not set. Skipping Airbyte sync.")
        return None

    client_id, client_secret = creds
    token_url = "https://api.airbyte.com/v1/applications/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    try:
        resp = requests.post(token_url, json=payload, timeout=10)
        if not resp.ok:
            print(f"Airbyte token request failed with status {resp.status_code}.")
            return None
        data = resp.json()
        return data.get("access_token")
    except Exception:
        return None


def sync_to_airbyte(company_name: str, research_data: Any, emails: List[Any]) -> bool:
    """
    Send deal research data to the Airbyte API.

    This function logs a snapshot of the research and outreach context
    by posting a JSON payload to the Airbyte API.

    Parameters
    ----------
    company_name : str
        Name of the company the research is about.
    research_data : Any
        Research summary or structured research data. Will be coerced to string.
    emails : list
        Collection of email data (e.g., outreach sequence). Used to count emails.

    Returns
    -------
    bool
        ``True`` if the request was successful (HTTP 2xx), ``False`` otherwise.
        If credentials are not set or any request fails, this function returns
        ``False`` and only prints a warning without raising an exception.
    """
    access_token = _get_airbyte_access_token()
    if not access_token:
        # Fail silently if we can't obtain a token
        return False

    url = "https://api.airbyte.com/v1/connections"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "company_name": company_name,
        "research_summary": str(research_data),
        "timestamp": datetime.utcnow().isoformat(),
        "email_count": len(emails) if emails is not None else 0,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.ok
    except Exception:
        return False


def get_sync_status() -> str:
    """
    Report whether Airbyte sync is configured.

    Returns
    -------
    str
        ``"Airbyte sync active"`` if client credentials are configured,
        otherwise ``"Airbyte not connected"``.
    """
    creds = _get_airbyte_credentials()
    if creds is not None:
        return "Airbyte sync active"
    return "Airbyte not connected"


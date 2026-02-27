from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from neo4j import GraphDatabase, Driver


def _get_neo4j_driver() -> Optional[Driver]:
    """
    Initialize and return a Neo4j driver using environment configuration.

    Returns
    -------
    neo4j.Driver | None
        A Neo4j driver instance if configuration is present, otherwise ``None``.
    """
    load_dotenv()
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    if not uri or not user or not password:
        return None

    try:
        return GraphDatabase.driver(uri, auth=(user, password))
    except Exception:
        return None


def save_to_graph(
    company_name: str,
    prospect_data: Dict[str, Any],
    strategy: str,
    sources: List[Dict[str, Any]],
) -> bool:
    """
    Persist company, pain points, and sources into the Neo4j graph.

    This function creates:
    - A `Company` node with properties:
      - name
      - timestamp
      - sales_angle
      - decision_maker
      - strategy (full strategy text)
    - A `PainPoint` node for each pain point in `prospect_data["pain_points"]`.
    - A `Source` node for each source in ``sources`` with properties:
      - title
      - url
    And relationships:
      (Company)-[:HAS_PAIN_POINT]->(PainPoint)
      (Company)-[:HAS_SOURCE]->(Source)

    Parameters
    ----------
    company_name : str
        Name of the company.
    prospect_data : dict
        Prospect analysis data, expected to include keys like
        `decision_maker`, `sales_angle`, and `pain_points`.
    strategy : str
        Generated sales strategy text.
    sources : list[dict]
        List of source dictionaries, each ideally containing `title` and `url`.

    Returns
    -------
    bool
        ``True`` if the data was saved successfully, ``False`` otherwise.
        Fails silently (returns ``False``) if Neo4j is not connected.
    """
    driver = _get_neo4j_driver()
    if driver is None:
        return False

    pain_points = prospect_data.get("pain_points") or []
    if isinstance(pain_points, str):
        pain_points = [pain_points]

    decision_maker = prospect_data.get("decision_maker", "")
    sales_angle = prospect_data.get("sales_angle", "")

    try:
        with driver.session() as session:
            session.execute_write(
                _save_company_tx,
                company_name=company_name,
                decision_maker=decision_maker,
                sales_angle=sales_angle,
                strategy=strategy,
                pain_points=pain_points,
                sources=sources,
            )
        return True
    except Exception:
        return False
    finally:
        try:
            driver.close()
        except Exception:
            pass


def _save_company_tx(
    tx,
    company_name: str,
    decision_maker: str,
    sales_angle: str,
    strategy: str,
    pain_points: List[str],
    sources: List[Dict[str, Any]],
) -> None:
    """
    Transactional helper to create nodes and relationships for a company.
    """
    timestamp = datetime.utcnow().isoformat()

    query = """
    MERGE (c:Company {name: $company_name})
    SET c.timestamp = $timestamp,
        c.sales_angle = $sales_angle,
        c.decision_maker = $decision_maker,
        c.strategy = $strategy

    WITH c
    UNWIND $pain_points AS pp
      MERGE (p:PainPoint {description: pp})
      MERGE (c)-[:HAS_PAIN_POINT]->(p)

    WITH c
    UNWIND $sources AS src
      MERGE (s:Source {url: src.url})
      SET s.title = src.title
      MERGE (c)-[:HAS_SOURCE]->(s)
    """

    # Normalize sources to ensure keys exist
    norm_sources = [
        {
            "title": (src.get("title") or "").strip(),
            "url": (src.get("url") or "").strip(),
        }
        for src in sources
        if src.get("url")
    ]

    tx.run(
        query,
        company_name=company_name,
        timestamp=timestamp,
        sales_angle=sales_angle,
        decision_maker=decision_maker,
        strategy=strategy,
        pain_points=[pp for pp in pain_points if pp],
        sources=norm_sources,
    )


def get_company_graph() -> List[Dict[str, Any]]:
    """
    Retrieve all companies and their related pain points and sources from Neo4j.

    Returns
    -------
    list[dict]
        A list of dictionaries, each containing:
        - company: dict of company properties
        - pain_points: list of pain point descriptions
        - sources: list of dicts with `title` and `url`

        Returns an empty list if nothing is found or if Neo4j is unavailable.
    """
    driver = _get_neo4j_driver()
    if driver is None:
        return []

    query = """
    MATCH (c:Company)
    OPTIONAL MATCH (c)-[:HAS_PAIN_POINT]->(p:PainPoint)
    OPTIONAL MATCH (c)-[:HAS_SOURCE]->(s:Source)
    RETURN c, collect(DISTINCT p) AS pain_points, collect(DISTINCT s) AS sources
    """

    try:
        with driver.session() as session:
            records = session.run(query)
            results: List[Dict[str, Any]] = []
            for record in records:
                company_node = record["c"]
                pp_nodes = record["pain_points"] or []
                src_nodes = record["sources"] or []

                company = {
                    "name": company_node.get("name"),
                    "timestamp": company_node.get("timestamp"),
                    "sales_angle": company_node.get("sales_angle"),
                    "decision_maker": company_node.get("decision_maker"),
                }

                pain_points = [
                    pp.get("description")
                    for pp in pp_nodes
                    if pp is not None and pp.get("description")
                ]

                sources = [
                    {
                        "title": src.get("title"),
                        "url": src.get("url"),
                    }
                    for src in src_nodes
                    if src is not None and src.get("url")
                ]

                results.append(
                    {
                        "company": company,
                        "pain_points": pain_points,
                        "sources": sources,
                    }
                )
        return results
    except Exception:
        return []
    finally:
        try:
            driver.close()
        except Exception:
            pass


def get_related_companies(company_name: str) -> List[str]:
    """
    Find companies that share similar pain points with the given company.

    Parameters
    ----------
    company_name : str
        Name of the reference company.

    Returns
    -------
    list[str]
        List of related company names that share at least one pain point
        with the specified company. Returns an empty list if no matches
        are found or if Neo4j is unavailable.
    """
    driver = _get_neo4j_driver()
    if driver is None:
        return []

    query = """
    MATCH (c:Company {name: $company_name})-[:HAS_PAIN_POINT]->(p:PainPoint)
    MATCH (other:Company)-[:HAS_PAIN_POINT]->(p)
    WHERE other.name <> $company_name
    RETURN DISTINCT other.name AS name
    """

    try:
        with driver.session() as session:
            records = session.run(query, company_name=company_name)
            return [record["name"] for record in records if record.get("name")]
    except Exception:
        return []
    finally:
        try:
            driver.close()
        except Exception:
            pass


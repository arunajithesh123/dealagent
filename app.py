from __future__ import annotations

import math
from typing import Any, Dict, List

from dotenv import load_dotenv

import streamlit as st
import plotly.graph_objects as go

from utils.styles import get_styles
from utils.airbyte_sync import get_sync_status, sync_to_airbyte
from agents.research_agent import run_research
from agents.prospect_agent import run_prospect
from agents.reka_agent import run_strategy
from agents.outreach_agent import run_outreach
from agents.graph_agent import (
    get_company_graph,
    get_related_companies,
    save_to_graph,
)


load_dotenv()

if "dealagent_running" not in st.session_state:
    st.session_state["dealagent_running"] = False
if "dealagent_last_company" not in st.session_state:
    st.session_state["dealagent_last_company"] = ""
if "graph_data" not in st.session_state:
    # Initialize with current graph snapshot if available
    try:
        st.session_state["graph_data"] = get_company_graph()
    except Exception:
        st.session_state["graph_data"] = []
if "results" not in st.session_state:
    st.session_state["results"] = {}
if "has_results" not in st.session_state:
    st.session_state["has_results"] = False

st.set_page_config(
    page_title="DealAgent — AI Sales Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_styles(), unsafe_allow_html=True)


def _render_error(message: str) -> None:
    """Render a styled error message."""
    st.error(f"❌ {message}")


def _render_agent_steps(statuses: List[Dict[str, str]], container) -> None:
    """Render the agent pipeline status using the custom CSS classes."""
    html_parts = []
    for step in statuses:
        state = step["state"]
        classes = ["agent-step"]
        if state == "active":
            classes.append("active")
        elif state == "done":
            classes.append("complete")

        icon = step["icon"]
        title = step["title"]
        subtitle = step["subtitle"]
        status_label = {
            "pending": "Pending",
            "active": "Running...",
            "done": "Completed",
            "error": "Error",
        }[state]

        html_parts.append(
            f"""
            <div class="{' '.join(classes)}">
              <div class="agent-step-icon">{icon}</div>
              <div class="agent-step-main">
                <div class="agent-step-title">{title}</div>
                <div class="agent-step-subtitle">{subtitle}</div>
                <div class="agent-step-status">{status_label}</div>
              </div>
            </div>
            """
        )

    container.markdown("\n".join(html_parts), unsafe_allow_html=True)


def _build_sources_from_research(raw_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Extract simple source objects from Tavily raw results."""
    sources: List[Dict[str, str]] = []
    for block in raw_results or []:
        for item in block.get("results", []):
            title = item.get("title") or "Source"
            url = item.get("url") or ""
            if url:
                sources.append({"title": title, "url": url})
    return sources


def _build_graph_figure(graph_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Build a simple network graph visualization from Neo4j data.

    Nodes:
        - Company: purple
        - PainPoints: red
        - Sources: blue
    """
    if not graph_data:
        fig = go.Figure()
        fig.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            plot_bgcolor="#050509",
            paper_bgcolor="#050509",
            title="No graph data available yet.",
        )
        return fig

    nodes: Dict[str, Dict[str, Any]] = {}
    edges: List[tuple[str, str]] = []

    # Build nodes and edges
    for entry in graph_data:
        company = entry.get("company") or {}
        cname = company.get("name")
        if not cname:
            continue
        company_id = f"company::{cname}"
        nodes[company_id] = {"label": cname, "type": "company"}

        for pp in entry.get("pain_points") or []:
            pid = f"pp::{pp}"
            nodes.setdefault(pid, {"label": pp, "type": "painpoint"})
            edges.append((company_id, pid))

        for src in entry.get("sources") or []:
            url = src.get("url")
            if not url:
                continue
            label = src.get("title") or url
            sid = f"src::{url}"
            nodes.setdefault(sid, {"label": label, "type": "source"})
            edges.append((company_id, sid))

    # Simple radial layout
    node_ids = list(nodes.keys())
    n = len(node_ids)
    xs, ys, texts, colors = [], [], [], []

    for idx, node_id in enumerate(node_ids):
        node = nodes[node_id]
        node_type = node["type"]

        angle = 2 * math.pi * idx / max(n, 1)
        radius = {
            "company": 2.0,
            "painpoint": 3.2,
            "source": 4.0,
        }.get(node_type, 3.0)

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        xs.append(x)
        ys.append(y)
        texts.append(node["label"])
        color = {
            "company": "#8b5cf6",
            "painpoint": "#f97373",
            "source": "#3b82f6",
        }.get(node_type, "#e5e7eb")
        colors.append(color)

        node["pos"] = (x, y)

    edge_x, edge_y = [], []
    for src_id, dst_id in edges:
        src_node = nodes.get(src_id)
        dst_node = nodes.get(dst_id)
        if not src_node or not dst_node:
            continue
        x0, y0 = src_node["pos"]
        x1, y1 = dst_node["pos"]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color="#4b5563"),
        hoverinfo="none",
        mode="lines",
    )

    node_trace = go.Scatter(
        x=xs,
        y=ys,
        mode="markers+text",
        text=texts,
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            showscale=False,
            color=colors,
            size=14,
            line=dict(width=1, color="#0f172a"),
        ),
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=20, r=20, t=40),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        plot_bgcolor="#050509",
        paper_bgcolor="#050509",
        title="Neo4j Knowledge Graph",
        font=dict(color="#e2e8f0"),
    )
    return fig


def _render_sidebar() -> None:
    """Render the sidebar with logo, knowledge graph summary, and footer."""
    with st.sidebar:
        st.markdown(
            "<h2 style='margin-bottom:0'>🤖 DealAgent</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color:#9ca3af;margin-top:4px;'>Powered by Tavily · Neo4j · Reka · Airbyte · OpenAI</p>",
            unsafe_allow_html=True,
        )
        st.divider()

        st.markdown("### 🗄️ Knowledge Graph")
        graph_data: List[Dict[str, Any]] = st.session_state.get("graph_data", [])

        total_companies = len(graph_data)
        st.metric("Companies Researched", value=total_companies)

        for entry in graph_data:
            company = entry.get("company") or {}
            cname = company.get("name") or "Unknown company"
            pain_points = entry.get("pain_points") or []
            sources = entry.get("sources") or []

            with st.expander(cname, expanded=False):
                if pain_points:
                    st.markdown("**Pain Points**")
                    for pp in pain_points:
                        st.markdown(f"- {pp}")

                if sources:
                    st.markdown("**Sources**")
                    for src in sources:
                        label = src.get("title") or src.get("url") or "Source"
                        url = src.get("url")
                        if url:
                            st.markdown(f"- [{label}]({url})")

                try:
                    related = get_related_companies(cname)
                except Exception:
                    related = []

                if related:
                    st.markdown("**Related Companies**")
                    st.markdown(", ".join(related))

        st.divider()
        st.caption(f"Sync status: {get_sync_status()}")
        st.markdown(
            "<p style='font-size:11px;color:#6b7280;margin-top:8px;'>Built with ❤️ at AWS Builder Loft</p>",
            unsafe_allow_html=True,
        )


def main() -> None:
    """Main entrypoint for the DealAgent Streamlit UI."""
    _render_sidebar()

    st.markdown(
        "<h1>Close More Deals with Autonomous AI Agents</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#9ca3af;font-size:16px;'>Enter any company name and watch 5 AI agents work together.</p>",
        unsafe_allow_html=True,
    )

    company_name = st.text_input(
        "Company Name",
        placeholder="e.g. Salesforce, Stripe, OpenAI...",
        label_visibility="collapsed",
    )

    run_button = st.button("🚀 Run DealAgent", type="primary")

    progress_container = st.container()
    st.markdown("---")

    if run_button:
        if not company_name.strip():
            _render_error("Please enter a company name before running DealAgent.")
            return

        if st.session_state.get("dealagent_running", False):
            _render_error("DealAgent is already running. Please wait for it to finish.")
            return

        st.session_state["dealagent_running"] = True
        st.session_state["dealagent_last_company"] = company_name.strip()

        # Agent pipeline states
        steps = [
            {
                "key": "research",
                "icon": "🔍",
                "title": "Research Agent (Tavily)",
                "subtitle": "Searching the web...",
                "state": "pending",
            },
            {
                "key": "prospect",
                "icon": "👤",
                "title": "Prospect Agent (OpenAI)",
                "subtitle": "Analyzing decision makers...",
                "state": "pending",
            },
            {
                "key": "strategy",
                "icon": "🧠",
                "title": "Strategy Agent (Reka AI)",
                "subtitle": "Building sales strategy...",
                "state": "pending",
            },
            {
                "key": "outreach",
                "icon": "✍️",
                "title": "Outreach Agent (OpenAI)",
                "subtitle": "Writing personalized emails...",
                "state": "pending",
            },
            {
                "key": "graph",
                "icon": "🗄️",
                "title": "Graph Agent (Neo4j)",
                "subtitle": "Saving to knowledge graph...",
                "state": "pending",
            },
            {
                "key": "airbyte",
                "icon": "🔌",
                "title": "Airbyte",
                "subtitle": "Syncing data pipeline...",
                "state": "pending",
            },
        ]

        def set_state(key: str, state: str) -> None:
            for s in steps:
                if s["key"] == key:
                    s["state"] = state
            _render_agent_steps(steps, progress_container)

        # Start pipeline
        _render_agent_steps(steps, progress_container)

        try:
            # Research Agent
            set_state("research", "active")
            with st.spinner("Running Research Agent..."):
                research_context, raw_results = run_research(company_name)
                sources = _build_sources_from_research(raw_results)
            set_state("research", "done")

            # Prospect Agent
            set_state("prospect", "active")
            with st.spinner("Running Prospect Agent..."):
                prospect_data = run_prospect(company_name, research_context)
            set_state("prospect", "done")

            # Strategy Agent
            set_state("strategy", "active")
            with st.spinner("Running Strategy Agent..."):
                strategy_text = run_strategy(company_name, prospect_data, research_context)
            set_state("strategy", "done")

            # Outreach Agent
            set_state("outreach", "active")
            with st.spinner("Running Outreach Agent..."):
                emails = run_outreach(company_name, prospect_data, strategy_text)
            set_state("outreach", "done")

            # Graph Agent (non-fatal)
            set_state("graph", "active")
            with st.spinner("Saving to Neo4j graph..."):
                try:
                    save_to_graph(
                        company_name=company_name,
                        prospect_data=prospect_data,
                        strategy=strategy_text,
                        sources=sources,
                    )
                except Exception:
                    pass
            set_state("graph", "done")

            # Airbyte Sync (non-fatal)
            set_state("airbyte", "active")
            with st.spinner("Syncing with Airbyte..."):
                try:
                    email_list = [
                        emails.get("email_1", {}),
                        emails.get("email_2", {}),
                        emails.get("email_3", {}),
                    ]
                    sync_to_airbyte(company_name, research_context, email_list)
                except Exception:
                    pass
            set_state("airbyte", "done")

            # Persist results in session state
            st.session_state["results"] = {
                "company": company_name.strip(),
                "research": research_context,
                "prospect": prospect_data,
                "strategy": strategy_text,
                "emails": emails,
                "sources": sources,
            }
            st.session_state["has_results"] = True

            # Refresh graph data in session state so sidebar count updates
            try:
                st.session_state["graph_data"] = get_company_graph()
            except Exception:
                st.session_state["graph_data"] = st.session_state.get("graph_data", [])

        except Exception as exc:  # catch-all to keep UI responsive
            for s in steps:
                if s["state"] == "active":
                    s["state"] = "error"
            _render_agent_steps(steps, progress_container)
            _render_error(f"Something went wrong while running DealAgent: {exc}")
            st.session_state["dealagent_running"] = False
            return

        st.session_state["dealagent_running"] = False

    # RESULTS TABS (persisted via session_state)
    if st.session_state.get("has_results", False):
        results = st.session_state.get("results", {})
        research_context = results.get("research", "")
        prospect_data = results.get("prospect", {}) or {}
        strategy_text = results.get("strategy", "") or ""
        emails = results.get("emails", {}) or {}
        sources = results.get("sources", []) or []

        tab1, tab2, tab3, tab4 = st.tabs(
            ["📊 Company Intel", "🧠 Sales Strategy", "📧 Email Sequence", "🗄️ Knowledge Graph"]
        )

        # Tab 1: Company Intel
        with tab1:
            st.markdown("#### Company Intelligence Overview")
            c1, c2, c3 = st.columns(3)

            decision_maker = prospect_data.get("decision_maker", "N/A")
            pain_points = prospect_data.get("pain_points") or []
            if isinstance(pain_points, str):
                pain_points = [pain_points]
            top_pain = pain_points[0] if pain_points else "N/A"
            sales_angle = prospect_data.get("sales_angle", "N/A")

            with c1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                      <div style="font-size:12px;text-transform:uppercase;color:#9ca3af;">Decision Maker</div>
                      <div style="font-size:22px;font-weight:600;margin-top:4px;">{decision_maker}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                      <div style="font-size:12px;text-transform:uppercase;color:#9ca3af;">Top Pain Point</div>
                      <div style="font-size:22px;font-weight:600;margin-top:4px;">{top_pain}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                      <div style="font-size:12px;text-transform:uppercase;color:#9ca3af;">Sales Angle</div>
                      <div style="font-size:22px;font-weight:600;margin-top:4px;">{sales_angle}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.expander("Full research summary"):
                st.markdown(research_context)

            if sources:
                st.markdown("###### Sources")
                tags = []
                for src in sources:
                    label = src.get("title") or src.get("url") or "Source"
                    url = src.get("url")
                    if url:
                        tags.append(
                            f'<a href="{url}" target="_blank" style="text-decoration:none;"><span class="source-tag">{label}</span></a>'
                        )
                st.markdown(" ".join(tags), unsafe_allow_html=True)

        # Tab 2: Sales Strategy
        with tab2:
            st.markdown("#### Reka AI Sales Strategy")
            st.markdown(
                f"""
                <div class="metric-card">
                  <div style="font-size:13px;text-transform:uppercase;color:#9ca3af;margin-bottom:8px;">
                    Strategy Summary
                  </div>
                  <div style="white-space:pre-wrap;font-size:14px;line-height:1.6;">
                  {strategy_text}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if pain_points:
                st.markdown("#### Key Pain Points")
                for pp in pain_points:
                    st.markdown(
                        f"""
                        <div class="email-card">
                          <div style="font-size:13px;text-transform:uppercase;color:#9ca3af;margin-bottom:4px;">
                            Pain Point
                          </div>
                          <div style="font-size:14px;">{pp}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # Tab 3: Email Sequence
        with tab3:
            st.markdown("#### 3-Step Email Sequence")
            cols = st.columns(3)
            email_order = [("email_1", "Email 1"), ("email_2", "Email 2"), ("email_3", "Email 3")]

            for col, (ekey, label) in zip(cols, email_order):
                with col:
                    email = emails.get(ekey, {}) or {}
                    subject = email.get("subject", "")
                    body = email.get("body", "")

                    st.markdown(
                        f"""
                        <div class="email-card">
                          <div style="font-size:11px;text-transform:uppercase;color:#9ca3af;margin-bottom:6px;">
                            {label}
                          </div>
                          <div style="font-size:14px;font-weight:600;margin-bottom:6px;">
                            {subject}
                          </div>
                          <div style="font-size:13px;white-space:pre-wrap;line-height:1.6;">
                            {body}
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if st.button(f"Copy {label}", key=f"copy_{ekey}"):
                        st.info("Copy the email content from the card above.")

        # Tab 4: Knowledge Graph
        with tab4:
            st.markdown("#### Neo4j Knowledge Graph")
            graph_for_tab = st.session_state.get("graph_data", [])
            fig = _build_graph_figure(graph_for_tab)
            st.plotly_chart(fig, use_container_width=True)

            company_for_related = results.get("company") or company_name
            try:
                related = get_related_companies(company_for_related)
            except Exception:
                related = []

            if related:
                st.markdown("#### Related Companies")
                st.markdown(", ".join(related))
            else:
                st.markdown(
                    "<p style='color:#6b7280;'>No related companies found yet for this company.</p>",
                    unsafe_allow_html=True,
                )


if __name__ == "__main__":
    main()


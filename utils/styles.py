from __future__ import annotations


def get_styles() -> str:
    """
    Return the global CSS string for the Streamlit app.

    The styles implement a dark, premium design with a focus on
    readable typography, subtle depth, and clear status indicators
    for the various agents and UI elements.

    The returned string is ready to be passed directly to
    ``st.markdown(get_styles(), unsafe_allow_html=True)``.
    """
    return """
<style>
/* Global layout */
.main {
    background-color: #0a0a0f;
    color: #e2e8f0;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
                 sans-serif;
}

/* Streamlit default text colors */
body, [class^="css"], .stMarkdown, .stText, .stTitle, .stHeader {
    color: #e2e8f0;
}

/* Metric / summary cards */
.metric-card {
    background: #13131a;
    border: 1px solid #2a2a3e;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 18px 35px rgba(0, 0, 0, 0.55);
    animation: fadeIn 0.4s ease-out;
}

/* Email cards */
.email-card {
    background: #13131a;
    border: 1px solid #2a2a3e;
    border-radius: 16px;
    padding: 20px;
    transition: transform 0.15s ease-out, box-shadow 0.15s ease-out,
                border-color 0.15s ease-out;
    animation: fadeIn 0.4s ease-out;
}

.email-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.65);
    border-color: #6366f1;
}

/* Agent step rows */
.agent-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    margin-bottom: 8px;
    border-radius: 12px;
    background: #111117;
    border-left: 3px solid #2a2a3e;
    border-right: 1px solid #2a2a3e;
    border-top: 1px solid #2a2a3e;
    border-bottom: 1px solid #2a2a3e;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.45);
}

.agent-step-icon {
    width: 28px;
    height: 28px;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 20%, #6366f1, #111827);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #e2e8f0;
    font-size: 16px;
}

.agent-step-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.agent-step-title {
    font-weight: 600;
    font-size: 15px;
}

.agent-step-subtitle {
    font-size: 12px;
    color: #9ca3af;
}

.agent-step-status {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9ca3af;
}

.agent-step.active {
    border-left: 3px solid #6366f1;
    box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.45),
                0 16px 38px rgba(15, 23, 42, 0.9);
    animation: pulse 1.4s ease-in-out infinite;
}

.agent-step.complete {
    border-left: 3px solid #22c55e;
    box-shadow: 0 0 0 1px rgba(34, 197, 94, 0.4),
                0 14px 32px rgba(15, 23, 42, 0.8);
}

/* Primary buttons */
.stButton > button {
    width: 100%;
    padding: 16px 18px;
    border-radius: 12px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    background-image: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #e2e8f0;
    font-size: 18px;
    font-weight: 600;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
                 sans-serif;
    cursor: pointer;
    box-shadow: 0 18px 40px rgba(37, 99, 235, 0.45);
    transition: transform 0.12s ease-out, box-shadow 0.12s ease-out,
                filter 0.12s ease-out, border-color 0.12s ease-out;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 22px 50px rgba(56, 189, 248, 0.45);
    filter: brightness(1.05);
    border-color: rgba(191, 219, 254, 0.9);
}

.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.8);
}

/* Source tags */
.source-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(99, 102, 241, 0.16);
    border: 1px solid rgba(99, 102, 241, 0.6);
    color: #c7d2fe;
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Graph nodes (Neo4j) */
.graph-node {
    display: inline-flex;
    align-items: center;
    padding: 6px 12px;
    border-radius: 999px;
    background: #111827;
    border: 1px solid #2a2a3e;
    color: #e2e8f0;
    font-size: 12px;
    gap: 6px;
}

.graph-node--company {
    border-color: #6366f1;
    box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.4);
}

.graph-node--painpoint {
    border-color: #f97316;
}

.graph-node--source {
    border-color: #22c55e;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #050509;
}

::-webkit-scrollbar-thumb {
    background: #1f2933;
    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: #374151;
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.58),
                    0 16px 38px rgba(15, 23, 42, 0.9);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(99, 102, 241, 0),
                    0 16px 38px rgba(15, 23, 42, 0.9);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(99, 102, 241, 0),
                    0 16px 38px rgba(15, 23, 42, 0.9);
    }
}
</style>
"""


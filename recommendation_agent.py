"""Recommendation Agent for operational interventions."""

from __future__ import annotations


def recommend_intervention(port: str, risk_score: float) -> str:
    """Return a basic intervention recommendation based on lane risk score."""
    if risk_score >= 70:
        return f"High risk at {port}: escalate lane review, prioritize container availability checks, and validate charge-code exposure."
    if risk_score >= 40:
        return f"Moderate risk at {port}: monitor dwell trends and review lanes with rising accessorial charges."
    return f"Low risk at {port}: continue monitoring CPC movement and cost mix."

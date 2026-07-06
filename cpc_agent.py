"""CPC Intelligence Agent.

This is a lightweight, deterministic agent stub. In production, this can be
wrapped with LangGraph and grounded LLM responses.
"""

from __future__ import annotations

import pandas as pd

COST_COLUMNS = [
    "base_freight",
    "fuel_surcharge",
    "detention_cost",
    "demurrage_cost",
    "storage_cost",
    "chassis_cost",
    "accessorial_cost",
]


class CPCAgent:
    """Analyze CPC movement and cost drivers."""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def summarize_port(self, destination_port: str) -> dict:
        port_df = self.data[self.data["destination_port"] == destination_port]
        if port_df.empty:
            return {"error": f"No records found for {destination_port}"}

        avg_cpc = port_df["total_transportation_cost"].mean()
        target = port_df["target_cpc"].mean()
        variance = avg_cpc - target
        driver_values = port_df[COST_COLUMNS].mean().sort_values(ascending=False)

        return {
            "destination_port": destination_port,
            "avg_cpc": round(avg_cpc, 2),
            "target_cpc": round(target, 2),
            "variance": round(variance, 2),
            "top_cost_drivers": driver_values.head(4).round(2).to_dict(),
        }

    def explain_cpc_escalation(self, destination_port: str) -> str:
        summary = self.summarize_port(destination_port)
        if "error" in summary:
            return summary["error"]
        drivers = ", ".join([f"{k}: ${v}" for k, v in summary["top_cost_drivers"].items()])
        return (
            f"For {destination_port}, average CPC is ${summary['avg_cpc']}, "
            f"against a target of ${summary['target_cpc']}. Variance is ${summary['variance']}. "
            f"Primary cost drivers are {drivers}."
        )

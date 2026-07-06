"""Root Cause Agent for CPC escalation explanation."""

from __future__ import annotations

import pandas as pd

COST_COLUMNS = [
    "fuel_surcharge",
    "detention_cost",
    "demurrage_cost",
    "storage_cost",
    "chassis_cost",
    "accessorial_cost",
]


class RootCauseAgent:
    """Generate simple root-cause narratives from cost components."""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def explain(self, destination_port: str) -> str:
        df = self.data[self.data["destination_port"] == destination_port]
        if df.empty:
            return f"No records found for {destination_port}."

        avg_cpc = df["total_transportation_cost"].mean()
        avg_target = df["target_cpc"].mean()
        variance_pct = ((avg_cpc - avg_target) / avg_target) * 100
        drivers = df[COST_COLUMNS].mean().sort_values(ascending=False).head(3)
        driver_text = "; ".join([f"{idx.replace('_', ' ')} (${val:.2f})" for idx, val in drivers.items()])

        return (
            f"CPC across {destination_port} is tracking {variance_pct:.1f}% versus target. "
            f"The top contributing charge codes are {driver_text}. "
            "Recommended next step: review high-dwell containers and lanes with repeated accessorial exposure."
        )

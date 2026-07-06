"""Lane Intelligence Agent for inbound ocean logistics."""

from __future__ import annotations

import pandas as pd


class LaneIntelligenceAgent:
    """Evaluate lane health, CPC risk, and operational intervention opportunities."""

    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()

    def lane_scorecard(self, destination_port: str) -> pd.DataFrame:
        df = self.data[self.data["destination_port"] == destination_port]
        if df.empty:
            return pd.DataFrame()

        grouped = (
            df.groupby("lane")
            .agg(
                containers=("container_id", "count"),
                avg_cpc=("total_transportation_cost", "mean"),
                target_cpc=("target_cpc", "mean"),
                avg_dwell=("port_dwell_days", "mean"),
                escalation_rate=("cpc_escalation_flag", "mean"),
                avg_detention=("detention_cost", "mean"),
                avg_demurrage=("demurrage_cost", "mean"),
            )
            .reset_index()
        )
        grouped["cpc_variance"] = grouped["avg_cpc"] - grouped["target_cpc"]
        grouped["risk_score"] = (
            grouped["escalation_rate"] * 50
            + grouped["avg_dwell"].clip(0, 10) * 3
            + (grouped["cpc_variance"].clip(lower=0) / 50)
        ).round(2)
        return grouped.sort_values("risk_score", ascending=False)

    def answer_lane_questions(self, destination_port: str, top_n: int = 5) -> dict:
        scorecard = self.lane_scorecard(destination_port)
        if scorecard.empty:
            return {"error": f"No lane records found for {destination_port}"}

        top_lanes = scorecard.head(top_n)
        return {
            "destination_port": destination_port,
            "questions_answered": [
                "Which lanes are driving CPC inflation?",
                "Which lanes are above target?",
                "Which lanes show elevated dwell or accessorial exposure?",
                "Which lanes should operations prioritize this week?",
            ],
            "top_risk_lanes": top_lanes[
                ["lane", "containers", "avg_cpc", "target_cpc", "cpc_variance", "avg_dwell", "risk_score"]
            ].round(2).to_dict(orient="records"),
        }

    def recommend_actions(self, destination_port: str) -> list[str]:
        scorecard = self.lane_scorecard(destination_port)
        if scorecard.empty:
            return [f"No lane records found for {destination_port}."]

        highest = scorecard.iloc[0]
        actions = [
            f"Prioritize review of lane {highest['lane']} because it has the highest risk score.",
            "Investigate charge-code mix for detention, demurrage, storage, and accessorial costs.",
            "Review containers with dwell time above the lane average.",
            "Compare carrier performance and cost variance before future booking allocation.",
        ]
        return actions

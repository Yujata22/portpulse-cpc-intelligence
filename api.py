"""FastAPI backend for LogisticsGPT CPC Intelligence prototype."""

from __future__ import annotations

from pathlib import Path
import sys
import pandas as pd
from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agents.cpc_agent import CPCAgent
from agents.lane_intelligence_agent import LaneIntelligenceAgent
from agents.root_cause_agent import RootCauseAgent

DATA_PATH = ROOT / "data" / "synthetic_cpc_data.csv"

app = FastAPI(title="LogisticsGPT CPC Intelligence API", version="0.1.0")


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError("Data file not found. Run src/generate_synthetic_data.py first.")
    return pd.read_csv(DATA_PATH)


@app.get("/")
def health_check() -> dict:
    return {"status": "ok", "service": "LogisticsGPT CPC Intelligence"}


@app.get("/port/{destination_port}")
def port_summary(destination_port: str) -> dict:
    data = load_data()
    agent = CPCAgent(data)
    return agent.summarize_port(destination_port.upper())


@app.get("/lane/{destination_port}")
def lane_intelligence(destination_port: str) -> dict:
    data = load_data()
    agent = LaneIntelligenceAgent(data)
    return agent.answer_lane_questions(destination_port.upper())


@app.get("/root-cause/{destination_port}")
def root_cause(destination_port: str) -> dict:
    data = load_data()
    agent = RootCauseAgent(data)
    return {"destination_port": destination_port.upper(), "analysis": agent.explain(destination_port.upper())}

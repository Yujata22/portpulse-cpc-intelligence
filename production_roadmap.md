# Production Roadmap

## Phase 1: Prototype

- Generate synthetic container-level data
- Train baseline CPC forecasting model
- Build deterministic agents
- Expose API endpoints

## Phase 2: Explainability

- Add SHAP attribution
- Add charge-code contribution visuals
- Add lane-level anomaly detection

## Phase 3: Agent Orchestration

- Convert deterministic agents into LangGraph workflows
- Add retrieval over business rules and charge-code documentation
- Add governed LLM summaries

## Phase 4: Production Integration

- Replace CSVs with Snowflake/PostgreSQL
- Add real-time milestone ingestion
- Add monitoring and model drift checks
- Add human-in-the-loop approval for operational recommendations

## Phase 5: Application Layer

- Build Next.js UI
- Add lane health scorecards
- Add proactive alerting
- Add analyst feedback capture

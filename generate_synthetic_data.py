"""Generate synthetic inbound ocean logistics CPC data.

This script creates container-level synthetic data for a CPC intelligence prototype.
It is generic and does not represent any proprietary operational dataset.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_ROWS = 2500
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "synthetic_cpc_data.csv"

US_PORTS = ["USLAX", "USLGB", "USOAK", "USSEA", "USNYC", "USSAV", "USNOR", "USHOU"]
ORIGIN_PORTS = ["CNSHA", "CNNGB", "CNYTN", "KRPUS", "JPTYO", "VNSGN", "INNSA", "DEHAM", "NLRTM"]
CARRIERS = ["Carrier_A", "Carrier_B", "Carrier_C", "Carrier_D"]
PROGRAMS = ["Retail", "FBA", "Vendor_Direct"]
LOAD_TYPES = ["FCL", "LCL"]


def generate_data(n_rows: int = N_ROWS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    origin = rng.choice(ORIGIN_PORTS, size=n_rows)
    destination = rng.choice(US_PORTS, size=n_rows, p=[0.18, 0.16, 0.09, 0.09, 0.16, 0.14, 0.08, 0.10])
    carrier = rng.choice(CARRIERS, size=n_rows)
    program = rng.choice(PROGRAMS, size=n_rows, p=[0.48, 0.42, 0.10])
    load_type = rng.choice(LOAD_TYPES, size=n_rows, p=[0.78, 0.22])

    # Event dates
    vessel_departure = pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 180, size=n_rows), unit="D")
    transit_days = rng.normal(25, 6, size=n_rows).clip(12, 50).round().astype(int)
    port_arrival = vessel_departure + pd.to_timedelta(transit_days, unit="D")

    port_dwell_days = rng.gamma(shape=2.2, scale=1.7, size=n_rows).clip(1, 18).round().astype(int)
    customs_release = port_arrival + pd.to_timedelta(rng.integers(1, 5, size=n_rows), unit="D")
    container_available = customs_release + pd.to_timedelta(rng.integers(0, 3, size=n_rows), unit="D")
    empty_return = container_available + pd.to_timedelta(port_dwell_days, unit="D")

    # Costs
    base_by_port = {"USLAX": 2300, "USLGB": 2250, "USOAK": 2450, "USSEA": 2400, "USNYC": 2700, "USSAV": 2550, "USNOR": 2500, "USHOU": 2600}
    base_freight = np.array([base_by_port[p] for p in destination]) + rng.normal(0, 180, size=n_rows)
    lcl_multiplier = np.where(load_type == "LCL", 1.22, 1.0)
    fuel_surcharge = base_freight * rng.uniform(0.10, 0.22, size=n_rows)

    congestion_factor = np.where(np.isin(destination, ["USLAX", "USLGB", "USNYC"]), 1.25, 1.0)
    detention_cost = np.where(port_dwell_days > 6, (port_dwell_days - 6) * rng.uniform(55, 110, size=n_rows), 0) * congestion_factor
    demurrage_cost = np.where(port_dwell_days > 5, (port_dwell_days - 5) * rng.uniform(70, 130, size=n_rows), 0) * congestion_factor
    storage_cost = np.where(port_dwell_days > 4, (port_dwell_days - 4) * rng.uniform(35, 80, size=n_rows), 0)
    chassis_cost = rng.uniform(80, 240, size=n_rows)
    accessorial_cost = rng.gamma(shape=2.0, scale=70, size=n_rows)

    total_cost = (
        base_freight * lcl_multiplier
        + fuel_surcharge
        + detention_cost
        + demurrage_cost
        + storage_cost
        + chassis_cost
        + accessorial_cost
    )

    target_cpc = np.array([base_by_port[p] * 1.45 for p in destination])
    cpc_variance = total_cost - target_cpc
    cpc_escalation_flag = (cpc_variance > 400).astype(int)

    df = pd.DataFrame(
        {
            "container_id": [f"CONT{i:07d}" for i in range(1, n_rows + 1)],
            "shipment_id": [f"SHP{i:07d}" for i in range(1, n_rows + 1)],
            "bol": [f"BOL{i:07d}" for i in rng.integers(1000000, 9999999, size=n_rows)],
            "origin_port": origin,
            "destination_port": destination,
            "lane": [f"{o}->{d}" for o, d in zip(origin, destination)],
            "carrier": carrier,
            "program": program,
            "load_type": load_type,
            "vessel_departure": vessel_departure,
            "port_arrival": port_arrival,
            "customs_release": customs_release,
            "container_available": container_available,
            "empty_return": empty_return,
            "transit_days": transit_days,
            "port_dwell_days": port_dwell_days,
            "base_freight": base_freight.round(2),
            "fuel_surcharge": fuel_surcharge.round(2),
            "detention_cost": detention_cost.round(2),
            "demurrage_cost": demurrage_cost.round(2),
            "storage_cost": storage_cost.round(2),
            "chassis_cost": chassis_cost.round(2),
            "accessorial_cost": accessorial_cost.round(2),
            "total_transportation_cost": total_cost.round(2),
            "target_cpc": target_cpc.round(2),
            "cpc_variance": cpc_variance.round(2),
            "cpc_escalation_flag": cpc_escalation_flag,
        }
    )
    return df


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = generate_data()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(df):,} rows at {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

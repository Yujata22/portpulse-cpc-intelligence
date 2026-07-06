from src.generate_synthetic_data import generate_data


def test_generate_data_has_rows():
    df = generate_data(n_rows=10, seed=1)
    assert len(df) == 10


def test_required_columns_exist():
    df = generate_data(n_rows=10, seed=1)
    required = {"container_id", "shipment_id", "bol", "destination_port", "total_transportation_cost"}
    assert required.issubset(set(df.columns))

# Synthetic Data Dictionary

| Column | Description |
|---|---|
| container_id | Synthetic container identifier |
| shipment_id | Synthetic shipment identifier, unique at shipment level |
| bol | Synthetic Bill of Lading identifier |
| origin_port | Origin port code |
| destination_port | U.S. destination port code |
| lane | Origin to destination lane |
| carrier | Synthetic carrier name |
| program | Business program such as Retail, FBA, Vendor Direct |
| load_type | FCL or LCL classification |
| vessel_departure | Vessel departure milestone |
| port_arrival | Port arrival milestone |
| customs_release | Customs release milestone |
| container_available | Container availability milestone |
| empty_return | Empty return milestone |
| transit_days | Vessel transit duration |
| port_dwell_days | Dwell time at port |
| base_freight | Base ocean freight cost |
| fuel_surcharge | Fuel charge component |
| detention_cost | Synthetic detention cost |
| demurrage_cost | Synthetic demurrage cost |
| storage_cost | Synthetic storage cost |
| chassis_cost | Synthetic chassis cost |
| accessorial_cost | Other accessorial charges |
| total_transportation_cost | Total cost/CPC value |
| target_cpc | Synthetic CPC benchmark |
| cpc_variance | CPC minus target CPC |
| cpc_escalation_flag | 1 if CPC variance exceeds threshold |

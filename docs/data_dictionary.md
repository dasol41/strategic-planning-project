# Data dictionary (processed)

The processed dataset `data/processed/metrics_long.csv` is a long-format table created from the wide year columns.

Columns:
- `region`: geographic scope (e.g., United States)
- `market`: market / vertical (e.g., Smart Appliances)
- `chart`: metric group (e.g., Revenue, Household Penetration Rate)
- `name`: metric name / segment (e.g., Total, Smart Appliances, Samsung)
- `unit`: original unit label (e.g., billion USD, percent)
- `source`: dataset source (e.g., Statista Market Insights)
- `year`: integer year
- `value`: numeric value (float), with 0 treated as missing for forecast-only gaps
- `cagr`: CAGR value if present in original export (may be missing/0 depending on row)

Notes:
- Some rows contain trailing zeros in future years; these are treated as missing during transformation.

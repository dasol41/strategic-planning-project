# Strategic Planning & Insights Project (Smart Appliances, U.S.)

This project builds a **strategy planning + KPI tracking** workflow by combining multi-dimensional business metrics into a unified dataset and generating **executive-ready insights**:
- Track **progress vs. goals** (Revenue, Growth, Penetration)
- Identify **operational/customer pressure points** via trend + root-cause style analysis
- Produce dashboards/figures suitable for management updates

## Dataset
This project expects the Statista Market Insights export you provided:
- `data/raw/mi_consumer_smart-home_united-states_usd_en_with_kmis_*.csv`

> ⚠️ Do not commit licensed raw data to GitHub. Keep it in `data/raw/` (gitignored).

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
pip install -r requirements.txt
```

1) Put your CSV into `data/raw/`  
2) Run the transformation:
```bash
python -m src.load_transform --input "data/raw/<your-file>.csv" --out "data/processed/metrics_long.csv"
```

3) Open the notebook:
- `notebooks/01_eda_kpi.ipynb`

## What you’ll deliver (GitHub-ready)
- Clean long-format dataset (`data/processed/metrics_long.csv`)
- KPI table + charts (Revenue trend, YoY growth, Penetration)
- A short “Strategic Insights” section (3–5 bullets) translating metrics → actions

## Project structure
```
lg-strategic-planning-insights/
  data/
    raw/           # (gitignored)
    processed/     # (gitignored)
  src/
    load_transform.py
    kpi.py
  notebooks/
    01_eda_kpi.ipynb
  reports/
    figures/
  docs/
    data_dictionary.md
```

import pandas as pd
from pathlib import Path

IN_PATH = Path.home() / "Downloads" / "smartappliances.csv"
OUT_MD = Path("reports/kpi_summary.md")
OUT_CSV = Path("reports/kpi_summary.csv")

TARGET = [
    ("Revenue", "Total"),
    ("Revenue Change", "Total"),
    ("Household Penetration Rate", "Smart Appliances"),
    ("Smart Homes", "Total"),
    ("Households", "Total"),
    ("Average Revenue per Smart Home", "Total"),
]

def pick_latest(df, chart, name):
    x = df[(df["chart"] == chart) & (df["name"] == name)].copy()
    x = x.dropna(subset=["value"]).sort_values("year")
    if x.empty:
        return None
    r = x.iloc[-1]
    return {
        "chart": chart,
        "name": name,
        "latest_year": int(r["year"]),
        "latest_value": r["value"],
        "unit": r.get("unit", ""),
    }

def last_n_years(df, chart, name, n=5):
    x = df[(df["chart"] == chart) & (df["name"] == name)].copy()
    x = x.dropna(subset=["value"]).sort_values("year")
    if x.empty:
        return x
    return x.tail(n)

def main():
    df = pd.read_csv(IN_PATH)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    rows = []
    for chart, name in TARGET:
        r = pick_latest(df, chart, name)
        if r:
            rows.append(r)

    out = pd.DataFrame(rows).sort_values(["chart", "name"])
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)

    lines = []
    lines.append("# KPI Summary (Latest Available)")
    lines.append("")
    for _, r in out.iterrows():
        lines.append(
            f"- **{r['chart']} / {r['name']}**: {r['latest_value']} {r['unit']} (Year: {r['latest_year']})"
        )

    lines.append("")
    lines.append("## Recent Trend Snapshots (Last 5 Available Years)")
    lines.append("")

    for chart, name in TARGET[:3]:
        t = last_n_years(df, chart, name, n=5)
        if t.empty:
            continue
        lines.append(f"### {chart} / {name}")
        lines.append("")
        for _, rr in t.iterrows():
            lines.append(f"- {int(rr['year'])}: {rr['value']} {rr.get('unit','')}")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    main()

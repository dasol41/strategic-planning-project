import pandas as pd
import numpy as np

def latest_non_null(series: pd.Series):
    s = series.dropna()
    if s.empty:
        return np.nan
    return s.iloc[-1]

def compute_kpis(long_df: pd.DataFrame) -> pd.DataFrame:
    """Return a compact KPI table for core strategic metrics."""
    core = long_df[long_df["chart"].isin([
        "Revenue", "Revenue Change", "Household Penetration Rate",
        "Average Revenue per Smart Home", "Smart Homes", "Households"
    ])].copy()

    # For each metric/name, compute latest value and latest year
    grp = core.groupby(["chart","name","unit"], as_index=False)
    out = grp.apply(lambda g: pd.Series({
        "latest_year": int(g.loc[g["value"].notna(),"year"].max()) if g["value"].notna().any() else np.nan,
        "latest_value": latest_non_null(g.sort_values("year")["value"])
    })).reset_index()

    return out.sort_values(["chart","name"])

def add_revenue_alignment(long_df: pd.DataFrame) -> pd.DataFrame:
    """Example 'alignment' score using demand proxy vs. capacity-like metrics if available."""
    # Placeholder: you can expand this once you add additional datasets (Trends, BLS, etc.)
    return pd.DataFrame()

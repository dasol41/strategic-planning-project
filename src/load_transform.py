import argparse
import pandas as pd
import numpy as np
from pathlib import Path

def to_num(x):
    try:
        s = str(x).replace(",", "").strip()
        if s == "" or s.lower() in {"nan", "none"}:
            return np.nan
        return float(s)
    except Exception:
        return np.nan

def transform_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    year_cols = [c for c in df.columns if c.isdigit()]
    id_cols = [c for c in df.columns if c not in year_cols]

    long_df = df.melt(id_vars=id_cols, value_vars=year_cols, var_name="year", value_name="value")
    long_df["year"] = long_df["year"].astype(int)
    long_df["value"] = long_df["value"].map(to_num)

    # Many exports encode missing forecasts as 0 — treat 0 as missing ONLY when the row has non-zero history.
    # This keeps genuine 0 values (rare in economic datasets) from being over-cleaned.
    grp_keys = ["Region", "Market", "Chart", "Name", "Unit", "Source"]
    def fix_zeros(g):
        if (g["value"] > 0).any():
            g.loc[g["value"] == 0, "value"] = np.nan
        return g

    long_df = long_df.groupby(grp_keys, group_keys=False).apply(fix_zeros)

    # Standardize column names for analysis
    long_df = long_df.rename(columns={
        "Region": "region",
        "Market": "market",
        "Chart": "chart",
        "Name": "name",
        "Unit": "unit",
        "Source": "source"
    })

    # CAGR column if present
    if "CAGR" in long_df.columns:
        pass

    return long_df[["region","market","chart","name","unit","source","year","value"]]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to raw CSV")
    ap.add_argument("--out", required=True, help="Path to write processed long CSV")
    args = ap.parse_args()

    inp = Path(args.input)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(inp)
    long_df = transform_wide_to_long(df)
    long_df.to_csv(out, index=False)
    print(f"Wrote {len(long_df):,} rows to {out}")

if __name__ == "__main__":
    main()

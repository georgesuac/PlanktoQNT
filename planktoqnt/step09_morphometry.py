import sqlite3
import pandas as pd
import numpy as np


def run(config, paths):

    print("\n[Step 09] Computing taxon-level morphometry...")

    input_db = paths["carbon_dir"] / "4_particle_carbon.db"
    output_db = paths["metrics_dir"] / "9_morphometry.db"

    settings = config.get("settings", {})
    group_by_col = settings.get("summary_group_by", "taxon_name")

    conn = sqlite3.connect(input_db)
    df = pd.read_sql("SELECT * FROM ifcb_particle_carbon;", conn)
    conn.close()

    print(f"Input rows: {len(df)}")
    print(f"Grouping by: {group_by_col}")

    if group_by_col not in df.columns:
        raise ValueError(f"Grouping column '{group_by_col}' not found.")

    # === Variables to summarize ===
    variables = [
        "Area",
        "Biovolume",
        "EquivDiameter",
        "MajorAxisLength",
        "MinorAxisLength",
        "carbon_pgC",
        "carbon_ugC",
    ]

    # Drop rows with missing values in key variables
    df = df.dropna(subset=variables + [group_by_col])

    # === Group and compute stats ===
    grouped = df.groupby(group_by_col, dropna=False)

    summary = grouped[variables].agg(["mean", "std", "count"]).reset_index()

    # Flatten multi-index columns
    summary.columns = [
        "_".join(col).strip("_") if isinstance(col, tuple) else col
        for col in summary.columns
    ]

    # === Compute SE ===
    for var in variables:
        summary[f"{var}_se"] = summary[f"{var}_std"] / np.sqrt(summary[f"{var}_count"])

    # === Save ===
    conn_out = sqlite3.connect(output_db)
    summary.to_sql("morphometry_summary", conn_out, if_exists="replace", index=False)
    conn_out.close()

    print(f"[Step 09] Database created: {output_db}")
    print(f"[Step 09] Rows: {len(summary)}")
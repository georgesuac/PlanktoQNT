import sqlite3
import pandas as pd


def run(config, paths):
    print("\n[Step 05] Computing sample-level taxonomic abundance and biomass...")

    input_db = paths["carbon_dir"] / "4_particle_carbon.db"
    output_db = paths["summary_dir"] / "5_sample_summary.db"

    settings = config.get("settings", {})
    group_by_col = settings.get("summary_group_by", "category")
    analyzed_volume_L = float(settings.get("analyzed_volume_L", 0.005))

    conn = sqlite3.connect(input_db)
    df = pd.read_sql("SELECT * FROM ifcb_particle_carbon;", conn)
    conn.close()

    if group_by_col not in df.columns:
        raise ValueError(
            f"Grouping column '{group_by_col}' not found. "
            f"Available columns include: {df.columns.tolist()}"
        )

    print(f"Input rows: {len(df)}")
    print(f"Grouping by: {group_by_col}")
    print(f"Analyzed volume: {analyzed_volume_L} L")

    df[group_by_col] = df[group_by_col].fillna("Unclassified")

    group_cols = [
        "file_name",
        "folder_id",
        "year",
        "day",
        "treatment",
        "replicate",
        group_by_col,
    ]

    available_group_cols = [c for c in group_cols if c in df.columns]

    summary = (
        df.groupby(available_group_cols, dropna=False)
        .agg(
            particles=("file_name_w_roi", "count"),
            carbon_ugC=("carbon_ugC", "sum"),
        )
        .reset_index()
    )

    summary["effective_volume_L"] = analyzed_volume_L
    summary["abundance_per_L"] = summary["particles"] / analyzed_volume_L
    summary["carbon_ugC_per_L"] = summary["carbon_ugC"] / analyzed_volume_L

    conn_out = sqlite3.connect(output_db)
    summary.to_sql("ifcb_sample_summary", conn_out, if_exists="replace", index=False)
    conn_out.close()

    print(f"\n[Step 05] Database created: {output_db}")
    print(f"[Step 05] Rows: {len(summary)}")
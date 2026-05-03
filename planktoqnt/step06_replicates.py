import sqlite3
import pandas as pd


def run(config, paths):
    print("\n[Step 06] Merging technical replicate IFCB runs...")

    input_db = paths["summary_dir"] / "5_sample_summary.db"
    output_db = paths["replicates_dir"] / "6_replicate_summary.db"

    conn = sqlite3.connect(input_db)
    df = pd.read_sql("SELECT * FROM ifcb_sample_summary;", conn)
    conn.close()

    print(f"Input rows: {len(df)}")

    settings = config.get("settings", {})
    group_by_col = settings.get("summary_group_by", "category")

    if group_by_col not in df.columns:
        raise ValueError(f"Grouping column '{group_by_col}' not found in Step 05 output.")

    replicate_cols = ["year", "day", "treatment", "replicate"]

    # Total volume and number of IFCB runs per biological replicate
    replicate_volume = (
        df[replicate_cols + ["file_name", "effective_volume_L"]]
        .drop_duplicates()
        .groupby(replicate_cols, dropna=False)
        .agg(
            effective_volume_L=("effective_volume_L", "sum"),
            n_ifcb_runs=("file_name", "nunique"),
        )
        .reset_index()
    )

    # Sum particles and carbon per biological replicate × taxonomic group
    taxon_summary = (
        df.groupby(replicate_cols + [group_by_col], dropna=False)
        .agg(
            particles=("particles", "sum"),
            carbon_ugC=("carbon_ugC", "sum"),
        )
        .reset_index()
    )

    # Merge total replicate volume back onto each taxonomic group
    replicate_summary = taxon_summary.merge(
        replicate_volume,
        on=replicate_cols,
        how="left"
    )

    replicate_summary["abundance_per_L"] = (
        replicate_summary["particles"] / replicate_summary["effective_volume_L"]
    )

    replicate_summary["carbon_ugC_per_L"] = (
        replicate_summary["carbon_ugC"] / replicate_summary["effective_volume_L"]
    )

    conn_out = sqlite3.connect(output_db)
    replicate_summary.to_sql(
        "ifcb_replicate_summary",
        conn_out,
        if_exists="replace",
        index=False,
    )
    conn_out.close()

    print(f"\n[Step 06] Database created: {output_db}")
    print(f"[Step 06] Rows: {len(replicate_summary)}")
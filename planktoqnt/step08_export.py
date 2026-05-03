import sqlite3
import pandas as pd


def run(config, paths):
    print("\n[Step 08] Exporting final datasets...")

    input_db = paths["metrics_dir"] / "7_ecological_metrics.db"
    output_dir = paths["exports_dir"]

    conn = sqlite3.connect(input_db)

    # === Export replicate-level metrics ===
    replicate_df = pd.read_sql("SELECT * FROM replicate_ecological_metrics;", conn)

    replicate_path = output_dir / "replicate_ecological_metrics.csv"
    replicate_df.to_csv(replicate_path, index=False)

    # === Export group contributions ===
    group_df = pd.read_sql("SELECT * FROM group_relative_contributions;", conn)

    group_path = output_dir / "group_relative_contributions.csv"
    group_df.to_csv(group_path, index=False)

    conn.close()

    print(f"[Step 08] Exported:")
    print(f" - {replicate_path}")
    print(f" - {group_path}")
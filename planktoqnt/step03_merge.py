from pathlib import Path
import sqlite3
import pandas as pd


def run(config, paths):

    print("\n[Step 03] Merging IFCB features with PlanktoNET classification...")

    features_db = paths["features_dir"] / "1_ifcb_features.db"
    classification_db = paths["classification_dir"] / "2_planktonet_classification.db"
    output_db = paths["merged_dir"] / "3_merged_ifcb_data.db"

    # === Load features ===
    conn_feat = sqlite3.connect(features_db)
    features_df = pd.read_sql("SELECT * FROM ifcb_features;", conn_feat)
    conn_feat.close()

    # === Load classification ===
    conn_class = sqlite3.connect(classification_db)
    class_df = pd.read_sql("SELECT * FROM planktonet_classification;", conn_class)
    conn_class.close()

    print(f"Features rows: {len(features_df)}")
    print(f"Classification rows: {len(class_df)}")

    # === Merge using unique particle ID ===
    merged_df = features_df.merge(
        class_df,
        how="left",
        on="file_name_w_roi",
        suffixes=("", "_class")
    )

    # Optional: drop duplicated columns coming from classification
    drop_cols = ["file_name_class", "folder_id_class", "roi_number_class"]
    merged_df = merged_df.drop(columns=[c for c in drop_cols if c in merged_df.columns])

    # === Save ===
    conn_out = sqlite3.connect(output_db)
    merged_df.to_sql("ifcb_with_classification", conn_out, if_exists="replace", index=False)
    conn_out.close()

    print(f"\n[Step 03] Database created: {output_db}")
    print(f"[Step 03] Rows: {len(merged_df)}")

    classified = merged_df["class_name"].notna().sum()
    print(f"[Step 03] Classified particles: {classified}")
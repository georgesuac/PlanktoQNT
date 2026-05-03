from pathlib import Path
import sqlite3
import pandas as pd
from glob import glob
from tqdm import tqdm


def run(config, paths):

    print("\n[Step 01] Building IFCB feature database...")

    feature_dir = paths["ifcb_feature_output"]
    metadata_path = paths["ifcb_metadata"]
    output_db = paths["features_dir"] / "1_ifcb_features.db"

    # === Load metadata ===
    metadata_df = pd.read_csv(metadata_path)

    # Normalize naming
    metadata_df = metadata_df.rename(columns={"folder": "folder_id"})
    metadata_df["folder_id"] = metadata_df["folder_id"].str.replace("_IFCB108", "", regex=False)

    # === SQLite setup ===
    conn = sqlite3.connect(output_db)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ifcb_features")
    conn.commit()

    # === Get feature files ===
    csv_files = sorted(glob(str(feature_dir / "*.csv")))

    print(f"Found {len(csv_files)} feature files")

    exclude_prefixes = ["Wedge", "Ring", "HOG"]

    for file_path in tqdm(csv_files):

        file_path = Path(file_path)
        file_name = file_path.name.replace("_fea_v2.csv", "")
        folder_id = file_name.split("_IFCB")[0]

        df = pd.read_csv(file_path)

        # === Drop high-dimensional ML features ===
        cols_to_drop = [col for col in df.columns if any(col.startswith(p) for p in exclude_prefixes)]
        df = df.drop(columns=cols_to_drop)

        # === Multi-blob correction ===
        cols = [
            "Area", "Biovolume", "ConvexArea", "ConvexPerimeter",
            "FeretDiameter", "MajorAxisLength", "MinorAxisLength", "Perimeter"
        ]

        for col in cols:
            summed_col = f"summed{col}"
            if summed_col in df.columns and "numBlobs" in df.columns:
                df[col] = df.apply(
                    lambda row: row[summed_col] if row["numBlobs"] > 1 else row[col],
                    axis=1
                )

        # === Identifiers ===
        df["roi_number"] = df["roi_number"].astype(int)
        df["roi_number_str"] = df["roi_number"].apply(lambda x: f"{x:05d}")

        df["file_name"] = file_name
        df["file_name_w_roi"] = file_name + "_" + df["roi_number_str"]
        df["folder_id"] = folder_id

        df = df.drop(columns=["roi_number_str"])

        # === Merge metadata ===
        merged = df.merge(metadata_df, on="folder_id", how="left")

        # === Column order ===
        base_cols = ["file_name", "file_name_w_roi", "folder_id", "roi_number"]
        other_cols = [c for c in merged.columns if c not in base_cols]
        merged = merged[base_cols + other_cols]

        # === Save ===
        merged.to_sql("ifcb_features", conn, if_exists="append", index=False)

    conn.close()

    print(f"\n[Step 01] Database created: {output_db}")
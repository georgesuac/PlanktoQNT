from pathlib import Path
import sqlite3
import pandas as pd
from tqdm import tqdm


def parse_image_name(image_name):
    stem = Path(image_name).stem
    parts = stem.split("_")

    roi_number = int(parts[-1])
    file_name = "_".join(parts[:-1])
    file_name_w_roi = f"{file_name}_{roi_number:05d}"
    folder_id = file_name.split("_IFCB")[0]

    return file_name, folder_id, roi_number, file_name_w_roi


def run(config, paths):
    print("\n[Step 02] Building PlanktoNET classification database...")

    planktonet_root = paths["planktonet_results"]
    taxonomic_info_path = paths["taxonomic_info"]
    output_db = paths["classification_dir"] / "2_planktonet_classification.db"

    if not planktonet_root.exists():
        raise FileNotFoundError(f"PlanktoNET results folder not found: {planktonet_root}")

    if not taxonomic_info_path.exists():
        raise FileNotFoundError(f"taxonomic_info.csv not found: {taxonomic_info_path}")

    taxonomic_df = pd.read_csv(taxonomic_info_path)

    records = []

    sample_dirs = sorted([p for p in planktonet_root.iterdir() if p.is_dir()])
    print(f"Found {len(sample_dirs)} PlanktoNET sample folders")

    for sample_dir in tqdm(sample_dirs):
        confidence_file = sample_dir / "confidence.tsv"

        if not confidence_file.exists():
            print(f"Warning: confidence.tsv not found in {sample_dir}")
            continue

        df = pd.read_csv(confidence_file, sep="\t")

        required_cols = {"image_name", "class_name", "confidence"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns in {confidence_file}: {missing}")

        for _, row in df.iterrows():
            file_name, folder_id, roi_number, file_name_w_roi = parse_image_name(row["image_name"])

            records.append({
                "file_name": file_name,
                "file_name_w_roi": file_name_w_roi,
                "folder_id": folder_id,
                "roi_number": roi_number,
                "image_name": row["image_name"],
                "class_name": row["class_name"],
                "probability": float(row["confidence"]),
            })

    classification_df = pd.DataFrame(records)

    classification_merged = classification_df.merge(
        taxonomic_df,
        on="class_name",
        how="left"
    )

    conn = sqlite3.connect(output_db)
    classification_merged.to_sql(
        "planktonet_classification",
        conn,
        if_exists="replace",
        index=False
    )
    conn.close()

    print(f"\n[Step 02] Database created: {output_db}")
    print(f"[Step 02] Rows: {len(classification_merged)}")
from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np


def run(config, paths):

    print("\n[Step 04] Calculating particle-level carbon biomass...")

    input_db = paths["merged_dir"] / "3_merged_ifcb_data.db"
    output_db = paths["carbon_dir"] / "4_particle_carbon.db"

    # === Load merged data ===
    conn = sqlite3.connect(input_db)
    df = pd.read_sql("SELECT * FROM ifcb_with_classification;", conn)
    conn.close()

    print(f"Input rows: {len(df)}")

    # === Convert volume ===
    PIXEL_TO_UM3 = 0.422
    df["volume_um3"] = df["Biovolume"] * PIXEL_TO_UM3

    # === Carbon calculation ===
    def assign_carbon(row):
        V = row["volume_um3"]
        category = row.get("category")

        if pd.isna(V) or V <= 0 or pd.isna(category):
            return pd.Series({"carbon_formula": None, "carbon_pgC": None})

        if category == "Diatoms":
            pgC = 0.288 * (V ** 0.811)
            formula = "Menden-Deuer 2000: Diatom"

        elif category == "Dinoflagellates":
            pgC = 0.760 * (V ** 0.819)
            formula = "Menden-Deuer 2000: Dino"

        elif category == "Ciliates":
            pgC = 0.216 * (V ** 0.939)
            formula = "Putt & Stoecker 1989: Ciliate"

        elif category == "Detritus":
            pgC = 0.22 * V
            formula = "Parsons et al. 1984: Detritus"

        else:
            pgC = 0.216 * (V ** 0.939)
            formula = "Putt & Stoecker 1989: Other Protists"

        return pd.Series({
            "carbon_formula": formula,
            "carbon_pgC": pgC
        })

    df[["carbon_formula", "carbon_pgC"]] = df.apply(assign_carbon, axis=1)

    # === Convert to µg C (more useful later) ===
    df["carbon_ugC"] = df["carbon_pgC"] * 1e-6

    # === Save ===
    conn_out = sqlite3.connect(output_db)
    df.to_sql("ifcb_particle_carbon", conn_out, if_exists="replace", index=False)
    conn_out.close()

    print(f"\n[Step 04] Database created: {output_db}")
    print(f"[Step 04] Rows: {len(df)}")

    valid = df["carbon_pgC"].notna().sum()
    print(f"[Step 04] Particles with carbon: {valid}")
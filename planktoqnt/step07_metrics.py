import sqlite3
import pandas as pd
import numpy as np


def run(config, paths):
    print("\n[Step 07] Calculating ecological metrics...")

    input_db = paths["replicates_dir"] / "6_replicate_summary.db"
    output_db = paths["metrics_dir"] / "7_ecological_metrics.db"

    settings = config.get("settings", {})
    group_by_col = settings.get("summary_group_by", "category")

    conn = sqlite3.connect(input_db)
    df = pd.read_sql("SELECT * FROM ifcb_replicate_summary;", conn)
    conn.close()

    print(f"Input rows: {len(df)}")
    print(f"Grouping by: {group_by_col}")

    replicate_cols = ["year", "day", "treatment", "replicate"]

    if group_by_col not in df.columns:
        raise ValueError(f"Grouping column '{group_by_col}' not found in Step 06 output.")

    # Total abundance and biomass per biological replicate
    totals = (
        df.groupby(replicate_cols, dropna=False)
        .agg(
            total_particles=("particles", "sum"),
            total_carbon_ugC=("carbon_ugC", "sum"),
            total_abundance_per_L=("abundance_per_L", "sum"),
            total_carbon_ugC_per_L=("carbon_ugC_per_L", "sum"),
            n_groups=(group_by_col, "nunique"),
        )
        .reset_index()
    )

    # Relative contribution of each group
    df = df.merge(
        totals[
            replicate_cols
            + ["total_abundance_per_L", "total_carbon_ugC_per_L", "total_particles", "total_carbon_ugC"]
        ],
        on=replicate_cols,
        how="left",
    )

    df["relative_abundance"] = df["abundance_per_L"] / df["total_abundance_per_L"]
    df["relative_carbon"] = df["carbon_ugC_per_L"] / df["total_carbon_ugC_per_L"]

    # Diversity metrics based on particle counts
    def shannon(p):
        p = p[p > 0]
        return -np.sum(p * np.log(p))

    def simpson_dominance(p):
        p = p[p > 0]
        return np.sum(p ** 2)

    diversity_records = []

    for keys, group in df.groupby(replicate_cols, dropna=False):
        total_particles = group["particles"].sum()

        if total_particles > 0:
            p = group["particles"] / total_particles
            shannon_H = shannon(p)
            simpson_D = simpson_dominance(p)
        else:
            shannon_H = np.nan
            simpson_D = np.nan

        record = dict(zip(replicate_cols, keys))
        record["shannon_H"] = shannon_H
        record["simpson_dominance_D"] = simpson_D
        record["simpson_diversity_1_minus_D"] = 1 - simpson_D if not pd.isna(simpson_D) else np.nan
        record["richness_n_groups"] = group[group["particles"] > 0][group_by_col].nunique()

        diversity_records.append(record)

    diversity = pd.DataFrame(diversity_records)

    replicate_metrics = totals.merge(
        diversity,
        on=replicate_cols,
        how="left",
    )

    # Save outputs
    conn_out = sqlite3.connect(output_db)

    replicate_metrics.to_sql(
        "replicate_ecological_metrics",
        conn_out,
        if_exists="replace",
        index=False,
    )

    df.to_sql(
        "group_relative_contributions",
        conn_out,
        if_exists="replace",
        index=False,
    )

    conn_out.close()

    print(f"\n[Step 07] Database created: {output_db}")
    print(f"[Step 07] Replicate metrics rows: {len(replicate_metrics)}")
    print(f"[Step 07] Group contribution rows: {len(df)}")
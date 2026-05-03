from pathlib import Path


def get_project_paths(config):
    project_dir = Path(config["project_dir"])

    paths = {
        "project_dir": project_dir,
        "metadata_dir": project_dir / "02_metadata",
        "datasets_dir": project_dir / "03_datasets",


        "features_dir": project_dir / "03_datasets" / "01_features",
        "classification_dir": project_dir / "03_datasets" / "02_classification",
        "merged_dir": project_dir / "03_datasets" / "03_merged",
        "carbon_dir": project_dir / "03_datasets" / "04_carbon",
        "summary_dir": project_dir / "03_datasets" / "05_summary",
        "replicates_dir": project_dir / "03_datasets" / "06_replicates",
        "metrics_dir": project_dir / "03_datasets" / "07_metrics",
        "exports_dir": project_dir / "03_datasets" / "08_exports",

        "ifcb_feature_output": Path(config["paths"]["ifcb_feature_output"]).expanduser().resolve(),
        "planktonet_results": Path(config["paths"]["planktonet_results"]).expanduser().resolve(),

        "ifcb_metadata": project_dir / "02_metadata" / "IFCB_info.csv",
        "taxonomic_info": project_dir / "02_metadata" / "taxonomic_info.csv",
    }

    return paths


def create_output_dirs(paths):
    output_keys = [
        "features_dir",
        "classification_dir",
        "merged_dir",
        "carbon_dir",
        "summary_dir",
        "replicates_dir",
        "metrics_dir",
        "exports_dir",
    ]

    for key in output_keys:
        paths[key].mkdir(parents=True, exist_ok=True)
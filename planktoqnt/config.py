from pathlib import Path
import yaml


def load_config(config_path):
    config_path = Path(config_path).resolve()

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    project_dir = config_path.parent
    config["project_dir"] = project_dir
    config["config_path"] = config_path

    return config
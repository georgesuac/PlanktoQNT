import argparse

from planktoqnt.config import load_config
from planktoqnt.paths import get_project_paths, create_output_dirs
from planktoqnt.step01_features_db import run as step01
from planktoqnt.step02_classification_db import run as step02
from planktoqnt.step03_merge import run as step03
from planktoqnt.step04_carbon import run as step04
from planktoqnt.step05_summary import run as step05
from planktoqnt.step06_replicates import run as step06
from planktoqnt.step07_metrics import run as step07
from planktoqnt.step08_export import run as step08
from planktoqnt.step09_morphometry import run as step09

def main():
    parser = argparse.ArgumentParser(description="Run the PlanktoQNT pipeline.")
    parser.add_argument(
        "--config",
        required=True,
        help="Path to project config.yaml file",
    )

    args = parser.parse_args()

    config = load_config(args.config)
    paths = get_project_paths(config)
    create_output_dirs(paths)

    print("\nPlanktoQNT pipeline initialized")
    print(f"Project: {config.get('project_name')}")
    print(f"Project directory: {paths['project_dir']}")
    print(f"IFCB feature output: {paths['ifcb_feature_output']}")
    print(f"PlanktoNET results: {paths['planktonet_results']}")
    print("\nOutput folders checked/created successfully.\n")

    # Step calls are added here. Comment out steps as needed.
    step01(config, paths)
    step02(config, paths)
    step03(config, paths)
    step04(config, paths)
    step05(config, paths)
    step06(config, paths)
    step07(config, paths)
    step08(config, paths)
    step09(config, paths)


if __name__ == "__main__":
    main()
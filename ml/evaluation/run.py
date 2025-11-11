from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(path: str) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main(config_path: str) -> None:
    config = load_config(config_path)
    print("Loaded config for evaluation:")
    print(yaml.dump(config, sort_keys=False))
    print("TODO: implement evaluation metrics.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run evaluation pipeline.")
    parser.add_argument("--config", required=True, help="Path to YAML config.")
    args = parser.parse_args()
    main(args.config)

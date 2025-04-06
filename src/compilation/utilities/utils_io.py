import json
from pathlib import Path

import yaml


# JSON utils
def json_load(file_path: Path):
    """Load data from a JSON file."""
    with file_path.open("r") as f:
        return json.load(f)


def json_dump(data, file_path: Path):
    """Dump data to a JSON file."""
    with file_path.open("w") as f:
        json.dump(data, f, indent=4)


# YAML utils
def yaml_load(file_path: Path):
    """Load data from a YAML file."""
    with file_path.open("r") as f:
        return yaml.safe_load(f)


def yaml_dump(data, file_path: Path):
    """Dump data to a YAML file."""
    with file_path.open("w") as f:
        yaml.safe_dump(data, f, default_flow_style=False)


# Text utils
def file_load(file_path: Path):
    """Load data from a text file."""
    with file_path.open("r") as f:
        return f.read()


def file_dump(data, file_path: Path):
    """Dump data to a text file."""
    with file_path.open("w") as f:
        f.write(data)

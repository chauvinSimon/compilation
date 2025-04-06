from utilities.utils_io import yaml_load
from utilities.utils_path import compilation_configs_dir, config_path


def load_config():
    return yaml_load(config_path)


def load_compilation_config():
    config = load_config()
    compilation_file_name = config["compilation_file_name"]
    compilation_file_path = compilation_configs_dir / compilation_file_name
    assert (
        compilation_file_path.exists()
    ), f"no compilation_file at {compilation_file_path}"
    return yaml_load(compilation_file_path)


if __name__ == "__main__":
    print(load_config())
    print(load_compilation_config())

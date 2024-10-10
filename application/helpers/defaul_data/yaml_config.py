import yaml


def load_config_yaml(yaml_file):
    """
    Load a YAML file and return the configuration as a dictionary.
    """
    try:
        with open(yaml_file, 'r') as stream:
            config = yaml.safe_load(stream)
            return config
    except FileNotFoundError as exc:
        print(f"File not found: {exc}")
        
    except yaml.YAMLError as exc:
        print(f"YAML error: {exc}")

from pathlib import Path

def find_project_root() -> Path:
    """Find the project root directory by looking for .project_root file"""
    current = Path.cwd()
    while current != current.parent:
        if (current / '.project_root').exists():
            return current
        current = current.parent
    raise FileNotFoundError("Could not find project root directory")

def get_frontend_dir() -> Path:
    """Get the frontend directory path"""
    return find_project_root() / 'frontend'

def get_config_path() -> Path:
    """Get the config file path"""
    return get_frontend_dir() / 'config' / 'config.yaml' 
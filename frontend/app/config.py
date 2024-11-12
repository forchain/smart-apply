import yaml
from typing import Dict, Any, Optional
from pathlib import Path

def get_config_path() -> Path:
    """Get the config file path"""
    return Path(__file__).parent.parent / 'config' / 'config.yaml'

class Config:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        config_path = get_config_path()
        if not config_path.exists():
            return {}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_api_base_url(self) -> str:
        """Get API base URL"""
        return self._config.get('api', {}).get('base_url', 'http://localhost:8000/api/v1')

    def get_default_resume(self) -> str:
        """Get default resume text"""
        return self._config.get('defaults', {}).get('resume', '')

    def get_default_jd(self) -> str:
        """Get default job description text"""
        return self._config.get('defaults', {}).get('jd', '')
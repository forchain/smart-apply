import yaml
from pathlib import Path
from typing import Dict, Any, Optional

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
        config_path = Path("config/config.yaml")
        if not config_path.exists():
            return {}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_default_resume(self) -> str:
        """Get default resume text"""
        return self._config.get('defaults', {}).get('resume', '')

    def get_default_jd(self) -> str:
        """Get default job description text"""
        return self._config.get('defaults', {}).get('jd', '') 
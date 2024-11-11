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
        config_path = Path("config.yaml")
        if not config_path.exists():
            return {}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get(self, section: str, default: Any = None) -> Any:
        """Get a value from config by section"""
        return self._config.get(section, default)

    def get_model_config(self, provider: str) -> Dict[str, str]:
        """Get model configuration for specified provider"""
        return self._config.get(provider, {})

    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for specified provider"""
        return self.get_model_config(provider).get('api_key')

    def get_model(self, provider: str) -> str:
        """Get model name for specified provider"""
        return self.get_model_config(provider).get('model')

    def get_base_url(self, provider: str) -> Optional[str]:
        """Get base URL for specified provider"""
        return self.get_model_config(provider).get('base_url')

    def get_default_resume(self) -> str:
        """Get default resume text"""
        return self._config.get('defaults', {}).get('resume', '')

    def get_default_jd(self) -> str:
        """Get default job description text"""
        return self._config.get('defaults', {}).get('jd', '') 
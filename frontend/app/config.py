import yaml
from pathlib import Path

class Config:
    def __init__(self):
        self.config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        self.config = self._load_config()
        
    def _load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
            
    def _read_template(self, path):
        """读取模板文件"""
        try:
            template_path = Path(__file__).parent.parent / path
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading template {path}: {e}")
            return ""

    def get_api_base_url(self):
        """获取API基础URL"""
        return self.config.get("api", {}).get("base_url", "http://localhost:8000/api/v1")

    def get_provider_api_key(self, provider):
        """获取指定提供商的API密钥"""
        return self.config.get("providers", {}).get(provider, {}).get("api_key", "")

    def get_default_resume(self):
        """获取默认简历模板"""
        resume_path = self.config.get("templates", {}).get("resume", "")
        return self._read_template(resume_path)

    def get_default_jd(self):
        """获取默认职位描述模板"""
        jd_path = self.config.get("templates", {}).get("job_description", "")
        return self._read_template(jd_path)

    def get_cover_letter_example(self, language="en"):
        """获取指定语言的求职信模板"""
        cover_letter_paths = self.config.get("templates", {}).get("cover_letter", {})
        template_path = cover_letter_paths.get(language, "")
        return self._read_template(template_path)
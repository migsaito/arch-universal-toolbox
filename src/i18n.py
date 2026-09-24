import json
from pathlib import Path
from typing import Dict, Any

class I18n:
    """Simple internationalization manager"""
    
    def __init__(self, lang: str = "en_US"):
        self.lang = lang
        self.translations: Dict[str, Any] = {}
        self.load_language(lang)
    
    def load_language(self, lang: str):
        """Load translations from JSON file"""
        self.lang = lang
        local_dir = Path(__file__).parent / "locales"
        system_dir = Path("/usr/share/arch-universal-toolbox/locales")
        locale_dir = system_dir if system_dir.exists() else local_dir
        lang_file = locale_dir / f"{lang}.json"
        
        if lang_file.exists():
            with open(lang_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        else:
            # Fallback to English
            en_file = locale_dir / "en_US.json"
            with open(en_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
    
    def translate(self, key: str) -> str:
        """Get translation for a key"""
        return self.translations.get(key, key)
    
    def t(self, key: str) -> str:
        """Shorthand for translate"""
        return self.translate(key)

# Global instance
_i18n = None

def get_i18n() -> I18n:
    global _i18n
    if _i18n is None:
        _i18n = I18n()
    return _i18n

def set_language(lang: str):
    """Change language"""
    get_i18n().load_language(lang)

def t(key: str) -> str:
    """Global translate shorthand"""
    return get_i18n().translate(key)

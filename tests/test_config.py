import json

from src import config


def test_load_settings_returns_defaults_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CONFIG_FILE", tmp_path / "settings.json")
    assert config.load_settings() == {"language": "en_US"}


def test_save_and_load_settings(tmp_path, monkeypatch):
    config_file = tmp_path / "nested" / "settings.json"
    monkeypatch.setattr(config, "CONFIG_FILE", config_file)
    monkeypatch.setattr(config, "CONFIG_DIR", config_file.parent)

    config.save_settings({"language": "pt_BR", "theme": "dark"})

    assert json.loads(config_file.read_text(encoding="utf-8")) == {
        "language": "pt_BR",
        "theme": "dark",
    }
    assert config.load_settings()["language"] == "pt_BR"

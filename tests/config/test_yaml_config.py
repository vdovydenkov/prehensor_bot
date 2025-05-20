# tests/config/test_yaml_config.py

from pathlib import Path

import bot.config.configurator as cfg_mod
from bot.config.defaults import DEFAULT_RAW_CONFIG

def test_load_yaml_config_invalid(tmp_path, monkeypatch):
    """
    Проверяет, что при битом YAML возвращается DEFAULT_RAW_CONFIG
    """
    cfg_dir = Path(cfg_mod.__file__).parent
    # Создаём битый settings.yaml
    (cfg_dir / "settings.yaml").write_text("not: valid: yaml", encoding="utf-8")

    # Должен сработать fallback на DEFAULT_RAW_CONFIG
    cfg = cfg_mod.load_yaml_config(path=cfg_dir / "settings.yaml")
    assert cfg_mod.YAMLSettings.model_validate(DEFAULT_RAW_CONFIG) == cfg

def test_DEFAULT_RAW_CONFIG_is_valid():
    """
    Проверяет, что DEFAULT_RAW_CONFIG валиден для YAMLSettings.
    Это гарантирует, что он может использоваться как fallback.
    """
    cfg = cfg_mod.YAMLSettings.model_validate(DEFAULT_RAW_CONFIG)
    assert isinstance(cfg, cfg_mod.YAMLSettings)



# tests/config/test_yaml_config.py

from pathlib import Path

import bot.config.configurator as cfg_mod
from bot.config.defaults import DEFAULT_RAW_CONFIG

def test_load_yaml_config_invalid(tmp_path):
    """
    Проверяет, что при битом YAML возвращается DEFAULT_RAW_CONFIG,
    используя временный settings.yaml в tmp_path.
    """
    broken_yaml = tmp_path / "settings.yaml"
    broken_yaml.write_text("not: valid: yaml", encoding="utf-8")

    # Передаём путь к битому файлу напрямую
    cfg = cfg_mod.load_yaml_config(path=broken_yaml)

    assert cfg_mod.YAMLSettings.model_validate(DEFAULT_RAW_CONFIG) == cfg

def test_DEFAULT_RAW_CONFIG_is_valid():
    """
    Проверяет, что DEFAULT_RAW_CONFIG валиден для YAMLSettings.
    Это гарантирует, что он может использоваться как fallback.
    """
    cfg = cfg_mod.YAMLSettings.model_validate(DEFAULT_RAW_CONFIG)
    assert isinstance(cfg, cfg_mod.YAMLSettings)



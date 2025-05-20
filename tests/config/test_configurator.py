# tests/config/test_configurator.py

import pytest
import yaml
from pathlib import Path

# Импортируем тестируемый модуль
import bot.config.configurator as cfg_mod
# Импорт значений по умолчанию
from bot.config.defaults import DEFAULT_RAW_CONFIG


@pytest.fixture(autouse=True)
def fake_base_dir(tmp_path, monkeypatch):
    """
    Подменяет базовую структуру каталогов и создаёт settings.yaml
    с содержимым из DEFAULT_RAW_CONFIG. Это позволяет изолировать
    тесты от реального окружения и конфигураций.
    """
    # Подменяем рабочий каталог, чтобы всё шло через tmp_path
    monkeypatch.chdir(tmp_path)

    # Создаём поддельную структуру каталога: bot/config
    fake_conf_path = tmp_path / "bot" / "config"
    fake_conf_path.mkdir(parents=True)

    # Сохраняем DEFAULT_RAW_CONFIG как settings.yaml
    settings_path = fake_conf_path / "settings.yaml"
    settings_path.write_text(yaml.dump(DEFAULT_RAW_CONFIG, allow_unicode=True), encoding="utf-8")

    # Подменяем __file__ у модуля configurator, чтобы он искал settings.yaml в tmp_path
    monkeypatch.setattr(cfg_mod, "__file__", str(fake_conf_path / "configurator.py"))

    yield

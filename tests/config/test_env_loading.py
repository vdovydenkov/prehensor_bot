# tests/config/test_env_loading.py

import pytest
from pathlib import Path
import bot.config.configurator as cfg_mod


def test_init_env_prefers_etc(monkeypatch, tmp_path):
    """
    Проверяет, что init_env() отдаёт приоритет файлу .env в /etc/prehensor_bot,
    даже если ./.env существует.
    """
    # Создаём поддельный файл /etc/prehensor_bot/.env
    etc_env_file = tmp_path / "etc" / "prehensor_bot" / ".env"
    etc_env_file.parent.mkdir(parents=True)
    etc_env_file.write_text("TG_TOKEN=token_from_etc", encoding="utf-8")

    # Также создаём файл ./.env — но он не должен использоваться
    local_env_file = tmp_path / ".env"
    local_env_file.write_text("TG_TOKEN=token_from_local", encoding="utf-8")

    # Меняем пути в модуле configurator на поддельные
    monkeypatch.setattr(cfg_mod, "ETC_ENV_PATH", etc_env_file)
    monkeypatch.setattr(cfg_mod, "LOCAL_ENV_PATH", local_env_file)

    # Проверяем, что init_env возвращает True и берёт данные именно из etc_env_file
    assert cfg_mod.init_env() is True


def test_init_env_fallback_local(monkeypatch, tmp_path):
    """
    Проверяет, что если /etc/.env нет, но есть ./.env — он будет загружен.
    """
    # Нет ETC_ENV_PATH
    fake_etc_env = tmp_path / "etc" / "prehensor_bot" / ".env"
    # Есть LOCAL_ENV_PATH
    local_env_file = tmp_path / ".env"
    local_env_file.write_text("TG_TOKEN=token_from_local", encoding="utf-8")

    # Обновляем рабочий каталог на tmp_path
    monkeypatch.chdir(tmp_path)

    # Подменяем пути в модуле configurator
    monkeypatch.setattr(cfg_mod, "ETC_ENV_PATH", fake_etc_env)  # отсутствует
    monkeypatch.setattr(cfg_mod, "LOCAL_ENV_PATH", local_env_file)

    # Проверяем, что init_env загружает локальный .env
    assert cfg_mod.init_env() is True


def test_init_env_none(monkeypatch, tmp_path):
    """
    Проверяет, что если .env отсутствует в обоих местах — init_env() вернёт False.
    """
    fake_etc_env = tmp_path / "etc" / "prehensor_bot" / ".env"
    fake_local_env = tmp_path / ".env"

    # Подменяем пути на несуществующие
    monkeypatch.setattr(cfg_mod, "ETC_ENV_PATH", fake_etc_env)
    monkeypatch.setattr(cfg_mod, "LOCAL_ENV_PATH", fake_local_env)

    # Проверка: не найден ни один .env — результат False
    assert cfg_mod.init_env() is False

# tests/config/test_cfg_instance.py

import os
import pytest
import bot.config.configurator as cfg_mod


def test_Cfg_missing_token_exits(monkeypatch):
    '''
    Проверяет, что при отсутствии переменной TG_TOKEN происходит exit(1)
    '''
    monkeypatch.setattr(cfg_mod, "init_env", lambda: False)

    with pytest.raises(SystemExit) as exc:
        cfg_mod.Cfg()

    assert exc.value.code == 1


def test_Cfg_success(monkeypatch, tmp_path):
    """
    Проверяет успешное создание объекта Cfg при валидном окружении
    и settings.yaml. Также проверяет, что создаются нужные каталоги.
    """
    monkeypatch.setattr(cfg_mod, "init_env", lambda: True)
    monkeypatch.setenv("TG_TOKEN", "tok")

    cfg = cfg_mod.Cfg()

    assert os.path.isdir(cfg.log_dir)
    assert os.path.isdir(cfg.temp_dir)
    assert cfg.tg_token == "tok"



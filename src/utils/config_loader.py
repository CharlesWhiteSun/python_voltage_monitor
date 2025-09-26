import os
import yaml
from enum import Enum
from typing import Any, Dict, Union


def load_config(name: Union[str, Enum]) -> Dict[str, Any]:
    """
    讀取 YAML 設定檔
    :param name: 設定檔名稱 (不含副檔名，例如 'plc')
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    config_path = os.path.join(project_root, "configs", f"{name}.yml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

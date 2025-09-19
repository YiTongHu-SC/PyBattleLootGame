"""
配置管理模块
从YAML配置文件加载游戏设置
"""

import yaml
import os
from typing import Dict, Any, List, Optional


class GameConfig:
    """游戏配置管理器 - 支持YAML格式"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径，如果为None则使用默认路径
        """
        if config_path is None:
            # 默认配置文件路径
            project_root = os.path.dirname(os.path.dirname(__file__))
            config_path = os.path.join(project_root, "config", "game_config.yaml")

        self.config_path = config_path
        self.config = {}
        self.load_config()

    def load_config(self):
        """加载YAML配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = yaml.safe_load(f) or {}
            else:
                # 如果配置文件不存在，使用默认配置
                self._create_default_config()
        except Exception as e:
            print(f"警告: 加载配置文件失败 ({e})，使用默认设置")
            self._create_default_config()

    def _create_default_config(self):
        """创建默认配置"""
        self.config = {
            "battle": {
                "max_rounds": 50,
                "critical_hit_chance": 0.1,
                "critical_hit_multiplier": 1.5,
                "damage_variance_min": 0.8,
                "damage_variance_max": 1.2,
            },
            "display": {
                "health_bar_length": 20,
                "auto_advance_battle": False,
                "battle_delay_seconds": 1,
            },
        }

    def get_battle_config(self) -> Dict[str, Any]:
        """获取战斗配置"""
        battle_config = self.config.get("battle", {})
        return {
            "max_rounds": battle_config.get("max_rounds", 50),
            "critical_hit_chance": battle_config.get("critical_hit_chance", 0.1),
            "critical_hit_multiplier": battle_config.get(
                "critical_hit_multiplier", 1.5
            ),
            "damage_variance_min": battle_config.get("damage_variance_min", 0.8),
            "damage_variance_max": battle_config.get("damage_variance_max", 1.2),
        }

    def get_display_config(self) -> Dict[str, Any]:
        """获取显示配置"""
        display_config = self.config.get("display", {})
        return {
            "health_bar_length": display_config.get("health_bar_length", 20),
            "auto_advance_battle": display_config.get("auto_advance_battle", False),
            "battle_delay_seconds": display_config.get("battle_delay_seconds", 1),
        }

    def save_config(self):
        """保存配置到YAML文件"""
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(
                    self.config,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    indent=2,
                )
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def get_config_value(self, section: str, key: str, default=None):
        """获取特定配置值"""
        try:
            section_data = self.config.get(section, {})
            if isinstance(section_data, dict):
                return section_data.get(key, default)
            else:
                return default
        except Exception:
            return default

    def set_config_value(self, section: str, key: str, value: Any):
        """设置特定配置值"""
        if section not in self.config:
            self.config[section] = {}

        if isinstance(self.config[section], dict):
            self.config[section][key] = value
        else:
            self.config[section] = {key: value}

    def get_game_info(self) -> str:
        """从YAML配置文件获取游戏说明信息"""
        try:
            # 游戏说明配置文件路径
            project_root = os.path.dirname(os.path.dirname(__file__))
            info_config_path = os.path.join(project_root, "config", "game_info.yaml")

            if os.path.exists(info_config_path):
                with open(info_config_path, "r", encoding="utf-8") as f:
                    info_config = yaml.safe_load(f) or {}

                game_info = info_config.get("game_info", {})
                content = game_info.get("content", "")
                if content:
                    return content

            # 文件读取失败
            return "警告：文件读取失败"

        except Exception as e:
            return "警告：文件读取失败"


# 全局配置实例
game_config = GameConfig()

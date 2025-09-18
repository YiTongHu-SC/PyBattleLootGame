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
            config_path = os.path.join(project_root, 'config', 'game_config.yaml')
        
        self.config_path = config_path
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """加载YAML配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
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
            'battle': {
                'max_rounds': 50,
                'critical_hit_chance': 0.1,
                'critical_hit_multiplier': 1.5,
                'damage_variance_min': 0.8,
                'damage_variance_max': 1.2
            },
            'display': {
                'health_bar_length': 20,
                'auto_advance_battle': False,
                'battle_delay_seconds': 1
            },
            'characters': [
                {'name': '剑士', 'health': 100, 'attack': 25, 'defense': 8},
                {'name': '法师', 'health': 80, 'attack': 35, 'defense': 5},
                {'name': '弓箭手', 'health': 90, 'attack': 30, 'defense': 6},
                {'name': '盾卫', 'health': 120, 'attack': 20, 'defense': 12},
                {'name': '刺客', 'health': 70, 'attack': 40, 'defense': 4},
                {'name': '圣骑士', 'health': 110, 'attack': 22, 'defense': 10}
            ]
        }
    
    def get_battle_config(self) -> Dict[str, Any]:
        """获取战斗配置"""
        battle_config = self.config.get('battle', {})
        return {
            'max_rounds': battle_config.get('max_rounds', 50),
            'critical_hit_chance': battle_config.get('critical_hit_chance', 0.1),
            'critical_hit_multiplier': battle_config.get('critical_hit_multiplier', 1.5),
            'damage_variance_min': battle_config.get('damage_variance_min', 0.8),
            'damage_variance_max': battle_config.get('damage_variance_max', 1.2)
        }
    
    def get_display_config(self) -> Dict[str, Any]:
        """获取显示配置"""
        display_config = self.config.get('display', {})
        return {
            'health_bar_length': display_config.get('health_bar_length', 20),
            'auto_advance_battle': display_config.get('auto_advance_battle', False),
            'battle_delay_seconds': display_config.get('battle_delay_seconds', 1)
        }
    
    def get_character_presets(self) -> List[Dict[str, Any]]:
        """获取预设角色列表"""
        characters = self.config.get('characters', [])
        
        # 确保每个角色都有必要的字段
        validated_characters = []
        for char in characters:
            if isinstance(char, dict) and all(key in char for key in ['name', 'health', 'attack', 'defense']):
                validated_characters.append({
                    'name': char['name'],
                    'health': int(char['health']),
                    'attack': int(char['attack']),
                    'defense': int(char['defense'])
                })
            else:
                print(f"警告: 角色配置格式错误，跳过: {char}")
        
        return validated_characters
    
    def save_config(self):
        """保存配置到YAML文件"""
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True, indent=2)
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
            info_config_path = os.path.join(project_root, 'config', 'game_info.yaml')
            
            if os.path.exists(info_config_path):
                with open(info_config_path, 'r', encoding='utf-8') as f:
                    info_config = yaml.safe_load(f) or {}
                
                game_info = info_config.get('game_info', {})
                content = game_info.get('content', '')
                if content:
                    return content
            
            # 如果文件不存在或读取失败，返回默认说明
            return self._get_default_game_info()
            
        except Exception as e:
            print(f"警告: 读取游戏说明失败 ({e})，使用默认说明")
            return self._get_default_game_info()
    
    def _get_default_game_info(self) -> str:
        """获取默认游戏说明"""
        return """
    ╔══════════════════════════════════════════════════════════╗
    ║                      游戏说明                            ║
    ╚══════════════════════════════════════════════════════════╝
    
    🎮 游戏玩法:
    • 这是一个回合制1v1战斗模拟器
    • 选择你的角色，与对手进行战斗
    • 每回合角色会自动攻击对方
    • 战斗持续到有一方生命值归零
    
    ⚔️ 角色属性:
    • 生命值 (Health): 角色的血量，降到0时战败
    • 攻击力 (Attack): 决定造成伤害的基础数值
    • 防御力 (Defense): 减少承受的伤害
    
    🎯 战斗机制:
    • 攻击伤害 = 攻击力 × 随机倍数(0.8-1.2) - 目标防御力
    • 10%概率产生暴击，伤害提升50%
    • 每次攻击至少造成1点伤害
    
    🏆 胜利条件:
    • 将对手的生命值降到0
    • 或在50回合内保持更高的生命值
    """


# 全局配置实例
game_config = GameConfig()
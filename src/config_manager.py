"""
配置管理模块
从配置文件加载游戏设置
"""

import configparser
import os
from typing import Dict, Any, List, Optional


class GameConfig:
    """游戏配置管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认路径
        """
        if config_path is None:
            # 默认配置文件路径
            project_root = os.path.dirname(os.path.dirname(__file__))
            config_path = os.path.join(project_root, 'config', 'game_config.ini')
        
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                self.config.read(self.config_path, encoding='utf-8')
            else:
                # 如果配置文件不存在，使用默认配置
                self._create_default_config()
        except Exception as e:
            print(f"警告: 加载配置文件失败 ({e})，使用默认设置")
            self._create_default_config()
    
    def _create_default_config(self):
        """创建默认配置"""
        self.config.add_section('battle')
        self.config.set('battle', 'max_rounds', '50')
        self.config.set('battle', 'critical_hit_chance', '0.1')
        self.config.set('battle', 'critical_hit_multiplier', '1.5')
        self.config.set('battle', 'damage_variance_min', '0.8')
        self.config.set('battle', 'damage_variance_max', '1.2')
        
        self.config.add_section('display')
        self.config.set('display', 'health_bar_length', '20')
        self.config.set('display', 'auto_advance_battle', 'false')
        self.config.set('display', 'battle_delay_seconds', '1')
        
        self.config.add_section('characters')
        self.config.set('characters', '剑士', '100,25,8')
        self.config.set('characters', '法师', '80,35,5')
        self.config.set('characters', '弓箭手', '90,30,6')
        self.config.set('characters', '盾卫', '120,20,12')
        self.config.set('characters', '刺客', '70,40,4')
        self.config.set('characters', '圣骑士', '110,22,10')
    
    def get_battle_config(self) -> Dict[str, Any]:
        """获取战斗配置"""
        return {
            'max_rounds': self.config.getint('battle', 'max_rounds'),
            'critical_hit_chance': self.config.getfloat('battle', 'critical_hit_chance'),
            'critical_hit_multiplier': self.config.getfloat('battle', 'critical_hit_multiplier'),
            'damage_variance_min': self.config.getfloat('battle', 'damage_variance_min'),
            'damage_variance_max': self.config.getfloat('battle', 'damage_variance_max')
        }
    
    def get_display_config(self) -> Dict[str, Any]:
        """获取显示配置"""
        return {
            'health_bar_length': self.config.getint('display', 'health_bar_length'),
            'auto_advance_battle': self.config.getboolean('display', 'auto_advance_battle'),
            'battle_delay_seconds': self.config.getfloat('display', 'battle_delay_seconds')
        }
    
    def get_character_presets(self) -> List[Dict[str, Any]]:
        """获取预设角色列表"""
        characters = []
        
        for name in self.config.options('characters'):
            try:
                values = self.config.get('characters', name).split(',')
                health, attack, defense = map(int, values)
                
                characters.append({
                    'name': name,
                    'health': health,
                    'attack': attack,
                    'defense': defense
                })
            except (ValueError, IndexError) as e:
                print(f"警告: 角色 '{name}' 配置格式错误，跳过 ({e})")
                continue
        
        return characters
    
    def save_config(self):
        """保存配置到文件"""
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_config_value(self, section: str, key: str, default=None):
        """获取特定配置值"""
        try:
            if self.config.has_option(section, key):
                return self.config.get(section, key)
            else:
                return default
        except Exception:
            return default
    
    def set_config_value(self, section: str, key: str, value: str):
        """设置特定配置值"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        self.config.set(section, key, value)


# 全局配置实例
game_config = GameConfig()
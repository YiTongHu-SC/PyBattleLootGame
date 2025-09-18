"""
角色生成器 - 生成随机角色名称和属性
"""

import json
import random
import os
from typing import Dict, List, Optional


class CharacterNameGenerator:
    """角色名称生成器"""
    
    def __init__(self, data_file_path: Optional[str] = None):
        """
        初始化角色名称生成器
        
        Args:
            data_file_path: character_names.json 文件路径，如果为None则使用默认路径
        """
        if data_file_path is None:
            # 默认路径：从src目录向上查找data目录
            current_dir = os.path.dirname(__file__)
            project_root = os.path.dirname(current_dir)
            data_file_path = os.path.join(project_root, "data", "character_names.json")
        
        self.data_file_path = data_file_path
        self._character_names: List[str] = []
        self._load_names()
    
    def _load_names(self) -> None:
        """从JSON文件加载角色名称列表"""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._character_names = data.get('character_names', [])
            
            if not self._character_names:
                raise ValueError("角色名称列表为空")
                
            print(f"✅ 成功加载 {len(self._character_names)} 个角色名称")
            
        except FileNotFoundError:
            print(f"❌ 找不到角色名称配置文件: {self.data_file_path}")
            # 提供默认名称作为备选
            self._character_names = [
                "神秘战士",
                "勇敢冒险家", 
                "暗影刺客",
                "圣光骑士",
                "元素法师"
            ]
            print("🔄 使用默认角色名称列表")
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON配置文件格式错误: {e}")
            self._character_names = ["未命名角色"]
            
        except Exception as e:
            print(f"❌ 加载角色名称时发生错误: {e}")
            self._character_names = ["错误角色"]
    
    def get_random_name(self) -> str:
        """
        随机获取一个角色名称
        
        Returns:
            str: 随机角色名称
        """
        if not self._character_names:
            return "无名角色"
        
        return random.choice(self._character_names)
    
    def get_all_names(self) -> List[str]:
        """
        获取所有可用的角色名称
        
        Returns:
            List[str]: 所有角色名称列表
        """
        return self._character_names.copy()
    
    def get_random_names(self, count: int, allow_duplicates: bool = False) -> List[str]:
        """
        获取多个随机角色名称
        
        Args:
            count: 需要获取的名称数量
            allow_duplicates: 是否允许重复名称
        
        Returns:
            List[str]: 随机角色名称列表
        """
        if not self._character_names:
            return ["无名角色"] * count
        
        if allow_duplicates or count <= len(self._character_names):
            if allow_duplicates:
                return [random.choice(self._character_names) for _ in range(count)]
            else:
                return random.sample(self._character_names, min(count, len(self._character_names)))
        else:
            # 如果需要的数量超过可用名称且不允许重复，则返回所有名称
            return self._character_names.copy()
    
    def reload_names(self) -> None:
        """重新加载角色名称配置"""
        self._load_names()
    
    def get_names_count(self) -> int:
        """获取可用角色名称的数量"""
        return len(self._character_names)


# 创建全局实例，方便在其他模块中使用
character_name_generator = CharacterNameGenerator()


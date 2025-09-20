"""
角色生成器 - 生成随机角色名称和属性
"""

import json
import random
import os
from typing import Dict, List, Optional, Any
from .resource_path import get_resource_path


class CharacterDataLoader:
    """角色数据加载器 - 专门处理角色预制数据"""

    def __init__(self, data_file_path: Optional[str] = None):
        """
        初始化角色数据加载器

        Args:
            data_file_path: character_data.json 文件路径，如果为None则使用默认路径
        """
        if data_file_path is None:
            # 使用资源路径处理函数获取数据文件路径
            data_file_path = get_resource_path("data/character_data.json")

        self.data_file_path = data_file_path
        self._character_presets: List[Dict[str, Any]] = []
        self.all_load_success = True
        self._load_character_data()

    def _load_character_data(self) -> None:
        """从JSON文件加载角色预制数据"""
        try:
            with open(self.data_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._character_presets = data.get("character_presets", [])

            if not self._character_presets:
                self.all_load_success = False
                raise ValueError("角色预制数据为空")

            # 验证每个角色数据的完整性
            validated_presets = []
            for char in self._character_presets:
                if isinstance(char, dict) and all(
                    key in char for key in ["class", "health", "attack", "defense"]
                ):
                    validated_presets.append(
                        {
                            "class": str(char["class"]),
                            "health": int(char["health"]),
                            "attack": int(char["attack"]),
                            "defense": int(char["defense"]),
                        }
                    )
                else:
                    print(f"⚠️ 角色数据格式错误，跳过: {char}")

            self._character_presets = validated_presets
            print(f"✅ 成功加载 {len(self._character_presets)} 个角色预制数据")

        except FileNotFoundError:
            self.all_load_success = False
            print(f"❌ 找不到角色数据配置文件: {self.data_file_path}")
            # 提供默认角色数据作为备选
            self._character_presets = [
                {"class": "剑士", "health": 100, "attack": 25, "defense": 8},
                {"class": "法师", "health": 80, "attack": 35, "defense": 5},
                {"class": "弓箭手", "health": 90, "attack": 30, "defense": 6},
                {"class": "盾卫", "health": 120, "attack": 20, "defense": 12},
                {"class": "刺客", "health": 70, "attack": 40, "defense": 4},
                {"class": "圣骑士", "health": 110, "attack": 22, "defense": 10},
            ]
            print("🔄 使用默认角色数据")

        except json.JSONDecodeError as e:
            self.all_load_success = False
            print(f"❌ JSON配置文件格式错误: {e}")

        except Exception as e:
            self.all_load_success = False
            print(f"❌ 加载角色数据时发生错误: {e}")

    def get_character_presets(self) -> List[Dict[str, Any]]:
        """
        获取所有角色预制数据

        Returns:
            List[Dict]: 角色预制数据列表，每个字典包含 name, health, attack, defense
        """
        return self._character_presets.copy()

    def get_random_character(self) -> Dict[str, Any]:
        """
        随机获取一个角色预制数据

        Returns:
            Dict: 随机角色数据
        """
        if not self._character_presets:
            return dict()

        return random.choice(self._character_presets).copy()

    def get_character_by_class(self, class_name: str) -> Optional[Dict[str, Any]]:
        """
        根据职业获取特定角色数据

        Args:
            class_name: 角色职业名称

        Returns:
            Dict or None: 找到的角色数据，如果未找到则返回None
        """
        for char in self._character_presets:
            if char["class"] == class_name:
                return char.copy()
        return None

    def get_character_classes(self) -> List[str]:
        """
        获取所有角色职业列表

        Returns:
            List[str]: 角色职业列表
        """
        return [char["class"] for char in self._character_presets]

    def get_characters_count(self) -> int:
        """获取可用角色数量"""
        return len(self._character_presets)

    def reload_character_data(self) -> None:
        """重新加载角色数据"""
        self._load_character_data()


class CharacterNameGenerator:
    """角色名称生成器"""

    def __init__(self, data_file_path: Optional[str] = None):
        """
        初始化角色名称生成器

        Args:
            data_file_path: character_names.json 文件路径，如果为None则使用默认路径
        """
        if data_file_path is None:
            # 使用资源路径处理函数获取数据文件路径
            data_file_path = get_resource_path("data/character_names.json")

        self.data_file_path = data_file_path
        self._character_names: List[str] = []
        self.all_load_success = True
        self._load_names()

    def _load_names(self) -> None:
        """从JSON文件加载角色名称列表"""
        try:
            with open(self.data_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._character_names = data.get("character_names", [])

            if not self._character_names:
                raise ValueError("角色名称列表为空")

            print(f"✅ 成功加载 {len(self._character_names)} 个角色名称")

        except FileNotFoundError:
            self.all_load_success = False
            print(f"❌ 找不到角色名称配置文件: {self.data_file_path}")
            # 提供默认名称作为备选
            self._character_names = [
                "神秘战士",
                "勇敢冒险家",
                "暗影刺客",
                "圣光骑士",
                "元素法师",
            ]
            print("🔄 使用默认角色名称列表")

        except json.JSONDecodeError as e:
            self.all_load_success = False
            print(f"❌ JSON配置文件格式错误: {e}")
            self._character_names = ["未命名角色"]

        except Exception as e:
            self.all_load_success = False
            print(f"❌ 加载角色名称时发生错误: {e}")
            self._character_names = ["错误角色"]

    def get_random_name(self, except_name: str = "") -> str:
        """
        随机获取一个角色名称
        
        except_name: 如果生成的名称与此名称相同，则重新生成
        
        return: 随机角色名称
        """
        if not self._character_names:
            return "无名角色"
        temp_name = random.choice(self._character_names)
        if except_name == temp_name:
            return self.get_random_name(except_name)
        return temp_name

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
                return random.sample(
                    self._character_names, min(count, len(self._character_names))
                )
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
character_data_loader = CharacterDataLoader()

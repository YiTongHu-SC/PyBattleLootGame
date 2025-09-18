"""
测试角色名称生成器功能
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

from src import character_name_generator, CharacterNameGenerator


def test_character_name_generator():
    """测试角色名称生成器"""
    print("=== 角色名称生成器测试 ===\n")
    
    # 测试1: 获取随机名称
    print("1. 测试随机名称生成:")
    for i in range(5):
        name = character_name_generator.get_random_name()
        print(f"   随机名称 {i+1}: {name}")
    
    # 测试2: 获取所有名称
    print(f"\n2. 所有可用名称 (共{character_name_generator.get_names_count()}个):")
    all_names = character_name_generator.get_all_names()
    for i, name in enumerate(all_names, 1):
        print(f"   {i:2d}. {name}")
    
    # 测试3: 获取多个不重复的随机名称
    print(f"\n3. 获取3个不重复的随机名称:")
    multiple_names = character_name_generator.get_random_names(3, allow_duplicates=False)
    for i, name in enumerate(multiple_names, 1):
        print(f"   {i}. {name}")
    
    # 测试4: 获取多个可重复的随机名称
    print(f"\n4. 获取5个可重复的随机名称:")
    duplicate_names = character_name_generator.get_random_names(5, allow_duplicates=True)
    for i, name in enumerate(duplicate_names, 1):
        print(f"   {i}. {name}")
    
    # 测试5: 创建自定义实例
    print(f"\n5. 测试自定义实例 (使用相同配置文件):")
    custom_generator = CharacterNameGenerator()
    custom_name = custom_generator.get_random_name()
    print(f"   自定义生成器随机名称: {custom_name}")


if __name__ == "__main__":
    test_character_name_generator()
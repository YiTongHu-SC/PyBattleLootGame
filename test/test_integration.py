"""
简单测试新功能
"""
import sys
import os
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

# 测试导入
print("测试导入...")
from src import character_name_generator

# 测试基本功能
print("✅ 导入成功！")
print(f"随机角色名称: {character_name_generator.get_random_name()}")
print(f"可用名称数量: {character_name_generator.get_names_count()}")

print("\n功能集成完成！新功能包括:")
print("1. CharacterNameGenerator 类")
print("2. 全局实例 character_name_generator")
print("3. 主程序新增'随机角色名称生成器'选项")
print("4. 角色选择时可以使用随机名称")
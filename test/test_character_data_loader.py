"""
测试新的角色数据加载系统
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(__file__)
sys.path.insert(0, project_root)

from src import character_data_loader, CharacterDataLoader


def test_character_data_loader():
    """测试角色数据加载器"""
    print("=== 角色数据加载器测试 ===\n")
    
    # 测试1: 获取所有角色预制数据
    print("1. 测试获取所有角色预制数据:")
    all_characters = character_data_loader.get_character_presets()
    print(f"   共加载 {len(all_characters)} 个角色:")
    for i, char in enumerate(all_characters, 1):
        print(f"   {i:2d}. {char['name']:8} | 生命值:{char['health']:3} | 攻击力:{char['attack']:2} | 防御力:{char['defense']:2}")
    
    # 测试2: 获取随机角色
    print(f"\n2. 测试随机角色获取:")
    for i in range(3):
        random_char = character_data_loader.get_random_character()
        print(f"   随机角色 {i+1}: {random_char}")
    
    # 测试3: 根据名称获取角色
    print(f"\n3. 测试根据名称获取角色:")
    target_names = ["剑士", "法师", "不存在的角色"]
    for name in target_names:
        char = character_data_loader.get_character_by_name(name)
        if char:
            print(f"   找到角色 '{name}': {char}")
        else:
            print(f"   未找到角色 '{name}'")
    
    # 测试4: 获取角色名称列表
    print(f"\n4. 测试角色名称列表:")
    names = character_data_loader.get_character_names()
    print(f"   所有角色名称: {names}")
    
    # 测试5: 统计信息
    print(f"\n5. 测试统计信息:")
    print(f"   角色数量: {character_data_loader.get_characters_count()}")
    
    # 测试6: 创建自定义实例
    print(f"\n6. 测试自定义实例:")
    custom_loader = CharacterDataLoader()
    custom_char = custom_loader.get_random_character()
    print(f"   自定义加载器随机角色: {custom_char}")


def test_integration():
    """测试与主程序的集成"""
    print("\n" + "=" * 50)
    print("=== 主程序集成测试 ===\n")
    
    # 模拟主程序的角色创建流程
    print("模拟主程序角色创建流程:")
    characters = character_data_loader.get_character_presets()
    print(f"1. 加载角色预制数据: 成功加载 {len(characters)} 个角色")
    
    if characters:
        char_data = characters[0]
        print(f"2. 选择第一个角色: {char_data}")
        
        # 模拟创建玩家对象（不实际导入Player类，只打印信息）
        player_name = f"玩家({char_data['name']})"
        print(f"3. 创建玩家: {player_name}")
        print(f"   - 生命值: {char_data['health']}")
        print(f"   - 攻击力: {char_data['attack']}")
        print(f"   - 防御力: {char_data['defense']}")


if __name__ == "__main__":
    test_character_data_loader()
    test_integration()
    
    print(f"\n✅ 所有测试完成！")
    print(f"📋 重构总结:")
    print(f"   - 创建了 character_data.json 独立的角色数据文件")
    print(f"   - 实现了 CharacterDataLoader 专门的角色数据加载类")
    print(f"   - 从 GameConfig 中移除了角色相关功能")
    print(f"   - 更新了主程序使用新的数据加载方式")
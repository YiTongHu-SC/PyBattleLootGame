"""
测试YAML配置文件功能
"""

import sys
import os
import yaml

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.config_manager import game_config


def test_yaml_config_files_exist():
    """测试YAML配置文件是否存在"""
    print("测试YAML配置文件存在性...")
    
    project_root = os.path.dirname(__file__)
    
    # 检查游戏说明YAML配置文件
    game_info_path = os.path.join(project_root, 'config', 'game_info.yaml')
    assert os.path.exists(game_info_path), f"游戏说明YAML配置文件不存在: {game_info_path}"
    
    # 检查主YAML配置文件
    game_config_path = os.path.join(project_root, 'config', 'game_config.yaml')
    assert os.path.exists(game_config_path), f"主YAML配置文件不存在: {game_config_path}"
    
    print("✅ YAML配置文件存在性测试通过")


def test_yaml_config_parsing():
    """测试YAML配置解析"""
    print("测试YAML配置解析...")
    
    # 测试战斗配置
    battle_config = game_config.get_battle_config()
    assert 'max_rounds' in battle_config, "战斗配置缺少max_rounds"
    assert 'critical_hit_chance' in battle_config, "战斗配置缺少critical_hit_chance"
    assert battle_config['max_rounds'] == 50, f"max_rounds应该是50，实际是{battle_config['max_rounds']}"
    
    # 测试显示配置
    display_config = game_config.get_display_config()
    assert 'health_bar_length' in display_config, "显示配置缺少health_bar_length"
    assert display_config['health_bar_length'] == 20, f"health_bar_length应该是20，实际是{display_config['health_bar_length']}"
    
    # 测试角色配置
    characters = game_config.get_character_presets()
    assert len(characters) >= 6, f"角色数量应该至少6个，实际是{len(characters)}个"
    
    # 验证角色数据结构
    for char in characters:
        assert 'name' in char, f"角色配置缺少name字段: {char}"
        assert 'health' in char, f"角色配置缺少health字段: {char}"
        assert 'attack' in char, f"角色配置缺少attack字段: {char}"
        assert 'defense' in char, f"角色配置缺少defense字段: {char}"
    
    print("✅ YAML配置解析测试通过")


def test_yaml_game_info():
    """测试YAML游戏说明配置"""
    print("测试YAML游戏说明配置...")
    
    game_info = game_config.get_game_info()
    
    # 验证内容是否包含关键信息
    assert "游戏说明" in game_info, "游戏说明标题缺失"
    assert "游戏玩法" in game_info, "游戏玩法部分缺失"
    assert "角色属性" in game_info, "角色属性部分缺失"
    assert "战斗机制" in game_info, "战斗机制部分缺失"
    assert "胜利条件" in game_info, "胜利条件部分缺失"
    
    # 检查没有解析错误（不应该包含双百分号）
    assert "%%" not in game_info, "游戏说明包含未处理的转义字符"
    
    print("✅ YAML游戏说明配置测试通过")
    print(f"游戏说明内容长度: {len(game_info)} 字符")


def test_yaml_structure():
    """测试YAML文件结构的有效性"""
    print("测试YAML文件结构...")
    
    project_root = os.path.dirname(__file__)
    
    # 测试主配置文件的YAML结构
    config_path = os.path.join(project_root, 'config', 'game_config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    assert isinstance(config_data, dict), "主配置文件应该是字典结构"
    assert 'battle' in config_data, "主配置文件缺少battle部分"
    assert 'display' in config_data, "主配置文件缺少display部分"
    assert 'characters' in config_data, "主配置文件缺少characters部分"
    assert isinstance(config_data['characters'], list), "characters应该是列表结构"
    
    # 测试游戏说明文件的YAML结构
    info_path = os.path.join(project_root, 'config', 'game_info.yaml')
    with open(info_path, 'r', encoding='utf-8') as f:
        info_data = yaml.safe_load(f)
    
    assert isinstance(info_data, dict), "游戏说明文件应该是字典结构"
    assert 'game_info' in info_data, "游戏说明文件缺少game_info部分"
    assert 'content' in info_data['game_info'], "游戏说明文件缺少content部分"
    
    print("✅ YAML文件结构测试通过")


if __name__ == "__main__":
    try:
        test_yaml_config_files_exist()
        test_yaml_structure()
        test_yaml_config_parsing()
        test_yaml_game_info()
        
        print("\n🎉 所有YAML配置测试都通过了！")
        
        print("\n📁 从INI到YAML的迁移完成:")
        print("  ✅ 创建了 config/game_config.yaml - YAML格式的主配置文件")
        print("  ✅ 创建了 config/game_info.yaml - YAML格式的游戏说明文件")
        print("  ✅ 更新了 src/config_manager.py - 完全支持YAML格式")
        print("  ✅ 安装了 PyYAML 依赖")
        print("  ✅ 更新了 main.py - 角色数据从YAML配置读取")
        
        print("\n🔧 YAML配置的优势:")
        print("  • 更清晰易读的格式")
        print("  • 支持复杂的数据结构（列表、嵌套字典）")
        print("  • 不需要处理特殊字符转义问题")
        print("  • 更好的注释支持")
        print("  • 更适合版本控制")
        
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        sys.exit(1)
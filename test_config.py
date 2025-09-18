"""
测试游戏配置文件功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.config_manager import game_config


def test_game_info():
    """测试游戏说明配置读取"""
    print("测试游戏说明配置读取...")
    
    # 获取游戏说明
    game_info = game_config.get_game_info()
    
    # 验证内容是否包含关键信息
    assert "游戏说明" in game_info, "游戏说明标题缺失"
    assert "游戏玩法" in game_info, "游戏玩法部分缺失"
    assert "角色属性" in game_info, "角色属性部分缺失"
    assert "战斗机制" in game_info, "战斗机制部分缺失"
    assert "胜利条件" in game_info, "胜利条件部分缺失"
    
    print("✅ 游戏说明配置测试通过")
    print(f"游戏说明内容长度: {len(game_info)} 字符")


def test_config_files_exist():
    """测试配置文件是否存在"""
    print("测试配置文件存在性...")
    
    project_root = os.path.dirname(__file__)
    
    # 检查游戏说明配置文件
    game_info_path = os.path.join(project_root, 'config', 'game_info.ini')
    assert os.path.exists(game_info_path), f"游戏说明配置文件不存在: {game_info_path}"
    
    # 检查主配置文件
    game_config_path = os.path.join(project_root, 'config', 'game_config.ini')
    assert os.path.exists(game_config_path), f"主配置文件不存在: {game_config_path}"
    
    print("✅ 配置文件存在性测试通过")


if __name__ == "__main__":
    try:
        test_config_files_exist()
        test_game_info()
        print("\n🎉 所有测试都通过了！游戏说明已成功移动到配置文件中。")
        
        print("\n📁 文件结构变更:")
        print("  ✅ 创建了 config/game_info.ini - 存储游戏说明")
        print("  ✅ 更新了 src/config_manager.py - 添加了 get_game_info() 方法")
        print("  ✅ 更新了 main.py - show_game_info() 现在从配置文件读取内容")
        
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 运行错误: {e}")
        sys.exit(1)
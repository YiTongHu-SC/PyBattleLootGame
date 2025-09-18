"""
快速测试脚本 - 验证战斗系统核心功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.player import Player
from src.battle import Battle


def test_basic_functionality():
    """测试基本功能"""
    print("🧪 开始测试战斗系统...")
    
    # 创建两个测试角色
    player1 = Player("测试剑士", health=100, attack=25, defense=8)
    player2 = Player("测试法师", health=80, attack=35, defense=5)
    
    print(f"✅ 成功创建角色:")
    print(f"   {player1.name}: {player1.current_health}HP, {player1.attack}攻击, {player1.defense}防御")
    print(f"   {player2.name}: {player2.current_health}HP, {player2.attack}攻击, {player2.defense}防御")
    
    # 测试攻击功能
    print(f"\n🗡️  测试攻击功能...")
    attack_result = player1.attack_target(player2)
    print(f"   {attack_result['attacker']} 攻击 {attack_result['target']}")
    print(f"   造成 {attack_result['actual_damage']} 点伤害")
    print(f"   {attack_result['target']} 剩余血量: {attack_result['target_health']}")
    
    # 测试战斗类
    print(f"\n⚔️  测试战斗系统...")
    # 重新创建角色以确保满血
    player1 = Player("测试剑士", health=100, attack=25, defense=8)
    player2 = Player("测试法师", health=80, attack=35, defense=5)
    
    battle = Battle(player1, player2)
    
    # 执行几个回合
    for i in range(3):
        round_result = battle.execute_round()
        print(f"   第{round_result['round']}回合: {len(round_result['actions'])} 个行动")
        
        if battle.battle_ended:
            winner_name = battle.winner.name if battle.winner else "无"
            print(f"   战斗结束! 胜者: {winner_name}")
            break
    
    print(f"\n📊 测试完成!")
    print(f"   {player1.name}: {player1.current_health}/{player1.max_health} HP")
    print(f"   {player2.name}: {player2.current_health}/{player2.max_health} HP")
    
    return True


def test_config_system():
    """测试配置系统"""
    print(f"\n🔧 测试配置系统...")
    
    try:
        from src.config_manager import game_config
        
        battle_config = game_config.get_battle_config()
        display_config = game_config.get_display_config()
        characters = game_config.get_character_presets()
        
        print(f"   ✅ 战斗配置加载成功: {len(battle_config)} 项设置")
        print(f"   ✅ 显示配置加载成功: {len(display_config)} 项设置")
        print(f"   ✅ 角色预设加载成功: {len(characters)} 个角色")
        
        return True
    except Exception as e:
        print(f"   ❌ 配置系统测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("="*60)
    print("       PyBattleLootGame 快速功能测试")
    print("="*60)
    
    success_count = 0
    total_tests = 2
    
    # 测试基本功能
    if test_basic_functionality():
        success_count += 1
    
    # 测试配置系统
    if test_config_system():
        success_count += 1
    
    print(f"\n" + "="*60)
    print(f"测试结果: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！战斗系统运行正常。")
        print("💡 你现在可以运行 'python main.py' 来开始游戏了！")
    else:
        print("⚠️  有测试失败，请检查代码。")
    
    print("="*60)


if __name__ == "__main__":
    main()
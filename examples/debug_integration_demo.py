#!/usr/bin/env python3
"""
调试工具集成示例
展示如何在 PyBattleLootGame 的各个组件中使用调试工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import (
    verbose, debug, info, critical,
    set_debug_environment, set_debug_level,
    Player, Battle, game_config
)


def demo_player_creation():
    """演示角色创建过程的调试输出"""
    print("\n=== 角色创建调试示例 ===")
    
    info("开始创建新角色")
    
    # 模拟角色数据验证
    name = "勇士小明"
    character_class = "战士"
    health = 100
    attack = 15
    defense = 8
    
    verbose("验证角色参数 - 姓名: %s, 职业: %s", name, character_class)
    verbose("属性检查 - 血量: %d, 攻击: %d, 防御: %d", health, attack, defense)
    
    if health <= 0:
        critical("角色创建失败: 血量不能为零或负数")
        return None
    
    if not name.strip():
        critical("角色创建失败: 姓名不能为空")
        return None
    
    debug("创建 %s 角色实例", character_class)
    player = Player(name, character_class, health, attack, defense)
    
    info("角色创建成功: %s (%s)", player.name, player.character_class)
    verbose("最终属性 - HP: %d/%d, ATK: %d, DEF: %d", 
            player.current_health, player.max_health, player.attack, player.defense)
    
    return player


def demo_battle_system():
    """演示战斗系统的调试输出"""
    print("\n=== 战斗系统调试示例 ===")
    
    # 创建两个角色
    player1 = Player("勇者", "战士", 100, 15, 8)
    player2 = Player("邪恶法师", "法师", 80, 18, 5)
    
    info("战斗初始化: %s vs %s", player1.name, player2.name)
    debug("P1属性 - HP:%d/%d ATK:%d DEF:%d", player1.current_health, player1.max_health, player1.attack, player1.defense)
    debug("P2属性 - HP:%d/%d ATK:%d DEF:%d", player2.current_health, player2.max_health, player2.attack, player2.defense)
    
    round_count = 0
    max_rounds = 5  # 限制演示回合数
    
    while player1.is_alive and player2.is_alive and round_count < max_rounds:
        round_count += 1
        info("--- 第 %d 回合 ---", round_count)
        
        verbose("回合开始状态 - %s: %d HP, %s: %d HP", 
                player1.name, player1.current_health, player2.name, player2.current_health)
        
        # P1攻击P2
        damage = max(1, player1.attack - player2.defense)
        player2.current_health -= damage
        player2.is_alive = player2.current_health > 0
        debug("%s 攻击 %s，造成 %d 伤害", player1.name, player2.name, damage)
        verbose("%s 剩余血量: %d", player2.name, max(0, player2.current_health))
        
        if not player2.is_alive:
            critical("战斗结束！%s 获得胜利！", player1.name)
            break
        
        # P2攻击P1
        damage = max(1, player2.attack - player1.defense)
        player1.current_health -= damage
        player1.is_alive = player1.current_health > 0
        debug("%s 攻击 %s，造成 %d 伤害", player2.name, player1.name, damage)
        verbose("%s 剩余血量: %d", player1.name, max(0, player1.current_health))
        
        if not player1.is_alive:
            critical("战斗结束！%s 获得胜利！", player2.name)
            break
    
    if round_count >= max_rounds:
        info("演示战斗达到最大回合数限制")


def demo_config_loading():
    """演示配置加载过程的调试输出"""
    print("\n=== 配置加载调试示例 ===")
    
    info("开始加载游戏配置")
    
    try:
        battle_config = game_config.get_battle_config()
        verbose("战斗配置加载成功")
        debug("最大回合数: %d", battle_config.get('max_rounds', 0))
        debug("暴击概率: %.2f", battle_config.get('critical_hit_chance', 0))
        debug("暴击倍率: %.2f", battle_config.get('critical_hit_multiplier', 0))
        
        display_config = game_config.get_display_config()
        verbose("显示配置加载成功")
        debug("血条长度: %d", display_config.get('health_bar_length', 0))
        debug("自动推进: %s", display_config.get('auto_advance_battle', False))
        debug("战斗延迟: %d秒", display_config.get('battle_delay_seconds', 0))
        
        info("所有配置加载完成")
        
    except Exception as e:
        critical("配置加载失败: %s", str(e))


def demo_environment_switching():
    """演示不同环境下的调试输出效果"""
    print("\n=== 环境切换演示 ===")
    
    environments = [
        ('development', '开发环境'),
        ('debug', '调试模式'),
        ('testing', '测试环境'),
        ('production', '生产环境')
    ]
    
    for env_key, env_name in environments:
        print(f"\n--- {env_name} ---")
        set_debug_environment(env_key)
        
        verbose("这是详细调试信息，通常用于开发阶段")
        debug("这是一般调试信息，用于调试问题")
        info("这是重要信息，记录关键操作")
        critical("这是关键信息，记录错误和重要事件")


def main():
    """主演示函数"""
    print("PyBattleLootGame 调试工具集成演示")
    print("=" * 50)
    
    # 设置为开发环境以显示所有调试信息
    set_debug_environment('development')
    
    # 演示各个组件的调试使用
    demo_player_creation()
    demo_battle_system()
    demo_config_loading()
    demo_environment_switching()
    
    print("\n" + "=" * 50)
    print("演示完成")
    
    print("\n提示：")
    print("- 在实际开发中，根据需要设置适当的环境和等级")
    print("- 生产环境建议只保留关键信息(CRITICAL)输出")
    print("- 调试信息可帮助快速定位问题和跟踪程序执行流程")


if __name__ == "__main__":
    main()
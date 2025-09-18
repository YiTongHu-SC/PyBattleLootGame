"""
PyBattleLootGame 主程序入口
运行1v1战斗模拟游戏
"""

import os
import sys
import random
import time
from typing import Tuple

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.player import Player
from src.battle import Battle
from src.config_manager import game_config


def clear_screen():
    """
    清屏函数 - 适用于VS Code集成终端
    使用ANSI转义序列避免调用系统命令，防止弹出额外的终端窗口
    """
    try:
        # 方法1: 使用ANSI转义序列清屏
        # \033[2J - 清除整个屏幕
        # \033[H - 将光标移动到左上角
        print("\033[2J\033[H", end="", flush=True)
    except Exception:
        # 方法2: 如果ANSI序列不支持，使用简单换行
        print("\n" * 50)


def display_title():
    """显示游戏标题"""
    title = """
    ╔══════════════════════════════════════════════════════════╗
    ║                 PyBattleLootGame                         ║
                        终端战斗模拟器                            
    ╚══════════════════════════════════════════════════════════╝
    """
    print(title)


def get_player_choice() -> str:
    """获取玩家选择"""
    time.sleep(0.2)
    while True:
        print("\n请选择操作:")
        print("1. 开始新的战斗")
        print("2. 查看游戏说明")
        print("3. 退出游戏")

        choice = input("\n请输入选项 (1-3): ").strip()

        if choice in ["1", "2", "3"]:
            return choice
        else:
            print("❌ 无效选择，请输入1、2或3")


def create_preset_characters() -> list:
    """创建预设角色"""
    characters = [
        {"name": "剑士", "health": 100, "attack": 25, "defense": 8},
        {"name": "法师", "health": 80, "attack": 35, "defense": 5},
        {"name": "弓箭手", "health": 90, "attack": 30, "defense": 6},
        {"name": "盾卫", "health": 120, "attack": 20, "defense": 12},
        {"name": "刺客", "health": 70, "attack": 40, "defense": 4},
        {"name": "圣骑士", "health": 110, "attack": 22, "defense": 10},
    ]
    return characters


def select_character(player_num: int, characters: list) -> Player:
    """让玩家选择角色"""
    print(f"\n玩家{player_num} 请选择你的角色:")
    print("-" * 50)

    for i, char in enumerate(characters, 1):
        print(
            f"{i}. {char['name']:8} | "
            f"生命值: {char['health']:3} | "
            f"攻击力: {char['attack']:2} | "
            f"防御力: {char['defense']:2}"
        )

    while True:
        try:
            choice = int(input(f"\n玩家{player_num} 选择角色 (1-{len(characters)}): "))
            if 1 <= choice <= len(characters):
                char_data = characters[choice - 1]
                player_name = f"玩家{player_num}({char_data['name']})"
                return Player(
                    name=player_name,
                    health=char_data["health"],
                    attack=char_data["attack"],
                    defense=char_data["defense"],
                )
            else:
                print(f"❌ 请输入1到{len(characters)}之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字")


def create_random_battle() -> Tuple[Player, Player]:
    """创建随机战斗"""
    characters = create_preset_characters()

    # 随机选择两个不同的角色
    char1_data = random.choice(characters)
    char2_data = random.choice(characters)

    player1 = Player(
        name=f"随机角色1({char1_data['name']})",
        health=char1_data["health"],
        attack=char1_data["attack"],
        defense=char1_data["defense"],
    )

    player2 = Player(
        name=f"随机角色2({char2_data['name']})",
        health=char2_data["health"],
        attack=char2_data["attack"],
        defense=char2_data["defense"],
    )

    return player1, player2


def start_battle():
    """开始战斗"""
    characters = create_preset_characters()

    print("\n" + "=" * 60)
    print("选择战斗模式:")
    print("1. 手动选择角色")
    print("2. 随机对战")

    while True:
        mode = input("\n请选择模式 (1-2): ").strip()
        if mode == "1":
            player1 = select_character(1, characters)
            player2 = select_character(2, characters)
            break
        elif mode == "2":
            player1, player2 = create_random_battle()
            print(f"\n🎲 随机匹配完成！")
            print(f"   {player1.name}")
            print(f"   VS")
            print(f"   {player2.name}")
            break
        else:
            print("❌ 请输入1或2")

    # 创建并开始战斗
    battle = Battle(player1, player2)
    battle_result = battle.fight_until_end()

    # 显示战斗摘要
    summary = battle.get_battle_summary()
    print(f"\n📊 战斗统计:")
    print(f"   {player1.name} 总伤害: {summary['player1_damage_dealt']}")
    print(f"   {player2.name} 总伤害: {summary['player2_damage_dealt']}")


def show_game_info():
    """显示游戏说明"""
    info = game_config.get_game_info()
    print(info)
    input("\n按回车键返回主菜单...")


def main():
    """主函数"""
    while True:
        time.sleep(0.2)
        clear_screen()
        display_title()

        choice = get_player_choice()

        if choice == "1":
            start_battle()
            input("\n按回车键返回主菜单...")

        elif choice == "2":
            clear_screen()
            show_game_info()

        elif choice == "3":
            print("\n👋 感谢游玩 PyBattleLootGame！")
            break


if __name__ == "__main__":
    main()

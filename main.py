"""
PyBattleLootGame 主程序入口
运行战斗模拟游戏
"""

import os
from datetime import datetime
import random
import time
from typing import Tuple

from src.dungeon_master import DungeonMaster

from src import (
    Player,
    Battle,
    game_config,
    character_name_generator,
    character_data_loader,
)

dungeon_master = DungeonMaster(game_config.game_info)


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


def get_player_choice() -> str:
    """获取玩家选择"""
    time.sleep(0.2)
    while True:
        dungeon_master.print_message("\n请选择操作:")
        dungeon_master.print_message("1. 开始新的战斗")
        dungeon_master.print_message("2. 查看游戏说明")
        dungeon_master.print_message("3. 退出游戏")

        choice = dungeon_master.input_prompt("请输入选项 (1-3): ")

        if choice in ["1", "2", "3"]:
            return choice
        else:
            dungeon_master.print_message("❌ 无效选择，请输入1、2或3")


def create_preset_characters() -> list:
    """创建预设角色（从JSON配置文件读取）"""
    return character_data_loader.get_character_presets()


def select_character(characters: list) -> Player:
    """让玩家选择角色，所有输出通过 DungeonMaster 进行"""
    dungeon_master.log_message(f"\n请选择你的角色职业:")
    dungeon_master.log_message("-" * 50)

    ## 展示角色列表
    for i, char in enumerate(characters, 1):
        dungeon_master.log_message(
            f"{i}. {char['class']:8} | "
            f"生命值: {char['health']:3} | "
            f"攻击力: {char['attack']:2} | "
            f"防御力: {char['defense']:2}"
        )

    get_player_choice = False
    player_name = ""
    char_data = {}
    while not get_player_choice:
        try:
            choice = int(input(f"\n玩家请选择角色 (1-{len(characters)}): "))
            if 1 <= choice <= len(characters):
                char_data = characters[choice - 1]

                # 询问是否使用随机名称
                dungeon_master.log_message(f"\n已选择角色: {char_data['class']}")
                name_choice = (
                    input("是否使用随机角色名称？(y/n，默认n): ").strip().lower()
                )

                if name_choice in ["y", "yes", "Y", "是"]:
                    random_name = character_name_generator.get_random_name()
                    player_name = f"{random_name}"
                    dungeon_master.log_message(f"🎲 随机角色名称: {random_name}")

                get_player_choice = True

            else:
                dungeon_master.log_message(f"❌ 请输入1到{len(characters)}之间的数字")
        except ValueError:
            dungeon_master.log_message("❌ 请输入有效的数字")

    ## 角色名字
    while not player_name:
        player_name = input("请输入你的角色名字: ").strip()
        if not player_name:
            dungeon_master.log_message("❌ 角色名字不能为空，请重新输入。")

    return Player(
        name=player_name,
        character_class=char_data["class"],
        health=char_data["health"],
        attack=char_data["attack"],
        defense=char_data["defense"],
    )


def start_battle():
    """开始战斗"""
    characters = create_preset_characters()

    # 创建唯一 log 文件名
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"battle_{timestamp}.log")
    dungeon_master.init_logger(log_file_path)

    # 角色选择界面
    dungeon_master.log_message("\n" + "=" * 60)
    player1 = select_character(characters)
    player1.pre_name = "【玩家】"
    # 随机敌人
    enemy_data = random.choice(characters)
    enemy_name = character_name_generator.get_random_name(player1.name)
    enemy = Player(
        name=enemy_name,
        character_class=enemy_data["class"],
        health=enemy_data["health"],
        attack=enemy_data["attack"],
        defense=enemy_data["defense"],
    )
    # 创建并开始战斗
    battle = Battle(player1, enemy, dungeon_master)
    battle_result = battle.fight_until_end()

    # 显示战斗摘要
    summary = battle.get_battle_summary()
    dungeon_master.log_message(f"\n📊 战斗统计:")
    dungeon_master.log_message(
        f"   {player1.name} 总伤害: {summary['player1_damage_dealt']}"
    )
    dungeon_master.log_message(
        f"   {enemy.name} 总伤害: {summary['player2_damage_dealt']}"
    )
    dungeon_master.log_message(f"战斗日志已保存到: {log_file_path}")
    dungeon_master.logger.close()


def show_game_guide():
    """显示游戏说明"""
    dungeon_master.print_guide()
    dungeon_master.input_prompt("按回车键返回主菜单...")


def main():
    """主函数"""
    if not character_data_loader.all_load_success:
        dungeon_master.print_message(
            "❌ 角色数据加载失败，无法启动游戏。请检查配置文件。"
        )
        return
    if not character_name_generator.all_load_success:
        dungeon_master.print_message(
            "❌ 角色名称数据加载失败，无法启动游戏。请检查配置文件。"
        )
        return
    if character_data_loader.get_characters_count() == 0:
        dungeon_master.print_message(
            "❌ 没有可用的角色预制数据，无法启动游戏。请检查配置文件。"
        )
        return

    time.sleep(1)

    while True:
        time.sleep(0.2)
        clear_screen()
        dungeon_master.print_game_logo_title()
        dungeon_master.print_intro()

        choice = get_player_choice()

        if choice == "1":
            start_battle()
            dungeon_master.input_prompt("按回车键返回主菜单...")

        elif choice == "2":
            clear_screen()
            show_game_guide()

        elif choice == "3":
            dungeon_master.print_exit_message()
            break


if __name__ == "__main__":
    main()

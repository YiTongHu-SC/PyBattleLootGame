"""
PyBattleLootGame 主程序入口
运行战斗模拟游戏
"""

import os
from datetime import datetime
import random
import time
from typing import Tuple

from src.tool import Logger

from src import (
    Player,
    Battle,
    game_config,
    character_name_generator,
    character_data_loader,
)


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
    game_logo_title = game_config.game_info.get("game_logo_title", "终端地下城")
    print(game_logo_title)


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
    """创建预设角色（从JSON配置文件读取）"""
    return character_data_loader.get_character_presets()


def select_character(characters: list, log_func=print) -> Player:
    """让玩家选择角色，所有输出通过 log_func"""
    log_func(f"\n请选择你的角色职业:")
    log_func("-" * 50)

    ## 展示角色列表
    for i, char in enumerate(characters, 1):
        log_func(
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
                log_func(f"\n已选择角色: {char_data['class']}")
                name_choice = (
                    input("是否使用随机角色名称？(y/n，默认n): ").strip().lower()
                )

                if name_choice in ["y", "yes", "Y", "是"]:
                    random_name = character_name_generator.get_random_name()
                    player_name = f"{random_name}"
                    log_func(f"🎲 随机角色名称: {random_name}")

                get_player_choice = True

            else:
                log_func(f"❌ 请输入1到{len(characters)}之间的数字")
        except ValueError:
            log_func("❌ 请输入有效的数字")

    ## 角色名字
    while not player_name:
        player_name = input("请输入你的角色名字: ").strip()
        if not player_name:
            log_func("❌ 角色名字不能为空，请重新输入。")

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
    logger = Logger(log_file_path)
    log_func = logger.get_log_func()

    # 角色选择界面
    log_func("\n" + "=" * 60)
    player1 = select_character(characters, log_func=log_func)
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
    battle = Battle(player1, enemy, log_func=log_func)
    battle_result = battle.fight_until_end()

    # 显示战斗摘要
    summary = battle.get_battle_summary()
    log_func(f"\n📊 战斗统计:")
    log_func(f"   {player1.name} 总伤害: {summary['player1_damage_dealt']}")
    log_func(f"   {enemy.name} 总伤害: {summary['player2_damage_dealt']}")
    log_func(f"战斗日志已保存到: {log_file_path}")
    logger.close()


def show_game_guide():
    """显示游戏说明"""
    game_guide = game_config.game_info.get("game_guide", "")
    print(game_guide)
    input("\n按回车键返回主菜单...")


def main():
    """主函数"""
    if not character_data_loader.all_load_success:
        print("❌ 角色数据加载失败，无法启动游戏。请检查配置文件。")
        return
    if not character_name_generator.all_load_success:
        print("❌ 角色名称数据加载失败，无法启动游戏。请检查配置文件。")
        return
    if character_data_loader.get_characters_count() == 0:
        print("❌ 没有可用的角色预制数据，无法启动游戏。请检查配置文件。")
        return
    print("欢迎来到 地下城 世界")
    time.sleep(1)
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
            show_game_guide()

        elif choice == "3":
            print(f"\n {game_config.game_info.get('game_exit', '')}")
            break


if __name__ == "__main__":
    main()

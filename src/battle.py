"""
战斗系统模块
处理1v1战斗逻辑，包括回合制战斗和战斗结果
"""

import random
import time
from typing import List, Dict, Any, Optional
from .player import Player


class Battle:
    """1v1战斗类"""

    def __init__(self, player1: Player, player2: Player):
        """
        初始化战斗

        Args:
            player1: 玩家1
            player2: 玩家2
        """
        self.player1 = player1
        self.player2 = player2
        self.battle_log: List[Dict[str, Any]] = []
        self.round_number = 0
        self.winner: Optional[Player] = None
        self.battle_ended = False

    def determine_turn_order(self) -> List[Player]:
        """
        确定行动顺序（基于速度，这里简单随机）

        Returns:
            按行动顺序排列的玩家列表
        """
        # 这里可以基于角色的敏捷属性来决定，目前简单随机
        players = [self.player1, self.player2]
        random.shuffle(players)
        return players

    def execute_round(self) -> Dict[str, Any]:
        """
        执行一个战斗回合

        Returns:
            回合结果信息
        """
        if self.battle_ended:
            return {"error": "Battle has already ended"}

        self.round_number += 1
        round_log = {"round": self.round_number, "actions": []}

        # 确定行动顺序
        turn_order = self.determine_turn_order()

        for attacker in turn_order:
            if not attacker.is_alive:
                continue

            # 确定目标
            target = self.player2 if attacker == self.player1 else self.player1

            if not target.is_alive:
                continue

            # 执行攻击
            attack_result = attacker.attack_target(target)
            round_log["actions"].append(attack_result)

            # 检查战斗是否结束
            if not target.is_alive:
                self.winner = attacker
                self.battle_ended = True
                break

        self.battle_log.append(round_log)
        return round_log

    def fight_until_end(self, max_rounds: int = 50) -> Dict[str, Any]:
        """
        战斗直到有一方败北

        Args:
            max_rounds: 最大回合数（防止无限战斗）

        Returns:
            战斗结果
        """
        print(f"\n🔥 战斗开始！🔥")
        print(f"{self.player1.get_full_name()} VS {self.player2.get_full_name()}")
        print("=" * 60)

        # 显示初始状态
        self._display_battle_status()
        self.auto_advance = False
        while not self.battle_ended and self.round_number < max_rounds:
            if not self.auto_advance:
                choice = input("\n回车键继续下一回合（输入A进入自动模式）...")
                if choice.strip().lower() == "a":
                    print("进入自动战斗模式...")
                    self.auto_advance = True
                else:
                    self.auto_advance = False

            round_result = self.execute_round()
            # 显示回合结果
            self._display_round_result(round_result)
            # 显示当前状态
            self._display_battle_status()

            if not self.battle_ended:
                time.sleep(1)  # 短暂停顿

        # 战斗结束
        battle_result = self._generate_battle_result(max_rounds)
        self._display_battle_end(battle_result)

        return battle_result

    def _display_battle_status(self):
        """显示战斗状态"""
        if self.round_number == 0:
            print("\n📊 对战信息:")
        else:
            print(f"\n📊 第{self.round_number}回合后状态:")
        print("-" * 60)
        print(self.player1)
        print()
        print(self.player2)
        print("-" * 60)

    def _display_round_result(self, round_result: Dict[str, Any]):
        """显示回合结果"""
        if "error" in round_result:
            return

        print(f"\n⚔️  第{round_result['round']}回合:")

        for action in round_result["actions"]:
            attacker = action["attacker"]
            target = action["target"]
            damage = action["actual_damage"]
            is_critical = action["is_critical"]

            crit_text = " 💥暴击！" if is_critical else ""
            print(f"   {attacker} 攻击 {target}，造成 {damage} 点伤害{crit_text}")

            if not action["target_alive"]:
                print(f"   💀 {target} 被击败！")

    def _display_battle_end(self, battle_result: Dict[str, Any]):
        """显示战斗结束信息"""
        print("\n" + "=" * 60)

        if battle_result["outcome"] == "victory":
            print(f"🎉 {battle_result['winner']} 获得胜利！")
        elif battle_result["outcome"] == "timeout":
            print("⏰ 战斗超时，平局！")

        print(f"战斗持续了 {battle_result['total_rounds']} 回合")
        print("=" * 60)

    def _generate_battle_result(self, max_rounds: int) -> Dict[str, Any]:
        """生成战斗结果"""
        if self.winner:
            return {
                "outcome": "victory",
                "winner": self.winner.name,
                "loser": (
                    self.player2.name
                    if self.winner == self.player1
                    else self.player1.name
                ),
                "total_rounds": self.round_number,
                "battle_log": self.battle_log,
            }
        else:
            return {
                "outcome": "timeout",
                "winner": None,
                "total_rounds": self.round_number,
                "max_rounds_reached": self.round_number >= max_rounds,
                "battle_log": self.battle_log,
            }

    def get_battle_summary(self) -> Dict[str, Any]:
        """获取战斗摘要"""
        total_damage_p1 = 0
        total_damage_p2 = 0

        for round_data in self.battle_log:
            for action in round_data["actions"]:
                if action["attacker"] == self.player1.name:
                    total_damage_p1 += action["actual_damage"]
                else:
                    total_damage_p2 += action["actual_damage"]

        return {
            "total_rounds": self.round_number,
            "player1_damage_dealt": total_damage_p1,
            "player2_damage_dealt": total_damage_p2,
            "winner": self.winner.name if self.winner else None,
            "battle_ended": self.battle_ended,
        }

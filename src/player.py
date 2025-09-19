"""
角色类模块
定义玩家角色的基本属性和战斗能力
"""

import random
from typing import Dict, Any


class Player:
    """玩家角色类"""

    def __init__(
        self, name: str, character_class: str, health: int, attack: int, defense: int
    ):
        """
        初始化角色

        Args:
            name: 角色名称
            health: 生命值
            attack: 攻击力
            defense: 防御力
        """
        self.name = name
        self.character_class = character_class
        self.max_health = health
        self.current_health = health
        self.attack = attack
        self.defense = defense
        self.is_alive = True
        self.pre_name = ""  # 称号前缀

    def take_damage(self, damage: int) -> int:
        """
        承受伤害

        Args:
            damage: 原始伤害值

        Returns:
            实际承受的伤害值
        """
        # 计算实际伤害（考虑防御力）
        actual_damage = max(1, damage - self.defense)  # 至少造成1点伤害

        self.current_health -= actual_damage

        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False

        return actual_damage

    def attack_target(self, target: "Player") -> Dict[str, Any]:
        """
        攻击目标

        Args:
            target: 被攻击的目标

        Returns:
            攻击结果信息
        """
        # 基础伤害带有随机性（80%-120%）
        damage_multiplier = random.uniform(0.8, 1.2)
        base_damage = int(self.attack * damage_multiplier)

        # 暴击判定（10%概率）
        is_critical = random.random() < 0.1
        if is_critical:
            base_damage = int(base_damage * 1.5)

        actual_damage = target.take_damage(base_damage)

        return {
            "attacker": self.name,
            "target": target.name,
            "base_damage": base_damage,
            "actual_damage": actual_damage,
            "is_critical": is_critical,
            "target_health": target.current_health,
            "target_alive": target.is_alive,
        }

    def heal(self, amount: int) -> int:
        """
        治疗

        Args:
            amount: 治疗量

        Returns:
            实际治疗量
        """
        if not self.is_alive:
            return 0

        old_health = self.current_health
        self.current_health = min(self.max_health, self.current_health + amount)
        actual_heal = self.current_health - old_health

        return actual_heal

    def get_health_percentage(self) -> float:
        """获取血量百分比"""
        return (self.current_health / self.max_health) * 100

    def get_status(self) -> Dict[str, Any]:
        """获取角色状态信息"""
        return {
            "name": self.name,
            "class": self.character_class,
            "health": f"{self.current_health}/{self.max_health}",
            "health_percentage": self.get_health_percentage(),
            "attack": self.attack,
            "defense": self.defense,
            "is_alive": self.is_alive,
        }

    def __str__(self) -> str:
        """字符串表示"""
        health_bar_length = 20
        health_percentage = self.get_health_percentage()
        filled_length = int(health_bar_length * health_percentage / 100)

        health_bar = "█" * filled_length + "░" * (health_bar_length - filled_length)
        status = "存活" if self.is_alive else "阵亡"

        return (
            f"{self.get_full_name()} [{status}]\n"
            f"生命值: {health_bar} {self.current_health}/{self.max_health} ({health_percentage:.1f}%)\n"
            f"攻击力: {self.attack} | 防御力: {self.defense}"
        )

    def get_full_name(self) -> str:
        """获取带前缀的全名"""
        return f"{self.pre_name} {self.name} [{self.character_class}]"

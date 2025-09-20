"""
PyBattleLootGame 源代码包
"""

from .tool import Logger
from .dungeon_master import DungeonMaster
from .player import Player
from .battle import Battle
from .config_manager import GameConfig, game_config
from .character_generator import (
    CharacterNameGenerator,
    character_name_generator,
    CharacterDataLoader,
    character_data_loader,
)
from .game_logger import (
    debug_logger,
    verbose, debug, info, critical,
    set_debug_level, set_debug_environment,
    enable_debug, disable_debug, debug_status,
    LogLevel, Environment
)

__version__ = "1.0.0"
__author__ = "PyBattleLootGame Developer"

__all__ = [
    "Player",
    "Battle",
    "GameConfig",
    "game_config",
    "CharacterNameGenerator",
    "character_name_generator",
    "CharacterDataLoader",
    "character_data_loader",
    "DungeonMaster",
    "Logger",
    # 调试工具
    "debug_logger",
    "verbose", "debug", "info", "critical",
    "set_debug_level", "set_debug_environment",
    "enable_debug", "disable_debug", "debug_status",
    "LogLevel", "Environment",
]

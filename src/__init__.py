"""
PyBattleLootGame 源代码包
"""

from .player import Player
from .battle import Battle
from .config_manager import GameConfig, game_config
from .character_generator import CharacterNameGenerator, character_name_generator, CharacterDataLoader, character_data_loader

__version__ = "1.0.0"
__author__ = "PyBattleLootGame Developer"

__all__ = ["Player", "Battle", "GameConfig", "game_config", "CharacterNameGenerator", "character_name_generator", "CharacterDataLoader", "character_data_loader"]
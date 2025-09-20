"""
游戏引导信息
"""

from .tool import Logger


class DungeonMaster:
    def __init__(self, game_info):
        self.game_info = game_info
        self.logger = Logger()

    def init_logger(self, log_file_path):
        self.logger.init_logger(log_file_path)

    def print_intro(self):
        intro = self.game_info.get("game_intro", "欢迎来到游戏！")
        self.print_message(intro)

    def print_game_logo_title(self):
        title = self.game_info.get("game_logo_title", "游戏标题")
        self.print_message(title)

    def print_guide(self):
        guide = self.game_info.get("game_guide", "游戏指南内容")
        self.print_message(guide)

    def print_exit_message(self):
        exit_message = self.game_info.get("game_exit", "感谢游玩！")
        self.print_message(exit_message)

    def input_prompt(self, prompt: str) -> str:
        return input(f"\n{prompt}").strip()

    def print_message(self, message: str):
        """直接打印消息，如果需要记录信息，可以使用 log_message 方法

        Args:
            message (str): 要打印的消息
        """
        print(message)

    def log_message(self, message: str):
        """记录日志信息

        Args:
            message (str): 要记录的日志信息
        """
        if not self.logger:
            raise ValueError("Logger 未初始化，请先调用 init_logger 方法")
        self.logger.log(message)

    def close_logger(self):
        if self.logger:
            self.logger.close()

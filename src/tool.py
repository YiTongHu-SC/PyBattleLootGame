from io import TextIOWrapper


class Logger:
    """
    简单的日志记录器，写入到指定文件并同步输出到终端。
    """

    def __init__(self):
        self.log_file: TextIOWrapper

    def init_logger(self, log_file_path):
        self.log_file = open(log_file_path, "w", encoding="utf-8")

    def log(self, msg):
        print(msg)
        self.log_file.write(msg + "\n")
        self.log_file.flush()

    def close(self):
        self.log_file.close()

    def get_log_func(self):
        """
        返回日志函数
        """
        return self.log

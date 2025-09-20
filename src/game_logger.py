"""
全局调试工具脚本
用于向屏幕输出不同等级的调试信息

等级说明:
- 0: 详细调试信息 (开发环境显示)
- 1: 一般调试信息 (开发调试模式及以上显示)  
- 2: 重要信息 (调试运行环境及以上显示)
- 3: 关键信息 (所有环境显示)

环境模式:
- development: 开发环境 (显示0级及以上)
- debug: 开发调试模式 (显示1级及以上)
- testing: 调试运行环境 (显示2级及以上)  
- production: 正式运行环境 (显示3级及以上)
"""

import os
import sys
from datetime import datetime
from enum import IntEnum
from typing import Optional, Union, Any, Dict
import inspect
import yaml
from .resource_path import get_resource_path


class LogLevel(IntEnum):
    """调试信息等级枚举"""
    VERBOSE = 0   # 详细调试信息
    DEBUG = 1     # 一般调试信息
    INFO = 2      # 重要信息
    CRITICAL = 3  # 关键信息


class Environment(IntEnum):
    """运行环境枚举"""
    DEVELOPMENT = 0   # 开发环境
    DEBUG = 1         # 开发调试模式
    TESTING = 2       # 调试运行环境
    PRODUCTION = 3    # 正式运行环境


class DebugLogger:
    """全局调试信息输出工具"""
    
    def __init__(self, environment: Optional[str] = None, min_level: Optional[int] = None, config_path: Optional[str] = None):
        """
        初始化调试工具
        
        Args:
            environment: 环境模式 ('development', 'debug', 'testing', 'production')
            min_level: 最小输出等级 (0-3)，如果指定则覆盖环境默认等级
            config_path: 配置文件路径
        """
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 设置基础属性
        if environment:
            self.environment = self._detect_environment(environment)
        elif self.config.get('environment'):
            self.environment = self._detect_environment(self.config.get('environment'))
        else:
            self.environment = self._detect_environment()

        self.min_level = min_level if min_level is not None else self._get_config_min_level()
        self.enabled = self._get_config_bool('display.enabled', True)
        self.show_timestamp = self._get_config_bool('display.show_timestamp', True)
        self.show_caller = self._get_config_bool('display.show_caller', True)
        self.color_enabled = self._get_config_bool('display.color_enabled', True) and self._check_color_support()
        
        # 颜色配置
        self.colors = self._get_color_config()
        self.reset_color = self.config.get('colors', {}).get('reset', '\033[0m')
        
        # 等级标识符配置
        self.level_labels = self._get_level_labels_config()
        
        # 时间戳格式
        self.timestamp_format = self._get_config_str('format.timestamp_format', '%H:%M:%S.%f')
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """加载配置文件"""
        if yaml is None:
            return {}
        
        if config_path is None:
            try:
                config_path = get_resource_path('config/debug.yaml')
            except:
                return {}
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
        except Exception:
            pass
        
        return {}
    
    def _get_config_value(self, key_path: str, default=None):
        """获取嵌套配置值"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def _get_config_bool(self, key_path: str, default: bool) -> bool:
        """获取布尔配置值"""
        value = self._get_config_value(key_path, default)
        return bool(value) if value is not None else default
    
    def _get_config_str(self, key_path: str, default: str) -> str:
        """获取字符串配置值"""
        value = self._get_config_value(key_path, default)
        return str(value) if value is not None else default
    
    def _get_config_min_level(self) -> int:
        """获取配置的最小等级或环境默认等级"""
        config_level = self._get_config_value('min_level')
        if config_level is not None:
            try:
                if isinstance(config_level, (int, float, str)):
                    return max(0, min(3, int(config_level)))
            except (ValueError, TypeError):
                pass
        return self.environment
    
    def _get_color_config(self) -> Dict[LogLevel, str]:
        """获取颜色配置"""
        color_config = self.config.get('colors', {})
        return {
            LogLevel.VERBOSE: color_config.get('verbose', '\033[37m'),
            LogLevel.DEBUG: color_config.get('debug', '\033[36m'),
            LogLevel.INFO: color_config.get('info', '\033[33m'),
            LogLevel.CRITICAL: color_config.get('critical', '\033[31m'),
        }
    
    def _get_level_labels_config(self) -> Dict[LogLevel, str]:
        """获取等级标签配置"""
        label_config = self._get_config_value('format.level_labels', {})
        if not isinstance(label_config, dict):
            label_config = {}
        return {
            LogLevel.VERBOSE: label_config.get('verbose', '[VERBOSE]'),
            LogLevel.DEBUG: label_config.get('debug', '[DEBUG]'),
            LogLevel.INFO: label_config.get('info', '[INFO]'),
            LogLevel.CRITICAL: label_config.get('critical', '[CRITICAL]'),
        }
    
    def _detect_environment(self, env_override: Optional[str] = None) -> Environment:
        """
        检测运行环境
        
        Args:
            env_override: 环境覆盖设置
            
        Returns:
            Environment: 检测到的环境类型
        """
        if env_override:
            env_map = {
                'development': Environment.DEVELOPMENT,
                'debug': Environment.DEBUG,
                'testing': Environment.TESTING,
                'production': Environment.PRODUCTION,
            }
            return env_map.get(env_override.lower(), Environment.DEVELOPMENT)
        
        # 从环境变量检测
        env_var = os.getenv('GAME_ENV', '').lower()
        if env_var in ['dev', 'development']:
            return Environment.DEVELOPMENT
        elif env_var in ['debug']:
            return Environment.DEBUG
        elif env_var in ['test', 'testing']:
            return Environment.TESTING
        elif env_var in ['prod', 'production']:
            return Environment.PRODUCTION
        
        # 根据其他指标判断
        if getattr(sys, 'frozen', False):  # 打包后的exe
            return Environment.PRODUCTION
        elif os.path.exists('.git'):  # Git仓库
            return Environment.DEVELOPMENT
        elif '--debug' in sys.argv:  # 命令行调试参数
            return Environment.DEBUG
        else:
            return Environment.DEVELOPMENT
    
    def _check_color_support(self) -> bool:
        """检查终端是否支持颜色输出"""
        if os.getenv('NO_COLOR'):
            return False
        if os.getenv('FORCE_COLOR'):
            return True
        
        # 检查是否在支持颜色的终端中
        try:
            if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
                return True
        except:
            pass
        
        # Windows终端颜色支持检查
        if os.name == 'nt':
            try:
                # 启用Windows控制台的ANSI颜色支持
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
                return True
            except:
                return False
        
        return True
    
    def _get_caller_info(self) -> str:
        """获取调用者信息"""
        if not self.show_caller:
            return ""
        
        # 获取调用栈，跳过当前函数和log函数
        frame = inspect.currentframe()
        try:
            # 跳过 _get_caller_info -> log -> 实际调用处
            if frame and frame.f_back and frame.f_back.f_back:
                caller_frame = frame.f_back.f_back.f_back
                if caller_frame:
                    filename = os.path.basename(caller_frame.f_code.co_filename)
                    line_no = caller_frame.f_lineno
                    func_name = caller_frame.f_code.co_name
                    return f"{filename}:{func_name}():{line_no}"
        except:
            pass
        finally:
            if frame:
                del frame
        
        return "unknown"
    
    def _format_message(self, level: LogLevel, message: str) -> str:
        """
        格式化输出消息
        
        Args:
            level: 日志等级
            message: 原始消息
            
        Returns:
            str: 格式化后的消息
        """
        parts = []
        
        # 时间戳
        if self.show_timestamp:
            try:
                timestamp = datetime.now().strftime(self.timestamp_format)
                # 处理微秒截断
                if '.%f' in self.timestamp_format:
                    timestamp = timestamp[:-3]  # 只显示毫秒
            except:
                timestamp = datetime.now().strftime("%H:%M:%S")
            parts.append(f"[{timestamp}]")
        
        # 等级标签
        level_label = self.level_labels[level]
        if self.color_enabled:
            level_label = f"{self.colors[level]}{level_label}{self.reset_color}"
        parts.append(level_label)
        
        # 调用者信息
        caller_info = self._get_caller_info()
        if caller_info:
            parts.append(f"({caller_info})")
        
        # 消息内容
        if self.color_enabled and level in self.colors:
            message = f"{self.colors[level]}{message}{self.reset_color}"
        parts.append(message)
        
        return " ".join(parts)
    
    def log(self, level: Union[int, LogLevel], message: Any, *args) -> None:
        """
        输出调试信息
        
        Args:
            level: 信息等级 (0-3)
            message: 要输出的消息
            *args: 格式化参数
        """
        if not self.enabled:
            return
        
        # 转换为LogLevel枚举
        if isinstance(level, int):
            if level < 0 or level > 3:
                level = LogLevel.DEBUG
            else:
                level = LogLevel(level)
        
        # 检查等级是否满足输出条件
        if level < self.min_level:
            return
        
        # 格式化消息
        if args:
            try:
                message = str(message) % args
            except:
                message = str(message) + " " + " ".join(str(arg) for arg in args)
        else:
            message = str(message)
        
        # 输出消息
        formatted_message = self._format_message(level, message)
        print(formatted_message, file=sys.stdout, flush=True)
    
    def verbose(self, message: Any, *args) -> None:
        """输出详细调试信息 (等级0)"""
        self.log(LogLevel.VERBOSE, message, *args)
    
    def debug(self, message: Any, *args) -> None:
        """输出一般调试信息 (等级1)"""
        self.log(LogLevel.DEBUG, message, *args)
    
    def info(self, message: Any, *args) -> None:
        """输出重要信息 (等级2)"""
        self.log(LogLevel.INFO, message, *args)
    
    def critical(self, message: Any, *args) -> None:
        """输出关键信息 (等级3)"""
        self.log(LogLevel.CRITICAL, message, *args)
    
    def set_level(self, level: Union[int, LogLevel]) -> None:
        """设置最小输出等级"""
        if isinstance(level, int):
            level = LogLevel(max(0, min(3, level)))
        self.min_level = level
    
    def set_environment(self, environment: Union[str, Environment]) -> None:
        """设置运行环境"""
        if isinstance(environment, str):
            environment = self._detect_environment(environment)
        self.environment = environment
        self.min_level = environment
    
    def enable(self) -> None:
        """启用调试输出"""
        self.enabled = True
    
    def disable(self) -> None:
        """禁用调试输出"""
        self.enabled = False
    
    def toggle_timestamp(self, show: Optional[bool] = None) -> None:
        """切换时间戳显示"""
        if show is None:
            self.show_timestamp = not self.show_timestamp
        else:
            self.show_timestamp = show
    
    def toggle_caller(self, show: Optional[bool] = None) -> None:
        """切换调用者信息显示"""
        if show is None:
            self.show_caller = not self.show_caller
        else:
            self.show_caller = show
    
    def toggle_color(self, enable: Optional[bool] = None) -> None:
        """切换颜色输出"""
        if enable is None:
            self.color_enabled = not self.color_enabled
        else:
            self.color_enabled = enable and self._check_color_support()
    
    def get_status(self) -> dict:
        """获取调试器当前状态"""
        return {
            'enabled': self.enabled,
            'environment': self.environment.name,
            'min_level': self.min_level,
            'show_timestamp': self.show_timestamp,
            'show_caller': self.show_caller,
            'color_enabled': self.color_enabled,
        }


# 全局调试器实例
debug_logger = DebugLogger()

# 便捷函数
def log(level: Union[int, LogLevel], message: Any, *args) -> None:
    """全局调试信息输出函数"""
    debug_logger.log(level, message, *args)

def verbose(message: Any, *args) -> None:
    """输出详细调试信息 (等级0)"""
    debug_logger.verbose(message, *args)

def debug(message: Any, *args) -> None:
    """输出一般调试信息 (等级1)"""
    debug_logger.debug(message, *args)

def info(message: Any, *args) -> None:
    """输出重要信息 (等级2)"""
    debug_logger.info(message, *args)

def critical(message: Any, *args) -> None:
    """输出关键信息 (等级3)"""
    debug_logger.critical(message, *args)

def set_debug_level(level: Union[int, LogLevel]) -> None:
    """设置调试等级"""
    debug_logger.set_level(level)

def set_debug_environment(environment: Union[str, Environment]) -> None:
    """设置调试环境"""
    debug_logger.set_environment(environment)

def enable_debug() -> None:
    """启用调试输出"""
    debug_logger.enable()

def disable_debug() -> None:
    """禁用调试输出"""
    debug_logger.disable()

def debug_status() -> dict:
    """获取调试器状态"""
    return debug_logger.get_status()


if __name__ == "__main__":
    """测试脚本"""
    print("=== 调试工具测试 ===")
    
    # 显示当前状态
    status = debug_status()
    print(f"当前环境: {status['environment']}")
    print(f"最小等级: {status['min_level']}")
    print()
    
    # 测试不同等级的输出
    print("测试不同等级输出:")
    verbose("这是详细调试信息 (等级0)")
    debug("这是一般调试信息 (等级1)")
    info("这是重要信息 (等级2)")
    critical("这是关键信息 (等级3)")
    print()
    
    # 测试环境切换
    print("切换到生产环境:")
    set_debug_environment('production')
    verbose("这条消息不会显示")
    debug("这条消息不会显示")
    info("这条消息不会显示")
    critical("只有这条消息会显示")
    print()
    
    # 恢复开发环境
    print("恢复开发环境:")
    set_debug_environment('development')
    verbose("现在所有消息都会显示")
    debug("包括这条调试信息")
    info("和这条重要信息")
    critical("以及这条关键信息")
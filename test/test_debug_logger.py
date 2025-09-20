#!/usr/bin/env python3
"""
调试工具测试脚本
测试 game_logger 模块的各种功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game_logger import (
    debug_logger, 
    verbose, debug, info, critical,
    set_debug_level, set_debug_environment,
    enable_debug, disable_debug, debug_status,
    LogLevel, Environment
)


def test_basic_logging():
    """测试基本的日志输出功能"""
    print("=== 测试基本日志输出 ===")
    
    verbose("这是详细调试信息 (等级0)")
    debug("这是一般调试信息 (等级1)")  
    info("这是重要信息 (等级2)")
    critical("这是关键信息 (等级3)")
    print()


def test_environment_switching():
    """测试环境切换功能"""
    print("=== 测试环境切换 ===")
    
    environments = ['development', 'debug', 'testing', 'production']
    
    for env in environments:
        print(f"\n--- 切换到 {env.upper()} 环境 ---")
        set_debug_environment(env)
        status = debug_status()
        print(f"当前环境: {status['environment']}, 最小等级: {status['min_level']}")
        
        verbose(f"[{env}] 详细信息测试")
        debug(f"[{env}] 调试信息测试")
        info(f"[{env}] 重要信息测试")
        critical(f"[{env}] 关键信息测试")


def test_level_control():
    """测试等级控制功能"""
    print("\n=== 测试等级控制 ===")
    
    # 重置为开发环境
    set_debug_environment('development')
    
    for level in range(4):
        print(f"\n--- 设置最小等级为 {level} ---")
        set_debug_level(level)
        
        verbose(f"[Level {level}] 详细信息 (等级0)")
        debug(f"[Level {level}] 调试信息 (等级1)")
        info(f"[Level {level}] 重要信息 (等级2)")
        critical(f"[Level {level}] 关键信息 (等级3)")


def test_formatting_options():
    """测试格式化选项"""
    print("\n=== 测试格式化选项 ===")
    
    # 重置为开发环境，等级0
    set_debug_environment('development')
    
    print("\n--- 默认格式 ---")
    info("这是默认格式的消息")
    
    print("\n--- 关闭时间戳 ---")
    debug_logger.toggle_timestamp(False)
    info("这是关闭时间戳的消息")
    
    print("\n--- 关闭调用者信息 ---")
    debug_logger.toggle_caller(False)
    info("这是关闭调用者信息的消息")
    
    print("\n--- 关闭颜色 ---")
    debug_logger.toggle_color(False)
    info("这是关闭颜色的消息")
    
    # 恢复默认设置
    debug_logger.toggle_timestamp(True)
    debug_logger.toggle_caller(True)
    debug_logger.toggle_color(True)


def test_enable_disable():
    """测试启用/禁用功能"""
    print("\n=== 测试启用/禁用 ===")
    
    set_debug_environment('development')
    
    print("\n--- 正常输出 ---")
    info("这条消息应该显示")
    
    print("\n--- 禁用调试输出 ---")
    disable_debug()
    info("这条消息不应该显示")
    
    print("--- 重新启用调试输出 ---")
    enable_debug()
    info("这条消息应该显示")


def test_formatting_with_args():
    """测试带参数的格式化"""
    print("\n=== 测试参数格式化 ===")
    
    set_debug_environment('development')
    
    name = "游戏测试"
    level = 5
    score = 1234.56
    
    verbose("玩家信息: %s", name)
    debug("当前等级: %d", level)
    info("得分: %.2f", score)
    critical("完整信息: %s 等级 %d, 得分 %.2f", name, level, score)
    
    # 测试多参数
    debug("多参数测试:", name, level, score)


def test_status_info():
    """测试状态信息"""
    print("\n=== 测试状态信息 ===")
    
    status = debug_status()
    print("调试器状态:")
    for key, value in status.items():
        print(f"  {key}: {value}")


def main():
    """主测试函数"""
    print("调试工具测试开始")
    print("=" * 50)
    
    # 执行各项测试
    test_basic_logging()
    test_environment_switching()
    test_level_control()
    test_formatting_options()
    test_enable_disable()
    test_formatting_with_args()
    test_status_info()
    
    print("\n" + "=" * 50)
    print("调试工具测试完成")


if __name__ == "__main__":
    main()
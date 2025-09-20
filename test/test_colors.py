#!/usr/bin/env python3
"""
颜色输出测试脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game_logger import verbose, debug, info, critical, debug_logger

def test_colors():
    print("=== 颜色输出测试 ===\n")
    
    # 显示调试器状态
    print(f"颜色支持: {debug_logger.color_enabled}")
    print(f"环境: {debug_logger.environment}")
    print(f"最小等级: {debug_logger.min_level}")
    print()
    
    # 测试原始ANSI代码
    print("原始ANSI测试:")
    print("\033[31m红色文本\033[0m")
    print("\033[33m黄色文本\033[0m")
    print("\033[36m青色文本\033[0m")
    print("\033[37m白色文本\033[0m")
    print()
    
    # 测试调试器颜色
    print("调试器颜色测试:")
    verbose("VERBOSE - 应该是白色")
    debug("DEBUG - 应该是青色")
    info("INFO - 应该是黄色")
    critical("CRITICAL - 应该是红色")
    print()
    
    # 测试无颜色模式
    print("无颜色模式测试:")
    debug_logger.toggle_color(False)
    verbose("VERBOSE - 无颜色")
    debug("DEBUG - 无颜色")
    info("INFO - 无颜色")
    critical("CRITICAL - 无颜色")
    
    # 恢复颜色
    debug_logger.toggle_color(True)
    print()
    info("颜色测试完成!")

if __name__ == "__main__":
    test_colors()
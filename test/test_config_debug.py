#!/usr/bin/env python3
"""
调试配置加载测试
"""

import sys
import os
import yaml

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game_logger import debug_logger

def test_config_loading():
    print("=== 配置加载调试 ===\n")
    
    # 直接加载YAML文件测试
    config_path = "config/debug.yaml"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("直接YAML加载结果:")
        colors = config.get('colors', {})
        for key, value in colors.items():
            print(f"  {key}: {repr(value)}")
        print()
        
    except Exception as e:
        print(f"YAML加载失败: {e}")
    
    # 检查调试器加载的配置
    print("调试器配置:")
    print(f"  config: {debug_logger.config}")
    print(f"  colors: {debug_logger.colors}")
    print(f"  reset_color: {repr(debug_logger.reset_color)}")
    print()
    
    # 测试转义序列处理
    test_string = "\\033[31m"
    print(f"测试字符串: {repr(test_string)}")
    print(f"处理后: {repr(test_string.replace('033[', '\\033['))}")

if __name__ == "__main__":
    test_config_loading()
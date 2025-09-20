#!/usr/bin/env python3
"""
测试环境等级交换
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game_logger import verbose, debug, info, critical, set_debug_environment, debug_status

print('=== 测试环境等级交换 ===')

environments = ['development', 'debug', 'testing', 'production']
for env in environments:
    set_debug_environment(env)
    status = debug_status()
    print(f'\n--- {env.upper()} 环境 (等级{status["min_level"]}) ---')
    verbose(f'[{env}] VERBOSE消息 (等级0)')
    debug(f'[{env}] DEBUG消息 (等级1)')
    info(f'[{env}] INFO消息 (等级2)')
    critical(f'[{env}] CRITICAL消息 (等级3)')

print('\n=== 交换效果说明 ===')
print('现在的等级映射:')
print('- DEVELOPMENT环境: 显示1级及以上 (DEBUG, INFO, CRITICAL)')
print('- DEBUG环境: 显示0级及以上 (VERBOSE, DEBUG, INFO, CRITICAL)')
print('- TESTING环境: 显示2级及以上 (INFO, CRITICAL)')  
print('- PRODUCTION环境: 显示3级及以上 (CRITICAL)')
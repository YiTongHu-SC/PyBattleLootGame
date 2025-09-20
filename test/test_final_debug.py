#!/usr/bin/env python3
"""
调试工具最终测试脚本
展示完整的调试工具功能
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


def test_final_functionality():
    """最终功能测试"""
    print("=== PyBattleLootGame 调试工具 - 最终测试 ===\n")
    
    # 显示初始状态
    status = debug_status()
    print(f"初始状态:")
    print(f"  环境: {status['environment']}")
    print(f"  最小等级: {status['min_level']}")
    print(f"  颜色支持: {status['color_enabled']}")
    print()
    
    # 测试各级别输出
    info("=== 等级测试 ===")
    verbose("0级: 这是详细调试信息 - 通常用于开发阶段的详细跟踪")
    debug("1级: 这是一般调试信息 - 用于调试问题和追踪流程")
    info("2级: 这是重要信息 - 记录关键操作和状态变化")
    critical("3级: 这是关键信息 - 错误、异常和重要事件")
    print()
    
    # 模拟游戏场景
    info("=== 游戏场景模拟 ===")
    
    # 玩家创建场景
    verbose("开始创建玩家角色")
    debug("验证玩家输入: 名称='测试勇者', 职业='战士'")
    info("玩家角色创建成功: 测试勇者 (战士)")
    
    # 战斗场景
    debug("初始化战斗系统")
    info("战斗开始: 测试勇者 vs 哥布林")
    verbose("回合1 - 玩家攻击，造成15点伤害")
    verbose("回合1 - 敌人反击，造成8点伤害")
    debug("战斗状态更新 - 玩家HP: 92/100, 敌人HP: 25/40")
    info("战斗胜利: 测试勇者获得胜利!")
    
    # 错误处理场景
    critical("配置文件读取失败: config/missing.yaml 文件不存在")
    critical("数据库连接错误: 无法连接到角色数据库")
    print()
    
    # 测试环境切换效果
    info("=== 环境切换效果演示 ===")
    
    environments = [
        ('production', '生产环境 - 仅显示关键信息'),
        ('testing', '测试环境 - 显示重要信息及以上'),
        ('debug', '调试模式 - 显示调试信息及以上'),
        ('development', '开发环境 - 显示所有信息')
    ]
    
    for env_key, env_desc in environments:
        print(f"\n--- {env_desc} ---")
        set_debug_environment(env_key)
        
        verbose("详细信息: 内部循环计数器值为42")
        debug("调试信息: 正在处理用户输入")
        info("重要信息: 保存游戏进度完成") 
        critical("关键信息: 系统内存使用率达到95%")
    
    # 恢复开发环境
    set_debug_environment('development')
    print()
    
    # 性能和使用建议
    info("=== 使用建议 ===")
    print("1. 开发阶段使用 development 环境，查看详细调试信息")
    print("2. 测试阶段使用 testing 环境，关注重要操作和错误")
    print("3. 生产环境使用 production 环境，仅记录关键事件")
    print("4. 使用参数化字符串避免不必要的性能开销:")
    print("   推荐: debug('处理用户 %s', username)")
    print("   避免: debug('处理用户 ' + username)")
    print()
    
    # 配置文件提示
    info("=== 配置文件 ===")
    print("可通过 config/debug.yaml 文件自定义调试行为:")
    print("- 设置默认环境和等级")
    print("- 自定义颜色和标签")
    print("- 控制显示选项")
    print()
    
    critical("测试完成 - 调试工具已就绪!")


if __name__ == "__main__":
    test_final_functionality()
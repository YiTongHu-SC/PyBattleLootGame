# 全局调试工具使用说明

## 概述

`game_logger.py` 是一个功能强大的全局调试工具，支持分级输出调试信息，并能根据不同的运行环境自动调整输出等级。

## 功能特性

### 调试等级

- **等级 0 (VERBOSE)**: 详细调试信息，用于开发时的详细跟踪
- **等级 1 (DEBUG)**: 一般调试信息，用于开发调试  
- **等级 2 (INFO)**: 重要信息，用于关键流程记录
- **等级 3 (CRITICAL)**: 关键信息，用于错误和重要事件

### 环境模式

- **开发环境 (DEVELOPMENT)**: 输出1级及以上信息 (DEBUG, INFO, CRITICAL)
- **开发调试模式 (DEBUG)**: 输出0级及以上信息 (VERBOSE, DEBUG, INFO, CRITICAL)
- **调试运行环境 (TESTING)**: 输出2级及以上信息 (INFO, CRITICAL)
- **正式运行环境 (PRODUCTION)**: 仅输出3级信息 (CRITICAL)

## 基本使用

### 导入方式

```python
# 方式1: 导入便捷函数
from src.game_logger import verbose, debug, info, critical

# 方式2: 导入完整工具
from src.game_logger import debug_logger

# 方式3: 从包中导入 (推荐)
from src import verbose, debug, info, critical
```

### 基本输出

```python
# 基本使用
verbose("这是详细调试信息")
debug("这是一般调试信息")
info("这是重要信息")
critical("这是关键信息")

# 带参数的格式化输出
player_name = "张三"
level = 10
debug("玩家 %s 升级到 %d 级", player_name, level)
info("当前血量: %d/%d", current_hp, max_hp)
```

## 配置和控制

### 设置环境模式

```python
from src.game_logger import set_debug_environment

# 手动设置环境
set_debug_environment('development')  # 开发环境
set_debug_environment('debug')        # 调试模式
set_debug_environment('testing')      # 测试环境
set_debug_environment('production')   # 生产环境
```

### 设置输出等级

```python
from src.game_logger import set_debug_level

# 设置最小输出等级
set_debug_level(0)  # 输出所有等级
set_debug_level(2)  # 只输出INFO和CRITICAL
```

### 启用/禁用调试

```python
from src.game_logger import enable_debug, disable_debug

disable_debug()  # 禁用所有调试输出
enable_debug()   # 重新启用调试输出
```

## 环境自动检测

工具会自动检测运行环境：

1. **环境变量检测**:
   ```bash
   # 设置环境变量
   set GAME_ENV=production  # Windows
   export GAME_ENV=production  # Linux/Mac
   ```

2. **打包状态检测**: 如果检测到是打包后的exe文件，自动设为生产环境

3. **Git仓库检测**: 如果在Git仓库中，自动设为开发环境

4. **命令行参数检测**: 如果有 `--debug` 参数，设为调试模式

## 高级功能

### 自定义格式化选项

```python
from src.game_logger import debug_logger

# 控制时间戳显示
debug_logger.toggle_timestamp(False)  # 关闭时间戳
debug_logger.toggle_timestamp(True)   # 开启时间戳

# 控制调用者信息显示
debug_logger.toggle_caller(False)     # 关闭调用者信息
debug_logger.toggle_caller(True)      # 开启调用者信息

# 控制颜色输出
debug_logger.toggle_color(False)      # 关闭颜色
debug_logger.toggle_color(True)       # 开启颜色
```

### 获取状态信息

```python
from src.game_logger import debug_status

status = debug_status()
print(f"当前环境: {status['environment']}")
print(f"最小等级: {status['min_level']}")
print(f"是否启用: {status['enabled']}")
```

## 实际应用示例

### 1. 战斗系统调试

```python
from src import debug, info, critical

class Battle:
    def fight(self, player1, player2):
        info("战斗开始: %s vs %s", player1.name, player2.name)
        
        while player1.is_alive() and player2.is_alive():
            debug("回合开始 - P1血量:%d P2血量:%d", player1.hp, player2.hp)
            
            damage = player1.attack(player2)
            debug("P1攻击P2，造成%d伤害", damage)
            
            if not player2.is_alive():
                critical("P2被击败！胜者：%s", player1.name)
                break
                
        info("战斗结束")
```

### 2. 角色加载调试

```python
from src import verbose, debug, info, critical

class CharacterLoader:
    def load_characters(self, file_path):
        verbose("开始加载角色数据: %s", file_path)
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                debug("成功读取文件，包含 %d 个角色", len(data))
                
                characters = []
                for char_data in data:
                    char = self._create_character(char_data)
                    characters.append(char)
                    verbose("创建角色: %s", char.name)
                
                info("角色加载完成，共加载 %d 个角色", len(characters))
                return characters
                
        except FileNotFoundError:
            critical("角色数据文件未找到: %s", file_path)
            return []
        except json.JSONDecodeError as e:
            critical("角色数据文件格式错误: %s", str(e))
            return []
```

### 3. 配置系统调试

```python
from src import debug, info, critical, set_debug_environment

class GameConfig:
    def __init__(self):
        # 在开发环境启用详细调试
        if self.is_development():
            set_debug_environment('development')
        else:
            set_debug_environment('production')
            
    def load_config(self, config_path):
        info("加载游戏配置: %s", config_path)
        
        try:
            # 配置加载逻辑
            debug("配置加载成功")
        except Exception as e:
            critical("配置加载失败: %s", str(e))
```

## 性能考虑

1. **零开销原则**: 在生产环境中，低等级的调试信息不会执行格式化操作
2. **条件检查**: 在调用 `log()` 函数前就进行等级检查
3. **延迟格式化**: 只有在需要输出时才进行字符串格式化

## 最佳实践

1. **等级分配**:
   - 0级: 循环内部、详细状态变化
   - 1级: 函数入口/退出、中间结果
   - 2级: 重要操作、用户行为
   - 3级: 错误、异常、关键状态变化

2. **消息格式**:
   - 包含足够的上下文信息
   - 使用动词描述正在进行的操作
   - 关键数据用参数化格式避免字符串拼接

3. **环境设置**:
   - 开发时使用详细模式
   - 测试时使用中等详细度
   - 生产环境只保留关键信息

4. **性能优化**:
   ```python
   # 好的做法
   debug("处理玩家数据: %s", player.name)
   
   # 避免的做法（会执行不必要的字符串拼接）
   debug("处理玩家数据: " + player.name)
   ```

## 与现有日志系统集成

如果项目中已有日志系统，可以配合使用：

```python
import logging
from src import debug, info, critical

# 游戏调试信息用 game_logger
debug("玩家移动到坐标 (%d, %d)", x, y)

# 系统日志用标准 logging
logging.info("用户登录成功")
```
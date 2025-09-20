"""
资源路径处理模块
解决PyInstaller打包后无法正确找到资源文件的问题
"""

import sys
import os


def get_resource_path(relative_path: str) -> str:
    """
    获取资源文件的绝对路径
    
    在开发环境中，返回相对于项目根目录的路径
    在PyInstaller打包环境中，返回临时目录中的路径
    
    Args:
        relative_path: 相对于项目根目录的路径，例如 "data/character_names.json"
    
    Returns:
        str: 资源文件的绝对路径
    """
    try:
        # PyInstaller 创建临时文件夹，并存储在 _MEIPASS 中
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path is None:
            raise AttributeError
    except AttributeError:
        # 开发环境中，使用当前文件所在目录的上级目录作为项目根目录
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)


def get_project_root() -> str:
    """
    获取项目根目录路径
    
    Returns:
        str: 项目根目录的绝对路径
    """
    try:
        # PyInstaller 环境
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path is not None:
            return base_path
        else:
            raise AttributeError
    except AttributeError:
        # 开发环境
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def resource_exists(relative_path: str) -> bool:
    """
    检查资源文件是否存在
    
    Args:
        relative_path: 相对于项目根目录的路径
    
    Returns:
        bool: 文件是否存在
    """
    return os.path.exists(get_resource_path(relative_path))
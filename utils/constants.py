"""常量的配置"""
from enum import Enum


class UserStatus(Enum):
    """用户状态"""
    # 启用 可以登录系统
    USER_ACTIVE = 1
    USER_IN_ACTIVE = 0


class UserRole(Enum):
    """用户的角色"""
    # 普通用户
    COMMON = 0
    # 管理员用户
    ADMIN = 1
    # 超级管理员
    SUPER_ADMIN = 2


class Page(Enum):
    per_page = 20

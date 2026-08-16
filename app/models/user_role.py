from enum import Enum


class UserRole(str, Enum):
    ROOT = "root"
    ADMIN = "admin"
    USER = "user"

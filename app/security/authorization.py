from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Depends, HTTPException, status

from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.user_role import UserRole

RoleDependency = Callable[
    [User],
    Coroutine[Any, Any, User],
]


def require_roles(*allowed_roles: UserRole) -> RoleDependency:
    """
    Create a FastAPI dependency that permits only selected user roles.

    Args:
        allowed_roles: Roles that are allowed to access the endpoint.

    Returns:
        An asynchronous FastAPI dependency.
    """

    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker


require_user = require_roles(
    UserRole.USER,
    UserRole.ADMIN,
    UserRole.ROOT,
)

require_admin = require_roles(
    UserRole.ADMIN,
    UserRole.ROOT,
)

require_root = require_roles(
    UserRole.ROOT,
)

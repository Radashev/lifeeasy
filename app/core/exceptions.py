class UserAlreadyExistsError(Exception):
    """Raised when user with the same email already exists."""


class UserNotFoundError(Exception):
    pass


class CannotChangeRootRoleError(Exception):
    pass



from typing import Any

class AppError(Exception):
    code="APP_ERROR"
    message="App error occured"

    def __init__(self, details:dict[str,Any]|None=None):
        self.details=details
        super().__init__(self.message)


"""
user custom exceptions
"""

class UserAlreadyExists(AppError):
    code="USER_ALREADY_EXIST"
    message="A user with this email is already exist"

class InvalidCredentialsError(AppError):
    code="INVALID_CREDENTIALS"
    message="Invalid email or password"

class TokenExpiredError(AppError):
    code="TOKEN_EXPIRED"
    message="The access token has expired"

class ValidationAppError(AppError):
    code = "VALIDATION_ERROR"
    message = "The provided data is invalid"





"""
Todo custom exceptions
"""

class TodoNotFoundError(AppError):
    code = "TODO_NOT_FOUND"
    message = "The requested todo item was not found"


class DuplicateTodoError(AppError):
    code = "DUPLICATE_TODO"
    message = "A todo with these details already exists"
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.errors.exceptions import (
    AppError,
    DuplicateTodoError,
    InvalidCredentialsError,
    TodoNotFoundError,
    TokenExpiredError,
    UserAlreadyExists,
    ValidationAppError,
)
from app.errors.responses import ErrorDetail, ErrorResponse

ERROR_STATUS_CODE = {
    UserAlreadyExists: status.HTTP_409_CONFLICT,
    InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
    TokenExpiredError: status.HTTP_401_UNAUTHORIZED,
    ValidationAppError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    DuplicateTodoError:status.HTTP_409_CONFLICT,
    TodoNotFoundError:status.HTTP_404_NOT_FOUND
}


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    status_code = ERROR_STATUS_CODE.get(
        type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR
    ) 
    response = ErrorResponse(
        error=ErrorDetail(code=exc.code, message=exc.message, details=exc.details)
    )

    return JSONResponse(
        status_code=status_code, content=response.model_dump(mode="json")
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = []

    for error in exc.errors():
        errors.append(
            {
                "location": list(error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    response = ErrorResponse(
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=errors,
        )
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=response.model_dump(mode="json"),
    )


async def unexcepted_error_handler(reqest: Request, exc: Exception):
    response = ErrorResponse(
        error=ErrorDetail(code="INTERNAL_SERVER_ERROR", message="Internal server Error")
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(mode="json"),
    )


def register_exception_handlers(app) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unexcepted_error_handler)

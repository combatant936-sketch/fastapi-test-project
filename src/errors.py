from fastapi import status
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request
from typing import Callable
from typing import Any
class BooklyException(Exception):
    """This is the base class for all bookly errors"""

    pass


class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(BooklyException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(BooklyException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(BooklyException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(BooklyException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(BooklyException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class BookNotFound(BooklyException):
    """Book Not found"""

    pass


class TagNotFound(BooklyException):
    """Tag Not found"""

    pass


class TagAlreadyExists(BooklyException):
    """Tag already exists"""

    pass


class UserNotFound(BooklyException):
    """User Not found"""

    pass


class AccountNotVerified(BooklyException):
    """Account not yet verified"""
    pass



def create_exception_handler(status_code: int, initial_details: Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(content=initial_details, status_code=status_code)
    
    return exception_handler
    

def register_custom_errors(app:FastAPI):
        app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "Invalid token",
                "message": "The provided token is invalid or expired."
            }
        )
    )

        app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "Revoked token",
                "message": "The provided token has been revoked."
            }
        )
    )

        app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "Access token required",
                "message": "Please provide a valid access token."
            }
        )
    )

        app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "Refresh token required",
                "message": "Please provide a valid refresh token."
            }
        )
    )


    # User errors

        app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status.HTTP_409_CONFLICT,
            {
                "error": "User already exists",
                "message": "A user with this email already exists."
            }
        )
    )

        app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            {
                "error": "Invalid credentials",
                "message": "Email or password is incorrect."
            }
        )
    )

        app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status.HTTP_403_FORBIDDEN,
            {
                "error": "Insufficient permission",
                "message": "You do not have permission to perform this action."
            }
        )
    )

        app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            {
                "error": "User not found",
                "message": "The requested user was not found."
            }
        )
    )

        app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status.HTTP_403_FORBIDDEN,
            {
                "error": "Account not verified",
                "message": "Please verify your account before continuing."
            }
        )
    )


    # Book errors

        app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            {
                "error": "Book not found",
                "message": "The requested book was not found."
            }
        )
    )


    # Tag errors

        app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status.HTTP_404_NOT_FOUND,
            {
                "error": "Tag not found",
                "message": "The requested tag was not found."
            }
        )
    )

        app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status.HTTP_409_CONFLICT,
            {
                "error": "Tag already exists",
                "message": "A tag with this name already exists."
            }
        )
    )
        @app.exception_handler(500)
        async def internal_error(request: Request, exc: Exception):
            return JSONResponse(
                content={
                    "error": "Internal Server Error",
                    "message": "Something went wrong on the server.",
                    "details":str(exc)
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        @app.exception_handler(404)
        async def internal_error(request: Request, exc: Exception):
            return JSONResponse(
                content={
                    "error": "Internal Server Error",
                    "message": "Opps Something went wrong on the server."
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
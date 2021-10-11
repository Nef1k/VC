from enum import Enum


class ResponseError(Enum):
    """Possible error codes and their respective messages."""

    UNKNOWN_ERROR = 'Unknown error'
    INVALID_CREDENTIALS = 'Invalid username or password'
    INVALID_CONTACT = 'Invalid contact'

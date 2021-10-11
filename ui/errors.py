from enum import Enum


class ResponseError(Enum):
    UNKNOWN_ERROR = 'Unknown error'
    INVALID_CREDENTIALS = 'Invalid username or password'
    INVALID_CONTACT = 'Invalid contact'

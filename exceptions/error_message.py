from rest_framework import status
from enum import Enum


class ErrorCodes(Enum):
    UNAUTHORIZED = 1
    INVALID_INPUT = 2
    NOT_FOUND = 3
    VALIDATION_FAILED = 4
    USER_ALREADY_EXIST = 5
    USER_DOES_NOT_EXIST = 6
    INCORRECT_PASSWORD = 7

error_messages = {
    1: {"result": "Unauthorized access", "http_status": status.HTTP_401_UNAUTHORIZED},
    2: {"result": "Invalid input provided", "http_status": status.HTTP_400_BAD_REQUEST},
    3: {"result": "Resource not found", "http_status": status.HTTP_404_NOT_FOUND},
    4: {"result": "Validation failed", "http_status": status.HTTP_400_BAD_REQUEST},
    5: {"result": "This user already exist", "http_status": status.HTTP_400_BAD_REQUEST},
    6: {"result": "This user does not exist", "http_status": status.HTTP_400_BAD_REQUEST},
    7: {"result": "Password is incorrect", "http_status": status.HTTP_400_BAD_REQUEST}
}

def get_error_message(code):
    return error_messages.get(code, 'Unknown error')
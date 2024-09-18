from .models import User
from exceptions.exception import CustomApiException
from exceptions.error_message import ErrorCodes


def login_validation(data):
    user = User.objects.filter(username=data.get("username")).first()
    if not user:
        raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST)
    if data.get('password') != user.password:
        raise CustomApiException(error_code=ErrorCodes.INCORRECT_PASSWORD)
    return user
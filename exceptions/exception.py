from rest_framework.exceptions import APIException
from .error_message import get_error_message


class CustomApiException(APIException):

    def __init__(self, error_code=None, message=None, ok=False):
        error_detail = get_error_message(error_code.value)
        self.status_code = error_detail['http_status']
        detail_message = message if message else error_detail['result']
        self.detail = {
            'detail': detail_message,
            'ok': ok,
            'result': '',
            'error_code': error_code.value,
        }
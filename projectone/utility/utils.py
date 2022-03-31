
import phonenumbers
from django.core.exceptions import ValidationError
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


def success_response(data=None, message=None, extra_data={}):
    result = {'status': {'code': 200, 'message': message},
              'data': data
              }
    result.update(extra_data)
    return JsonResponse(result)


def error_response(data=None, message=None, code=403,   errors=[]):
    result = {'status': {'code': code, 'message': message},
              'data': data,
              'errors': errors
              }

    return JsonResponse(result, status=code)


def validation_error_response(errors=[]):
    customized_response = []
    for key, value in errors.detail.items():
        error = {'field': key, 'message': value}
        customized_response.append(error)
    return error_response(message="Validation error", errors=customized_response, code=400)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'AUTH_HEADER_TYPES': settings.SIMPLE_JWT['AUTH_HEADER_TYPES'],
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

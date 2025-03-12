import json
import logging
from functools import wraps
from django.http import JsonResponse

logger= logging.getLogger('django')

def handle_exceptions(view_func):
    """Handles exceptions in routes."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except json.JSONDecodeError as decode_err:
            logger.error(f'Error decoding JSON in request body: {str(decode_err)}')
            return JsonResponse({
                'error':'Invalid JSON format in request body.'
            }, status=400)
        except Exception as exc:
            logger.error(f'An internal server error occurred: {str(exc)}', exc_info=True)
            return JsonResponse({
                'error':f'An internal server error occurred: {str(exc)}. Please try again later.'
            }, status=500)

    return wrapper
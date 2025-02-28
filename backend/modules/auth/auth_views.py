import json
import logging
from django.http import JsonResponse
from config.settings.session_manager import get_db_session
from modules.auth.auth_models import ClientUser
from utils.hashing.password_hasher import hash_password
from utils.tokens.generate_token import generate_token

logger= logging.getLogger('django')

# Registration route
def register(request):
    """
    Handles user registrations.
    :param request: Expected valid request method for route.
    :return: JsonResponse confirming user registration or denying it.
    """
    if request.method!='POST':
        logger.error(f'Request method invalid: expected "POST", got {request.method}')
        return JsonResponse({
            'error':'Invalid request method!'
        }, status=405)

    try:
        data= json.loads(request.body)
        first_name= data.get('first_name')
        last_name= data.get('last_name')
        email= data.get('email')
        password= data.get('password')

        # Validate fields if not empty
        for field in data:
            if not field:
                return JsonResponse({
                    'error':'Some fields are required!\n'
                }, status=400)

        # Check if user exists in database by querying email:
        # if true, return JsonResponse denying registration request with this email.
        with get_db_session() as session:
            if session.query(ClientUser).filter_by(email=email).first():
                return JsonResponse({
                    'error':'User by this email already exists!'
                }, status=401)

        # if not, send user an email with link to confirmation route to confirm address.
        # function returns boolean if link is confirmed
        # email should be valid for 1 hour. if confirmation doesn't happen, kill link validity.
        # if email link is confirmed, register new User model instance to database.

        newClient= ClientUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hash_password(password),
        )
        session.add(newClient)

        logger.info(f'New user registered.')
        return JsonResponse({
            'message':'New user registered successfully!'
        }, status= 201)

    except Exception as exc:
        #logger.error(f'An internal error occurred during user registration: {str(exc.__annotations__)}')
        return JsonResponse({
            'error':f'An internal error occurred: {str(exc)} Please try again later.'
        }, status=500)


def login(request):
    """
    Handles user login requests.
    :param request: Expected valid request method for route.
    :returns: JSON response confirming or denying user login request.
    """

    if request.method!='GET':
        logger.error(f'Invalid method: expected "POST", got {request.method} instead.')
        return JsonResponse({
            'error':'Invalid method!'
        }, status=405)

    _data= json.loads(request.body)
    _email= _data.get('email')
    _password= _data.get('password')

    for field in _data:
        if not field:
            return JsonResponse({
                'error':'Some fields are still required!\n',
            }, status=400)

    try:
        with get_db_session() as session:
            if not session.query(ClientUser).filter_by(email=_email) or not session.query(ClientUser).filter_by(password_hash=_password):
                return JsonResponse({
                    'error':'Invalid credentials!'
                }, status=400)

        # generate token
        token= generate_token(_email)
        # redirect to dashboard

        return JsonResponse({
            'message':'Login successful!',
            #'token': token,
        }, status=200)

    except Exception as exc:
        logger.error(f'An internal error occurred while logging in: {str(exc)}')
        return JsonResponse({
            'error':f'An internal server error occurred: {str(exc)}.\n  Please try again later.'
        }, status=500)


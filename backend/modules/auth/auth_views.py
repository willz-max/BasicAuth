import json
import logging
from django.http import JsonResponse
from config.settings.session_manager import get_db_session
from modules.auth.auth_models import ClientUser
from utils.hashing.password_hasher import hash_password

logger= logging.getLogger('django')

# Registration route
def register(request):
    """
    Handles user registrations.
    :param request: Expected valid request method for route.
    :return: JsonResponse confirming employee registration or denying it.
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

        # Validating fields if not empty
        for field in data:
            if not field:
                return JsonResponse({
                    'error':'Some fields are required!\n'
                })

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
        #logger.error(f'An internal error occurred during user registration: {str(exc.__class__.__annotations__)}')
        return JsonResponse({
            'error':f'An internal error occurred: {str(exc)} Please try again later.'
        }, status=400)


print(type(hash_password))  # Should print True
from utils import hashing

print("hash_password from hashing module:", hasattr(hashing, "hash_password"))  # Should print True
print("Type of hash_password:", type(hash_password))  # Should print <class 'function'>
print("Contents of hashing module:", dir(hashing))  # Should list 'hash_password'

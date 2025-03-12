import json
import logging
from django.http import JsonResponse
from config.settings.session_manager import get_db_session
from modules.auth.auth_models import ClientUser
from utils.handlers.errors.error_handlers import handle_exceptions
from utils.hashing.password_hasher import hash_password, verify_password
from utils.tokens.generate_token import generate_token, generate_verification_token, send_verification_email

logger= logging.getLogger('django')

def validate_request_data(data, required):
    """
    Validates that all required fields are present and not empty.
    :param data: Requested data.
    :param required: Required fields.
    """
    missing_fields= [field for field in required if not data.get(field)]
    if missing_fields:
        return False, f'Missing required fields: {', '.join(missing_fields)}'
    return True, None

def validate_email(email:str):
    """Validates email format."""
    if '@' not in email or '.' not in email:
        return JsonResponse({
            'error':'Invalid email format!',
        }, status=400)
    return None

def validate_password(password:str):
    """Validates password format."""
    if len(password)<8:
        return JsonResponse({
            'error':'Password must be at least 8 characters.'
        }, status=400)
    return None


# Registration route
@handle_exceptions
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

        required=[
            'first_name', 'last_name', 'email', 'password'
        ]
        is_valid, error_message= validate_request_data(data, required)
        if not is_valid:
            return JsonResponse({
                'error':error_message,
            }, status=400)

        first_name= data.get('first_name')
        last_name= data.get('last_name')
        email= data.get('email')
        password= data.get('password')

        email_isValid= validate_email(email)
        password_isValid= validate_password(password)
        if email_isValid and password_isValid:
            return email_isValid, password_isValid

        # Check if user exists in database by querying email:
        # if true, return JsonResponse denying registration request with this email.
        with get_db_session() as session:
            if session.query(ClientUser).filter_by(email=email).first():
                return JsonResponse({
                    'error':'User by this email already exists!'
                }, status=409)

        ## if not, send user an email with link to confirmation route to confirm address.
        ## function returns boolean if link is confirmed
        ## email should be valid for 1 hour. if confirmation doesn't happen, kill link validity.
        ## if email link is confirmed, register new User model instance to database.

        newClient= ClientUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=hash_password(password),
        )
        session.add(newClient)
        session.commit()

        verif_token= generate_verification_token(email)
        #email_sent= send_verification_email(email, verif_token)
        email_sent= 'sent'

        logger.info(f'New user registered: {email}')
        return JsonResponse({
            'message':'New user registered successfully!',
            'user_id': newClient.id,
            'email_sent': email_sent,
        }, status= 201)

    except Exception as exc:
        #logger.error(f'An internal error occurred during user registration: {str(exc.__annotations__)}')
        return JsonResponse({
            'error':f'An internal error occurred: {str(exc)} Please try again later.'
        }, status=500)

# Login route
@handle_exceptions
def login(request):
    """
    Handles user login requests.
    :param request: Expected valid request method for route.
    :returns: JSON response confirming or denying user login request.
    """

    if request.method!='POST':
        logger.error(f'Invalid method: expected "POST", got {request.method} instead.')
        return JsonResponse({
            'error':'Invalid method!'
        }, status=405)

    data= json.loads(request.body)

    required= [
        'email', 'password'
    ]
    is_valid, error_message= validate_request_data(data=data, required=required)
    if not is_valid:
        return JsonResponse({
            'error':error_message,
        }, status=400)

    email= data.get('email')
    password= data.get('password')

    try:
        with get_db_session() as session:
            user= session.query(ClientUser).filter_by(email=email).first()
            if not user or not verify_password(password, user.password_hash):
                return JsonResponse({
                    'error':'Invalid credentials!'
                }, status=401)

            # generate token
            token= generate_token(email)

            ## redirect to dashboard

            # Update last login stamp
            #user.updated_at= datetime.now()
            session.commit()

            logger.info(f'User logged in successfully: {email}')
            return JsonResponse({
                'message':'Login successful!',
                'token': token,
            }, status=200)

    except Exception as exc:
        logger.error(f'An internal error occurred while logging in: {str(exc)}')
        return JsonResponse({
            'error':f'An internal server error occurred: {str(exc)}. Please try again later.'
        }, status=500)
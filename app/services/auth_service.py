import bcrypt
from app.schemas.user import SignupRequest, SignupResponse, LoginRequest
from app.database import connection
from app.models.user import INSERT_USER, LOGIN_USER
import psycopg2

def create_user(data: SignupRequest) -> SignupResponse:
    cursor = connection.cursor()
    try:
        hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

        cursor.execute(
            INSERT_USER,
            (data.first_name, data.last_name, data.email, hashed_password)
        )
        user_id, first_name, last_name, email = cursor.fetchone() 
        connection.commit()
    except psycopg2.errors.UniqueViolation:
        connection.rollback()
        raise ValueError("Email already registered")
    except Exception as e:
        connection.rollback()
        raise e
    
    return SignupResponse(id=user_id, first_name=first_name, last_name=last_name, email=email)

def login_user(data: LoginRequest) -> SignupResponse:
    cursor = connection.cursor()
    cursor.execute(LOGIN_USER, (data.email,))
    
    result = cursor.fetchone()
    if result is None:
        raise ValueError("User not found")
    
    user_id, first_name, last_name, email, user_password = result
    if not bcrypt.checkpw(data.password.encode(), user_password.encode()):
        raise ValueError("Invalid password")

    return SignupResponse(id=user_id, first_name=first_name, last_name=last_name, email=email)
        


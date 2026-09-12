import bcrypt
from app.schemas.user import SignupRequest, SignupResponse
from app.database import connection
from app.models.user import INSERT_USER

def create_user(data: SignupRequest) -> SignupResponse:
    cursor = connection.cursor()
    hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

    cursor.execute(
        INSERT_USER,
        (data.first_name, data.last_name, data.email, hashed_password)
    )
    user_id, first_name, last_name, email = cursor.fetchone() 
    connection.commit()
    
    return SignupResponse(id=user_id, first_name=first_name, last_name=last_name, email=email)


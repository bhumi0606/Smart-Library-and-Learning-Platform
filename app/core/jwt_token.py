
from datetime import datetime,timedelta
from fastapi import HTTPException, status
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from app.core.config import ACCESS_TOKEN_TIME, ALGORITHM, REFRESH_TOKEN_TIME, SECRET_KEY
from app.schemas.member.TokenData import TokenData

def create_access_token(data:TokenData, refresh_token=False):
    payload = {
        'email': data.email,
        'role': data.role,
        'type': "refresh" if refresh_token else "access",
        'exp': datetime.utcnow()+timedelta(days=REFRESH_TOKEN_TIME if refresh_token else ACCESS_TOKEN_TIME)
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm = ALGORITHM
    )
    return token

def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms = [ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    

def create_refresh_token(token):
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only an access token can be refreshed",
        )
    data = TokenData(
        email=payload.get("email"),
        role=payload.get("role"),
    )

    return create_access_token(
        data,
        refresh_token=True,
    )
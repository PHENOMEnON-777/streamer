from datetime import timedelta, timezone ,datetime
from jose import JWTError,jwt
from .schemas import TokenData
from core.config import get_settings

settings = get_settings()




def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_referesh_token(data:dict,):
    to_encode = data.copy()
    encode_jwt = jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encode_jwt


def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user_id: str = payload.get("id") 
        if email is None or user_id is None:
            raise credentials_exception
        return TokenData(email=email,id=user_id)
    except JWTError:
        raise credentials_exception

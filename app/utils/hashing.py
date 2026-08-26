
from passlib.context import CryptContext

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(password,hashed_password):
    if password_context.verify(password,hashed_password):
        return True

def hash_password(password):
    return password_context.hash(password)
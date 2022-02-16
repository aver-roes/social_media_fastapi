# NOTE: this file is used to hold some utility functions

from passlib.context import CryptContext


# informing passlib the hash algorithm used to hash passwords
pws_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pws_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    return pws_context.verify(plain_password, hashed_password)

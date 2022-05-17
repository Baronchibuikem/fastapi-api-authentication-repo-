from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password )


def values_equal(value_one:any, value_two:any) -> bool:
    return value_one == value_two
from fastapi import status, HTTPException, Depends, APIRouter, Response
from app.models.user_model import User
from app.database.db_config import get_db
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse, ChangePassword
from app.utils.user_utils import hash_password, values_equal, verify
from app.utils.oauth2 import get_current_user, create_access_token
from app.schemas.token_schema import Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/user",
    tags=["users"]
)



@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # generate a token for the user
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a User."""
    # hash the password
    user.password = hash_password(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)) -> UserResponse:
    """Get a user by id."""
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    return user


@router.put("/change-password", status_code=status.HTTP_200_OK, response_model=UserResponse)
def change_password(password_data:ChangePassword, db: Session = Depends(get_db), 
            current_user: int = Depends(get_current_user)):
    """Change your password."""

    # check that new_password and confirm_password match
    response = values_equal(password_data.new_password, password_data.confirm_new_password)
    if not response:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"your passwords do not match")

    # check that user exist
    user_query = db.query(User).filter(User.email==current_user.email)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not found")

    # check that current password is equal to current save password in db
    password_match = verify(password_data.current_password, current_user.password)
    if not password_match:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"your saved password doesn't match with the current password you enter")

    # hash the new password
    passwordhashed = hash_password(password_data.new_password)

    # update user with new password
    user_query.update({"password":passwordhashed})
    db.commit()
    return Response(status_code=status.HTTP_200_OK,)

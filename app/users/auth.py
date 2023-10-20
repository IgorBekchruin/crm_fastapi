from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from app.pages.oauth_class import OAuth2PasswordBearerWithCookie

from app.users.jwt import create_jwt_token, verify_jwt_token
from app.users.models import User
from app.users.schemas import UserCreate, UserSave, UserSchem
from app.users.user_dao import UserDAO


router = APIRouter(
    prefix='/api/v1/auth',
    tags=['Auth']
)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    user = UserSave(**{
        "username": user.username,
        "hashed_password": hashed_password,
    })
    await UserDAO.add(user)
    return {'user'}


@router.post("/login")
async def authenticate_user(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserDAO.find_user(form_data.username)  # Получите пользователя из базы данных
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(form_data.password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt_token({"sub": user.username})
    response.set_cookie(key='access_token', value=f"Bearer {jwt_token}", httponly=True)
    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/auth/login", status_code=302)
    response.delete_cookie(key='access_token')
    return response


async def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await UserDAO.find_user(decoded_data["sub"])  # Получите пользователя из базы данных
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user


def has_role(role: str):
    def role_validator(current_user: User = Depends(get_current_user)):
        if role not in current_user.roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_validator

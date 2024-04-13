from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.depends import get_db_session
from app.auth_user import UserUseCases
from app.schemas import User

router = APIRouter(prefix='/user')

@router.post('/register')
def user_register(user: User, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    uc.user_register(user=user)

    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )

@router.post('/login')
def user_login(
    login_request_form: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    uc = UserUseCases(db_session=db_session)
    user = User(
        username=login_request_form.username,
        password=login_request_form.password
    )

    token_data = uc.user_login(user=user, expires_in=60)
    return JSONResponse(
        content=token_data,
        status_code=status.HTTP_200_OK
    )
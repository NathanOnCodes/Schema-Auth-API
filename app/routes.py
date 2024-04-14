from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.depends import get_db_session, token_verifier
from app.auth_user import UserUseCases
from app.schemas import User

user_router = APIRouter(prefix='/user')
test_router = APIRouter(prefix='/test', dependencies=[Depends(token_verifier)])

@test_router.post('/register')
def user_register(user: User, db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    uc.user_register(user=user)

    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )

@test_router.post('/login')
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

@test_router.get('/test')
def test_user_verify():
    return 'It works'
from datetime import timedelta
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser, VerifySuperUserDep, temp_code_verify
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import Message, NewPassword, Token, UserPublic
from app.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
    validate_refresh_token,
    credentials_exception
)

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    print("\n\n settings.ACCESS_TOKEN_EXPIRE_MINUTES \n\n ", settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        refresh_token=security.create_access_token(
            user.email, expires_delta=refresh_token_expires
        ),
        expires_in=(settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    )
    print("\n\n token_data \n\n ", token_data)
    return token_data

@router.post("/oauth/token", response_model=Token)
def tokens_manager_oauth_codeflow(
    session: SessionDep,
    grant_type: str = Form(...),
    refresh_token: Optional[str] = Form(None),
    code: Optional[str] = Form(None)
):
    """
    Token URl For OAuth Code Grant Flow

    Args:
        grant_type (str): Grant Type
        code (Optional[str], optional)
        refresh_token (Optional[str], optional)

    Returns:
        access_token (str)
        token_type (str)
        expires_in (int)
        refresh_token (str)
    """
    # Token refresh flow
    if grant_type == "refresh_token":
        # Check if the refresh token is Present
        if not refresh_token:
            raise credentials_exception
        # Validate the refresh token and client credentials
        user_email = validate_refresh_token(refresh_token)
        user = crud.get_user_by_email(
        session=session, email=user_email['sub']
        )
        if not user:
            raise credentials_exception

    # Initial token generation flow
    elif grant_type == "authorization_code":
        if not code:
            raise credentials_exception
        user = temp_code_verify(session, token=code)
        if not user:
            raise credentials_exception
    else:
        raise credentials_exception

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    print("\n\n settings.ACCESS_TOKEN_EXPIRE_MINUTES \n\n ", settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        refresh_token=security.create_access_token(
            user.email, expires_delta=refresh_token_expires
        ),
        expires_in=(settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    )

    print("\n\n token_data \n\n ", token_data)
    return token_data
    
@router.get("/oauth/temp-code")
def get_temp_code(user_id: int, super_user: VerifySuperUserDep):
    """
    Get Temp Code against user_id to implentent OAuth2 for Custom Gpt

    Args:
        user_id 

    Returns:
        code (str): Temp Code
    """
    access_token_expires = timedelta(minutes=3)
    code = security.create_access_token(
            super_user.id, expires_delta=access_token_expires
        ),
    return {"code": code[0]}


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    """
    Password Recovery
    """
    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    return Message(message="Password updated successfully")


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    user = crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )

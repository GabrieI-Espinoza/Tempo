from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError

from app.core.security import decode_access_token
from app.tortoise.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    """Resolve the authenticated user from a bearer access token."""

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise credentials_exception()

    try:
        payload = decode_access_token(credentials.credentials)
        if payload.get("type") != "access":
            raise credentials_exception()

        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception()

        user_id = UUID(sub)
    except (PyJWTError, ValueError):
        raise credentials_exception()

    user = await User.get_or_none(user_id=user_id)
    if user is None:
        raise credentials_exception()

    return user

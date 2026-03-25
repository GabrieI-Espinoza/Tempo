from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import uuid
from jwt import PyJWTError

from app.core.security import decode_access_token
from app.tortoise.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Check if scheme is Bearer, and that credentials are provided
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise credentials_exception

    # Extract the JWT token
    token = credentials.credentials

    try:
        # Decode the JWT token
        payload = decode_access_token(token)

        # Extract token type from payload
        token_type = payload.get("type")
        # Verify token type
        if token_type != "access":
            raise credentials_exception

        # Extract user_id from payload
        sub = payload.get("sub")
        # Ensure user_id is present
        if not sub:
            raise credentials_exception

        # Convert user_id to UUID
        user_id = uuid.UUID(sub)
    except (ValueError, PyJWTError):
        # Handle invalid UUID or JWT errors
        raise credentials_exception

    # Verify user exists in the database
    user = await User.get_or_none(user_id=user_id)
    if user is None:
        raise credentials_exception

    return user

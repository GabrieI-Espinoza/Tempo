from slowapi import Limiter
from slowapi.util import get_remote_address

# Rate limiter keyed by client IP, shared across routes
limiter = Limiter(key_func=get_remote_address)

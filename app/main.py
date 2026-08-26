from fastapi import FastAPI

from app.api.router import api_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limiter import limiter

app = FastAPI(
    title="Smart Library & Learning Platform"
)

app.include_router(api_router)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)
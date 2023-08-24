from fastapi import Depends, FastAPI, Request

from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.bearer import AuthCookie


from app.database import get_session, get_user
from app.database import init_models

from app.auth.codec import decodeAuthToken

from app.auth.router import router_login, router_register

app = FastAPI(title="FN")

@app.on_event("startup")
async def init_tables():
    await init_models()

@app.get("/")
async def mainPages(request: Request, session: AsyncSession = Depends(get_session)):
    cookie = decodeAuthToken(request)
    if cookie is not None:
        return f"hello world {cookie.get('user_id')}"
    return "hello world"


app.include_router(
    router_login,
    tags="A"
)

app.include_router(
    router_register,
    tags="A"
)

@app.get("/test", dependencies=[Depends(AuthCookie())])
def test():
    return "good"
from fastapi import APIRouter, Body, Response

from app.database import get_user, create_user

from app.auth.codec import signJWT

from app.models import UserLoginSchema, UserRegisterSchema

router_login = APIRouter(
)

router_register = APIRouter(
)


@router_login.post("/login")
async def login(response: Response, userData: UserLoginSchema = Body(...)):
    user = await get_user(userData.login)
    if user is not None:
        if user.password == userData.password:
            token = signJWT(user.login)
            response.set_cookie(key="auth", value=token["access_token"])
            return "Successfully authorized"
    return False


@router_register.post("/register")
async def register(user: UserRegisterSchema = Body(...)):
    if await get_user(user.login) is None:
        await create_user(user.login, user.password)
        return "User registered"
    return "User not registered"

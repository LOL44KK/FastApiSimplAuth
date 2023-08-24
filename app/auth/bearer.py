from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.codec import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


class AuthCookie(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request):
        auth_token = self.extract_token(request)
        if auth_token:
            if not self.verify_jwt(auth_token):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return auth_token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
        
    def extract_token(self, request: Request) -> str:
        auth_token = None
        if "auth" in request.cookies:
            auth_token = request.cookies["auth"]
        if not auth_token and "authorization" in request.headers:
            auth_header = request.headers["authorization"]
            scheme, credentials = auth_header.split(None, 1)
            if scheme.lower() == "bearer":
                auth_token = credentials
        return auth_token
    
    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid = False
        try:
            payload = decodeJWT(jwtoken)
            if payload:
                is_token_valid = True
        except:
            pass
        return is_token_valid

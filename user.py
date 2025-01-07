from fastapi import FastAPI, Request, Response, Depends, HTTPException
from itsdangerous import URLSafeSerializer
from pydantic import BaseModel

app = FastAPI()

# Secret key for signing session data (keep this secure!)
SECRET_KEY = "your-secret-key"
serializer = URLSafeSerializer(SECRET_KEY)

# Session key
SESSION_COOKIE_NAME = "session_cookie"

# Example data model
class User(BaseModel):
    username: str
    email: str

# Dependency to get the current session
def get_session(request: Request):
    session_data = request.cookies.get(SESSION_COOKIE_NAME)
    if session_data:
        try:
            # Decode the session data
            return serializer.loads(session_data)
        except:
            # Invalid session data
            return {}
    return {}

# Dependency to set the session
def set_session(response: Response, session_data: dict):
    # Encode the session data
    session_cookie = serializer.dumps(session_data)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_cookie,
        httponly=True,  # Prevent client-side JavaScript access
        max_age=3600,   # Session expires after 1 hour
    )

# Route to set session data
@app.post("/login")
async def login(response: Response, user: User):
    # Create session data
    session_data = {"username": user.username, "email": user.email}
    # Set the session cookie
    set_session(response, session_data)
    return {"message": "Login successful"}

# Route to get session data
@app.get("/profile")
async def profile(session: dict = Depends(get_session)):
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"username": session.get("username"), "email": session.get("email")}

# Route to clear session data (logout)
@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"message": "Logout successful"}
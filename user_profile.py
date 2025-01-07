from fastapi import FastAPI, Request, Response, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory session storage
sessions = {}

# Dependency to get the current session
def get_session(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        return sessions[session_id]
    return {}

# Dependency to create or update a session
def set_session(response: Response, session_data: dict):
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    sessions[session_id] = session_data
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,  # Prevent client-side JavaScript access
        max_age=3600,   # Session expires after 1 hour
    )

# Route to render the form
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Route to handle form submission
@app.post("/submit")
async def submit_form(
    request: Request,
    response: Response,
    username: str = Form(...),
    email: str = Form(...),
):
    # Create session data
    session_data = {"username": username, "email": email}
    # Set the session
    set_session(response, session_data)
    return RedirectResponse(url="/profile", status_code=303)

# Route to display profile (session data)
@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request, session: dict = Depends(get_session)):
    if not session:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("profile.html", {"request": request, "session": session})

# Route to clear session (logout)
@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie("session_id")
    return RedirectResponse(url="/", status_code=303)
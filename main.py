from fastapi import FastAPI, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, Union, List
from datetime import datetime
import os
import agents


app = FastAPI()

# Mount static files (e.g., CSS, JS)
app.mount('/static', StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates (e.g html)
templates = Jinja2Templates(directory="templates")


#Limitations with using a global list variable instead of sessions (Skills, Tasks):

# The global list is stored in memory. If the server restarts or crashes, all data will be lost (Data Persistence)
# This approach doesn’t scale well for larger applications or distributed systems (e.g., multiple server instances) (Scalability).
# If multiple requests try to modify the global list simultaneously, you might run into race conditions or data corruption (Concurrency Issues).
# Using global variables can make your code harder to test, debug, and maintain (Global State Problem) .

# --> To avoid this, use a database: sqlite3, postgresql, MySQL...etc (+ sessions)

Skills = []
skill_id_counter = 1

class Skill(BaseModel):
    id: int
    name: str = None #default value
    mastery: int #percentage value
    date: datetime = Field(default_factory=datetime.now)
    # description: Optional[str] = None
    # category: Optional[str] = None
    # tags: List[str] = []
    # is_certified: bool = False
    # experience_years: float = 0.0
    # last_used: Optional[datetime] = None
    # priority: str = "Medium"
    # resources: List[str] = []
    
# skill = Skill(
#     id=1,
#     name="Python Programming",
#     mastery=85,
#     description="Proficient in Python for data analysis and web development.",
#     category="Programming",
#     tags=["Python", "Data Analysis", "Web Development"],
#     is_certified=True,
#     experience_years=3.5,
#     last_used=datetime(2023, 9, 15),
#     priority="High",
#     resources=["Fluent Python", "Real Python Tutorials"]
# )

Tasks = []
task_id_counter = 1
class Task(BaseModel):
    id: int
    name: str = Field(min_length=1)
    date: datetime = Field(default_factory=datetime.now)
    # priority: str = "Medium"
    # status: str = "Not Started"
    # due_date: Optional[datetime] = None
    # assigned_to: Optional[str] = None
    # tags: List[str] = []
    # estimated_time: float = 0.0
    # completed: bool = False
    # dependencies: List[int] = []
    # notes: Optional[str] = None
    # category: Optional[str] = None

# task = Task(
#     id=1,
#     name="Complete project report",
#     priority="High",
#     status="In Progress",
#     due_date=datetime(2023, 10, 15),
#     assigned_to="John Doe",
#     tags=["Work", "Urgent"],
#     estimated_time=8.5,
#     completed=False,
#     dependencies=[2, 3],
#     notes="Ensure all sections are reviewed before submission.",
#     category="Work"
# )

# Routes for Task Object 

# Dynamic HTML Rendering (Server-Side Rendering):

@app.get("/", response_class=HTMLResponse)
async def read_tasks(request: Request):
    return templates.TemplateResponse("task.html", {"request": request, "Tasks": Tasks})

@app.post("/")
async def add_task(content: str = Form(...)):
    global task_id_counter, Tasks
    task = Task(id=task_id_counter, name=content, date=datetime.now())
    Tasks.append(task)
    task_id_counter += 1
    return RedirectResponse(url="/", status_code=303)

@app.post("/update/{task_id}")
async def update_task(task_id: int, content: str = Form(...)):
    task = next((t for t in Tasks if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.name = content
    return RedirectResponse(url="/", status_code=303)

@app.get("/delete/{task_id}")
async def delete_task(task_id: int):
    global Tasks
    Tasks = [t for t in Tasks if t.id != task_id]
    return RedirectResponse(url="/", status_code=303)

# Routes for handling Skill Object:

# Dynamic HTML Rendering (Server-Side Rendering):

@app.get("/AddSkill", response_class=HTMLResponse)
async def render_html(request: Request):
    return templates.TemplateResponse("skill.html", {"request": request, "Skills": Skills})

@app.post("/AddSkill")
async def add_skill(content: str = Form(None), mastery: str = Form(None)):
    global skill_id_counter, Skills
    skill = Skill(id=skill_id_counter, name=content, mastery = int(mastery), date=datetime.now())
    Skills.append(skill)
    skill_id_counter += 1 
    return RedirectResponse(url="/AddSkill", status_code=303)

@app.post("/UpdateSkill/{skill_id}")
async def update_skill(skill_id: int, content: str = Form(None), mastery: str = Form(None)):
    skill = next((t for t in Skills if t.id == skill_id), None)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not Found!")
    skill.name = content
    skill.mastery = int(mastery)
    return RedirectResponse(url="/AddSkill", status_code=303)
    
@app.get("/DeleteSkill/{skill_id}")
async def delete_skill(skill_id: int):
    global Skills
    Skills = [s for s in Skills if s.id != skill_id]
    return RedirectResponse(url="/AddSkill", status_code=303)


# Routes for handling Experience Object:

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
DATA_PATH = 'uploads/'

## Route to serve the HTML form
@app.get("/Experience", response_class=HTMLResponse)
async def upload_form():
    with open("templates/experience.html", "r") as file:
        return HTMLResponse(content=file.read())
    
## Route to handle file upload
@app.post("/UploadFile")
async def upload_cv(cv: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, cv.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await cv.read())
        return RedirectResponse(url="/Experience", status_code=303)
        # return JSONResponse(content={"message": "File uploaded successfully!"}, status_code=200)
        # return {"message": f"File '{cv.filename}' uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

## RAG the CV:
@app.post("/ReadFile")
async def read_file(file):
    agents.create_vector_db(DATA_PATH)
    resp = agents.CV_QA(file)
    









# Routes for handling Output


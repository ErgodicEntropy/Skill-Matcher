from fastapi import FastAPI, HTTPException, Request, Path, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
from pydantic import BaseModel, Field
from typing import Optional, Union, List
from datetime import datetime, date
import time

app = FastAPI()

# Mount static files (e.g., CSS, JS)
app.mount('/static', StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates (e.g html)
templates = Jinja2Templates(directory="templates")



Skills = []

Tasks = []

class Skill(BaseModel):
    id: int
    name: str = None #default value
    mastery: float #percentage value
    date: date

class Experience(BaseModel):
    id : int
    name: str = None
    
class Task(BaseModel):
    id: int
    name: str
    date: datetime = datetime.now()

# Routes for Task Object 

# Dynamic HTML Rendering (Server-Side Rendering):

## POST METHOD        

@app.route('/', methods=['POST', 'GET'])
def addtask(request: Request, content: str = Form(None)):
    if request.method == "POST":
        idd = len(Tasks) + 1
        task = Task(id=idd, name=content, date=datetime.now().hour)
        Tasks.append(task)
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("task.html", {"request": request, "Tasks": Tasks})

## PUT METHOD        
@app.route("/UpdateTask/{task_id}", methods=["GET", "POST"])
async def update_task(request: Request, task_id: int, content: str = Form(None)):
    try:
        task =  next(task for task in Tasks if task.id == task_id)
    except StopIteration:
        raise HTTPException(status_code=404, details="Task not found!")

    if request.method == "POST":
        # Handle form submission
        task.name = content
        return RedirectResponse(url="/", status_code=303)

    # Render the update form (GET request)
    return templates.TemplateResponse("updatetask.html", {"request": request, "task": task})

## DELETE METHOD       
@app.route("/DeleteTask/{task_id}", methods=["POST", "GET"])
def delete_task(task_id: int, request: Request):
    if request.method == "POST":
        try:
            Tasks.pop(task_id-1)
            return RedirectResponse(url="/", status_code=303)            
        except StopIteration:
            raise HTTPException(status_code=404, detail="Task not found!")

@app.route("/finalize_tasks", methods=["POST"])
def finalize():
    return RedirectResponse(url="/skills_home", status_code=303)

# Routes for handling Skill Object:

# Static HTML Rendering (Client-Side Rendering):

@app.get('/skills_home')
def read():
    with open("templates/skill.html", "r") as file:
        return HTMLResponse(content=file.read())

## POST METHOD        
@app.post('/skills', response_model=Skill)
def add_task(skill: Skill):
    Skills.append(skill)
    return skill

## GET METHOD        
@app.get('/SkillList', response_model=list[Skill])
def get_tasklist():
    return Skills 

@app.get('/skills/{id}', response_model=Skill)
def get_task(id: int):
    try:
        skill = Skills[id-1]
        return skill
    except:
        raise HTTPException(status_code=404, detail="Skill not found!")


## PUT METHOD        
@app.put('/skills/{id}', response_model=Skill)
def update_task(id: int, updated_skill: Skill):
    for skill in Skills:
        if skill.id == id:
            skill.name = updated_skill.name
            skill.mastery = updated_skill.mastery
            return skill
    raise HTTPException(status_code=404, detail="Skill not found!")
        

## DELETE METHOD        
@app.delete("/skills/{id}")
def update_tasks(id: int):
    for skill in Skills:
        if skill.id == id:
            Skills.pop(id-1)
            return {"message": f"Skill {id} Deleted"}

    raise HTTPException(status_code=404, detail="Skill not found!")


# Routes for handling Experience Object:

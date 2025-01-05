from fastapi import FastAPI, HTTPException, Request, Path, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
from pydantic import BaseModel, Field
from typing import Optional, Union


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
    
class Experience(BaseModel):
    id : int
    name: str = None
    
class Task(BaseModel):
    id: int
    name: str
    priority: Optional[int]

# Routes for handling Skill Object:

## POST METHOD        
@app.post('/skill_create/{name}', response_model=Skill)
def add_task(name: str):
    idd = len(Skills) + 1
    skill = Skill(id=idd,name=name)
    Skills.append(skill)
    return Skills

## GET METHOD        
@app.get('/skills_get', response_model=list[Skill])
def get_tasklist():
    return Skills 

@app.get('/skill_get/{id}', response_model=Skill)
def get_task(id: int):
    try:
        skill = Skills[id-1]
        return skill
    except:
        raise HTTPException(status_code=404, detail="Skill not found!")


## PUT METHOD        
@app.put('/skill_update/{id}')
def update_task(id: int, name: str):
    try:
        skill = Skills[id-1]
        skill.name = name
    except:
        raise HTTPException(status_code=404, detail="Skill not found!")
        

## DELETE METHOD        
@app.delete("/skill_delete/{id}")
def update_tasks(id: int):
    try:
        Skills.pop(id-1)
    except:
        raise HTTPException(status_code=404, detail="Skill not found!")



#display Skills List
@app.post("/displayskill", response_class=HTMLResponse)
async def read_root(request: Request, message):
    return templates.TemplateResponse("skill.html", {"request": request, "message": message})


# Routes for Task Object 


## POST METHOD        
@app.post('/task_create/{name}', response_model=Task)
def add_task(name: str):
    idd = len(Tasks) + 1
    task = Task(id=idd,name=name)
    Tasks.append(task)
    return Tasks

## GET METHOD        
@app.get('/tasks_get', response_model=list[Task])
def get_tasklist():
    return Tasks 

@app.get('/task_get/{id}', response_model=Task)
def get_task(id: int):
    try:
        task = Tasks[id-1]
        return task
    except:
        raise HTTPException(status_code=404, detail="Task not found!")


## PUT METHOD        
@app.put('/task_update/{id}')
def update_task(id: int, name: str):
    try:
        task = Tasks[id-1]
        task.name = name
    except:
        raise HTTPException(status_code=404, detail="Task not found!")
        

## DELETE METHOD        
@app.delete("/task_delete/{id}")
def update_tasks(id: int):
    try:
        Skills.pop(id-1)
    except:
        raise HTTPException(status_code=404, detail="Task not found!")



#display Tasks List
@app.post("/displaytask", response_class=HTMLResponse)
async def read_root(request: Request, message):
    return templates.TemplateResponse("task.html", {"request": request, "message": message})






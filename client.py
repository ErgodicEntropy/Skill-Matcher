import requests
import asyncio

#HTTP Requests: METHOD, URL, HEADERS, PAYLOAD/BODY and STATUS CODE


#Add Skills
try:
    N = int(input("enter the number of skills:"))
except ValueError:
    print("Invalid input. Please enter a number.")
    exit()
    
for k in range(N):
    X = str(input("Enter the name of the skill:"))
    skillresp  = requests.post(f'http://127.0.0.1:8000/skill/{X}')
    if skillresp.status_code == 200:
        print(f"added Skill {X}", skillresp.json())
    else:
        print(f"failed to add Skill {X}", skillresp.json())
        
        
#Retrieve Skills

resp = requests.get('http://127.0.0.1:8000/')
Skills = resp.json()

for k in range(len(Skills)):     
    retrievedresp = requests.get(f'http://127.0.0.1:8000/skills/{k}')
    if retrievedresp.status_code == 200:
        print(f"Skill at index {k}:", retrievedresp.json())
    else:
        print(f"Failed to retrieve skill at index {k}:", retrievedresp.json())
        
#Get Skills list

SkillList = requests.get('http://127.0.0.1:8000/') 
print("Skill List", SkillList.json())


from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.import_requests import analyze_prompt  # Make sure to import your function

app = FastAPI()

# Add CORS middleware after creating the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production, e.g., ["http://example.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods like GET, POST, PUT, DELETE
    allow_headers=["*"],  # Allows all headers
)

class TaskInput(BaseModel):
    task: str
    url: str #adding a field for the url 

@app.post("/submit")
async def receive_task(task_input: TaskInput):
    analyze_prompt(task_input.task, task_input.url)  # Pass the URL to your function
    return {"received_task": task_input.task, "url": task_input.url}
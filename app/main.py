from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from app.tasks import execute_task
from app.utils import read_file_content

app = FastAPI()

class TaskRequest(BaseModel):
    task: str

@app.post("/run")
async def run_task(task_request: TaskRequest):
    task = task_request.task
    try:
        result = execute_task(task)
        return {"status": "success", "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file(path: str):
    # Ensure the path starts with /data/
    if not path.startswith("/data/"):
        raise HTTPException(status_code=400, detail="Access to this path is not allowed")
    try:
        # Convert the path to the actual file system path
        actual_path = os.path.join("C:/data", path[len("/data/"):])
        content = read_file_content(actual_path)
        return {"status": "success", "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
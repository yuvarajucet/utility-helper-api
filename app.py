import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import dotenv
import os
dotenv.load_dotenv()

from Controller.YoutubeController import youtuber

app = FastAPI()

app.include_router(youtuber)

app.add_middleware(
    CORSMiddleware,
    allow_origins = os.getenv("origin"),
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
async def index():
    return {
        "message" : "API running..."
    }


if __name__ == "__main__":
    uvicorn.run(app=app)
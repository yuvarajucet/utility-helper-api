import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import dotenv
import os

from Controller.YoutubeController import youtuber
from Controller.TruecallerController import truecaller

dotenv.load_dotenv()
app = FastAPI()

app.include_router(youtuber)
app.include_router(truecaller)

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
        "message" : "API version 2.0 running..."
    }


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", app=app)

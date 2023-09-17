import os
import datetime
from fastapi import APIRouter, Request, Response
from fastapi.responses import FileResponse
from Model.YoutubeData import YoutubeRequestModel
from Helper.YoutubeHelper import YoutubeHelper

youtuber = APIRouter(
    prefix="/api/v1/youtube",
    tags=["youtube"],
    responses={404: {"message": "Not found"}}
)

@youtuber.post("/download", tags=["youtube"])
async def download(request: Request, resp: Response, info: YoutubeRequestModel):
    deleteOldItems()
    resp = YoutubeHelper.VideoDownloader(YoutubeHelper,info)
    return resp

@youtuber.get("/download/{type}/{url}", tags=["youtube"])
async def download(type,url):
    path = os.getcwd() + "/downloads/" + url
    if os.path.exists(path):
        if type == "mp4":
            return FileResponse(path = path, filename = YoutubeHelper.GetFileTitleByID(url), media_type = "application/mp4")
        elif type == "mp3":
            return FileResponse(path = path, filename = YoutubeHelper.GetFileTitleByID(url), media_type = "application/mp3")
    
    return {
        "status": False,
        "message": "File not found"
    }

def deleteOldItems():
    folderPath = os.getcwd() + "/downloads/"
    currentTime = datetime.datetime.now()
    for filename in os.listdir(folderPath):
        filePath = os.path.join(folderPath, filename)

        if os.path.exists(filePath):
            modifiedTime = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))
            timeDiff = currentTime - modifiedTime

            if timeDiff.total_seconds() > 600:
                os.remove(filePath)

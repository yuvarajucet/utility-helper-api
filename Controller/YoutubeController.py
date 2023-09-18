import os
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
async def download(info: YoutubeRequestModel):
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

@youtuber.get("/get-data", tags=["youtube"])
async def getData():
    resp = YoutubeHelper.GetTotalYoutubeUsage(YoutubeHelper)
    return resp
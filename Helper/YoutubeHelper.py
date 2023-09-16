import json
from Model.YoutubeData import YoutubeRequestModel, YoutubeResponseModel, DownloadDataDB
from pytube import YouTube as YT
import os
import uuid

class YoutubeHelper:

    def __init__(self) -> None:
        pass

    def VideoDownloader(self, info: YoutubeRequestModel) -> YoutubeResponseModel:
        try:
            instance = YT(info.url)
            downloadId = self.getGuid()
            title = instance.title
            downloadPath = './downloads/'
            
            if info.type == "mp4":
                targetVideoFile = instance.streams.get_highest_resolution()
                targetVideoFile.download(output_path = downloadPath, filename = downloadId + ".mp4")
            
            elif info.type == "mp3":
                audio_streams = instance.streams.filter(only_audio=True)
                bestQualityAudio = audio_streams[0]
                for stream in audio_streams:
                    if stream.abr > bestQualityAudio.abr:
                        bestQualityAudio = stream
                bestQualityAudio.download(output_path = downloadPath, filename = downloadId + ".mp3")

            response: YoutubeResponseModel = {
                "status": True,
                "message": "Video found",
                "url": os.getenv("APIServer") + "/api/v1/youtube/download/" + info.type + "/" + downloadId + "." + info.type,
                "title": title
            }
            self.ReadOrWriteData({"id": downloadId, "title": title, "type": info.type})
            return response

        except Exception as ex:
            response: YoutubeResponseModel = {
                "status": False,
                "message": "Failed to download",
                "url": "Null",
                "title": "Null"
            }
            return response

    def getGuid():
        return str(uuid.uuid4())
    
    def ReadOrWriteData(info: DownloadDataDB):
        try:
            with open("./Data/downloadData.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        
        data.append(info)

        with open("./Data/downloadData.json", "w") as file:
            json.dump(data, file, indent = 4)

    def GetFileTitleByID(fullId: str) -> str:
        try:
            with open("./Data/downloadData.json", "r") as file:
                data: DownloadDataDB = json.load(file)
        except FileNotFoundError:
            data = []

        uniqId = fullId.split(".")[0]
        for info in data:
            if info["id"] == uniqId:
                return info["title"]
        return "File"
        
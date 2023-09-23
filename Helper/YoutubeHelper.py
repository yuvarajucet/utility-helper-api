import json
import datetime
from Model.YoutubeData import YoutubeRequestModel, YoutubeResponseModel, DownloadDataDB, TotalDataResponse
from pytube import YouTube as YT
import os
import uuid

class YoutubeHelper:

    def __init__(self) -> None:
        pass

    def VideoDownloader(self, info: YoutubeRequestModel) -> YoutubeResponseModel:
        self.deleteOldItems()
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

            contentType = "Video" if info.type == "mp4" else "Audio"
            response: YoutubeResponseModel = {
                "status": True,
                "mideaType": info.type,
                "message": "{0} found".format(contentType),
                "url": os.getenv("APIServer") + "/api/v1/youtube/download/" + info.type + "/" + downloadId + "." + info.type,
                "title": title
            }
            self.ReadOrWriteData({"id": downloadId, "title": title, "type": info.type})
            return response

        except Exception as ex:
            response: YoutubeResponseModel = {
                "status": False,
                "mideaType": info.type,
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
        
    def GetTotalYoutubeUsage(self):
        try:
            with open("./Data/downloadData.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        response: TotalDataResponse = {
            "totalUsage" : len(data),
            "totalMp3" : self.GetTotalData(data, "mp3"),
            "totalMp4" : self.GetTotalData(data, "mp4"),
        }

        return response
        
    def GetTotalData(data, type_) -> int:
        totalData = 0
        if len(data) != 0:
            for info in data:
                if info["type"] == type_:
                    totalData+=1
        return totalData

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

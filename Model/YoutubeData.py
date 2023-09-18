from pydantic import BaseModel, Field

class YoutubeRequestModel(BaseModel):
    url: str = Field(...)
    type: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "url": "https://yout.ube/xxxx?id=xxx",
                "type": "mp4"
            }
        }

class YoutubeResponseModel(BaseModel):
    status: bool = Field(...)
    message: str = Field(...)
    url: str = Field(...)
    title: str = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "status": True,
                "message": "Data fetch success",
                "url": "https://localhost/video.mp4",
                "title": "This is demo video"
            }
        }

class DownloadDataDB(BaseModel):
    id: str = Field(...)
    title:str = Field(...)
    type: str = Field(...)

class TotalDataResponse(BaseModel):
    totalUsage: int = Field(...)
    totalMp3: int = Field(...)
    totalMp4: int = Field(...)
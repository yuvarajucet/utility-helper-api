from pydantic import BaseModel, Field

class TruecallerResponseData(BaseModel):
    name: str = Field(default = "No info")
    phone: str = Field(default= "No info")
    provider: str = Field(default = "No info")
    country: str = Field(default = "No info")
    city: str = Field(default = "No info")
    image: str = Field(default = "No info")
    email: str = Field(default = "No info")
    userType: str = Field(default = "No info")
    bussinessImage: str = Field(default = "No info")

class TruecallerUsageResponse(BaseModel):
    total: int = Field(...)

class TruecallerLogin(BaseModel):
    number: str = Field(...)
    otp: str = Field(default= None)
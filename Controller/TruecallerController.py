from fastapi import APIRouter
from Helper.TruecallerHelper import TruecallerHelper
from Model.TruecallerData import TruecallerLogin

truecaller = APIRouter(
    prefix="/api/v1/truecaller",
    tags=["truecaller"],
    responses={404: {"message" : "Not found"}}
)

@truecaller.post("/config/{req_type}", tags=["truecaller"])
async def ConfigTrueCaller(req_type, data: TruecallerLogin):
    if req_type == "login":
        return TruecallerHelper.RegisterMobileNumber(TruecallerHelper, data.number)
    elif req_type == "validate":
        return TruecallerHelper.ValidateOTP(TruecallerHelper, data.number, data.otp)

@truecaller.get("/userinfo/{number}", tags=["truecaller"])
async def GetInfo(number: str):
    resp = TruecallerHelper.GetNumberInfo(TruecallerHelper, number)
    return resp

@truecaller.get("/get-data", tags=["truecaller"])
async def GetData():
    return TruecallerHelper.TrucallerUsageData(TruecallerHelper)
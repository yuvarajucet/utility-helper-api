from fastapi import APIRouter
from Helper.TruecallerHelper import TruecallerHelper

truecaller = APIRouter(
    prefix="/api/v1/truecaller",
    tags=["truecaller"],
    responses={404: {"message" : "Not found"}}
)

@truecaller.get("/config", tags=["truecaller"])
async def ConfigTrueCaller():
    return {"message": "Not implemented"}

@truecaller.get("/userinfo/{number}", tags=["truecaller"])
async def GetInfo(number: str):
    resp = await TruecallerHelper.GetNumberInfo(TruecallerHelper, number)
    return resp

@truecaller.get("/get-data", tags=["truecaller"])
async def GetData():
    return TruecallerHelper.TrucallerUsageData()
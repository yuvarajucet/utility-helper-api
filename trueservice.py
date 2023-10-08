import uvicorn
from fastapi import FastAPI

from Module.TruecallerModule import TruecallerModule

TruecallerLocal = FastAPI()

@TruecallerLocal.get("/api/v1/getfromlocaldata")
async def GetTruecallerInfo(phone, country_code, installation_id):
    return TruecallerModule.search_phonenumber(TruecallerModule, phone, country_code, installation_id)

if __name__ == "__main__":
    uvicorn.run(app=TruecallerLocal, port=5000)
import os
import json
from truecallerpy import search_phonenumber

from Model.TruecallerData import TruecallerResponseData, TruecallerUsageResponse

class TruecallerHelper:

    def __init__(self) -> None:
        pass

    async def GetNumberInfo(self, number):
        phone = number
        country_code = "IN"
        installation_id = os.getenv("InstallationID")

        response = None
        isExists = self.CheckNumberAlreadyExists(self, number)
        if isExists == None:
            data = await search_phonenumber(phone, country_code, installation_id)
            response = self.CreateUserData(self, data)
        else:
            response = isExists
        return response

    def CreateUserData(self, userInfo):
        userData: TruecallerResponseData = {
            "name" : self.FillUserInfo(self, userInfo, "name"),
            "phone" : self.FillUserInfo(self, userInfo, "phone"),
            "provider": self.FillUserInfo(self, userInfo, "provider"),
            "country": self.FillUserInfo(self, userInfo, "country"),
            "city": self.FillUserInfo(self, userInfo, "city"),
            "image": self.FillUserInfo(self, userInfo, "image"),
            "email": self.FillUserInfo(self, userInfo, "email"),
            "userType": self.FillUserInfo(self, userInfo, "usertype"),
            "bussinessImage": self.FillUserInfo(self, userInfo, "bussinessimage")
        }
        self.StoreLocalDB(self, userData)
        return userData

    def FillUserInfo(self, userInfo, requiredField):
        userData = userInfo["data"]["data"][0]
        if len(userData) > 0:
            if requiredField == "name":
                if userData.get("name") is not None:
                    return userData["name"]
            
            elif requiredField == "image":
                if userData.get("image") is not None:
                    return userData["image"]
                
            elif requiredField == "phone":
                if len(userData["phones"]) > 0:
                    if userData.get("phones") is not None:
                        return userData["phones"][0]["e164Format"] 

            elif requiredField == "provider":
                if len(userData["phones"]) > 0:
                    if userData.get("phones") is not None:
                        return userData["phones"][0]["carrier"]
            
            elif requiredField == "country":
                if len(userData["phones"]) > 0:
                    if userData.get("phones") is not None:
                        return userData["phones"][0]["countryCode"]
            
            elif requiredField == "city":
                if len(userData["addresses"]) > 0:
                    if userData.get("addresses") is not None:
                        return userData["addresses"][0]["city"]
                
            elif requiredField == "usertype":
                if len(userData["badges"]) > 0:
                    if userData.get("badges") is not None:
                        return userData["badges"][0]
            
            elif requiredField == "bussinessimage":
                if userData.get("businessProfile") is not None:
                    return userData["businessProfile"]["logoUrl"]
                
            elif requiredField == "email":
                if len(userData["internetAddresses"]) > 0:
                    if userData.get("internetAddresses") is not None:
                        return userData["internetAddresses"][0]["id"]

    def StoreLocalDB(self, data):
        try:
            with open("./Data/TruecallerData.json", 'r') as file:
                info = json.load(file)
        except FileNotFoundError:
            info = []
        
        isExists = self.CheckNumberAlreadyExists(self, data["phone"])
        if isExists == None:
            info.append(data)
            with open("./Data/TruecallerData.json", 'w') as file:
                json.dump(info, file, indent=4)

    def CheckNumberAlreadyExists(self, number):
        try:
            with open("./Data/TruecallerData.json", 'r') as file:
                info = json.load(file)
        except FileNotFoundError:
            info = []
        
        if len(info) > 0:
            for data in info:
                if data["phone"] == number:
                    return data
        return None
    
    def TrucallerUsageData():
        try:
            with open("./Data/TruecallerData.json", "r") as file:
                info = json.load(file)
        except FileNotFoundError:
            info = []

        response: TruecallerUsageResponse = {
            "total": len(info)
        }
        return response
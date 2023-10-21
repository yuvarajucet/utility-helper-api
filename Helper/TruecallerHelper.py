import os
import json
import random

from Module.TruecallerModule import TruecallerModule as TR
from Model.TruecallerData import TruecallerResponseData, TruecallerUsageResponse
from UserData.SaveData import SaveData
from Logger.ErrorLog import Logger

class TruecallerHelper:

    def __init__(self) -> None:
        pass

    def RegisterMobileNumber(self, phone):
        registerStatus = TR.SendOTPForLogin(TR, phone)
        return registerStatus

    def ValidateOTP(self, phone, otp):
        validateStatus = TR.ValidateOTP(TR, phone, otp)
        return validateStatus

    def GetNumberInfo(self, number):
        token_data = SaveData.GetUserTokenData(SaveData)
        if len(token_data) > 1:
            randomToken = token_data[random.randint(0, len(token_data) - 1)]
        else:
            if len(token_data):
                randomToken = token_data[0]
            else:
                return {
                    "status": False,
                    "message": "There is no access token to get user info. Please login!"
                }

        phone = number
        country_code = "IN"
        installation_id = randomToken["access_token"]

        response = None
        isExists = self.CheckNumberAlreadyExists(self, number)
        if isExists == None:
            data = TR.search_phonenumber(TR, number, country_code, installation_id)
            if data["status"]:
                response = self.CreateUserData(self, data["data"])
            else:
                return {
                    "status": False,
                    "message": data["message"]
                }
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
        try:
            userData = userInfo["data"][0]
            if len(userData) > 0:
                if requiredField == "name":
                    if userData.get("name") is not None:
                        return userData["name"]
                
                elif requiredField == "image":
                    if userData.get("image") is not None:
                        return userData["image"]
                    
                elif requiredField == "phone":
                    if len(userData["phones"]) > 0:
                        if userData.get("phones") is not None and userData["phones"][0].get("e164Format") is not None:
                            return userData["phones"][0]["e164Format"] 

                elif requiredField == "provider":
                    if len(userData["phones"]) > 0:
                        if userData.get("phones") is not None and userData["phones"][0].get("carrier") is not None:
                            return userData["phones"][0]["carrier"]
                
                elif requiredField == "country":
                    if len(userData["phones"]) > 0:
                        if userData.get("phones") is not None and userData["phones"][0].get("countryCode") is not None:
                            return userData["phones"][0]["countryCode"]
                
                elif requiredField == "city":
                    if len(userData["addresses"]) > 0:
                        if userData.get("addresses") is not None and userData["addresses"][0].get("city") is not None:
                            return userData["addresses"][0]["city"]
                    
                elif requiredField == "usertype":
                    if len(userData["badges"]) > 0:
                        if userData.get("badges") is not None and userData.get("badges") is not None:
                            return userData["badges"][0]
                
                elif requiredField == "bussinessimage":
                    if userData.get("businessProfile") is not None and userData.get("logoUrl") is not None:
                        return userData["businessProfile"]["logoUrl"]
                    
                elif requiredField == "email":
                    if len(userData["internetAddresses"]) > 0:
                        if userData.get("internetAddresses") is not None and userData.get("id") is not None:
                            return userData["internetAddresses"][0]["id"]
                        
        except Exception as ex:
            Logger.Log(Logger, self.FillUserInfo.__name__, str(ex))

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
    
    def TrucallerUsageData(self):
        try:
            with open("./Data/TruecallerData.json", "r") as file:
                info = json.load(file)
        except FileNotFoundError:
            info = []

        response: TruecallerUsageResponse = {
            "total": len(info)
        }
        return response

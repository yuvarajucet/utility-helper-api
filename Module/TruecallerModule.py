import requests
import json
import random
import os

from UserData.SaveData import SaveData
from Logger.ErrorLog import Logger

class TruecallerModule:
    
    def __init__(self) -> None:
        pass

    def SendOTPForLogin(self, phone):
        NUMS = '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
        LETTS = 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        json = {'countryCode':'','dialingCode':None,'installationDetails':{'app':{'buildVersion':5,'majorVersion':11,'minorVersion':75, 'store':'GOOGLE_PLAY'},'device':{'deviceId':''.join(random.choices(NUMS+LETTS, k=16)),'language':'en','manufacturer':'Xiaomi','mobileServices':['GMS'],'model':'M2010J19SG','osName':'Android','osVersion':'10','simSerials':[''.join(random.choices(NUMS, k=19)), ''.join(random.choices(NUMS, k=20))]},'language':'en','sims':[{'imsi':''.join(random.choices(NUMS, k=15)),'mcc':'413','mnc':'2','operator':None}]},'phoneNumber':phone,'region':'region-2','sequenceNo':2}
        headers = {'content-type':'application/json; charset=UTF-8','accept-encoding':'gzip','user-agent':'Truecaller/11.75.5 (Android;10)','clientsecret':'lvc22mp3l1sfv6ujg83rd17btt'}

        try:
            response = requests.post('https://account-asia-south1.truecaller.com/v2/sendOnboardingOtp', headers=headers, json=json)
            if response.json()['status'] == 1 or response.json()['status'] == 9:
                os.environ["requestId"] = response.json()['requestId']
                return {
                    "status": True,
                    "message": f"Sent an OTP for {phone}"
                }
            else:
                os.environ["requestId"] = "0"
                return {
                    "status": False,
                    "message": response.json()['message']
                } 
        except Exception as ex:
            Logger.Log(Logger, self.SendOTPForLogin.__name__, str(ex))
            return {
                "status": False,
                "message": "Failed to send OTP!"
            }

    def ValidateOTP(self, phone, otp):
        json = {
            'countryCode':'',
            'dialingCode':None,
            'phoneNumber':phone,
            'requestId':os.getenv("requestId"),
            'token':otp
        }

        headers = {
            'content-type':'application/json; charset=UTF-8',
            'accept-encoding':'gzip',
            'user-agent':'Truecaller/11.75.5 (Android;10)',
            'clientsecret':'lvc22mp3l1sfv6ujg83rd17btt'
        }

        try:
            response = requests.post('https://account-asia-south1.truecaller.com/v1/verifyOnboardingOtp', headers=headers, json=json)

            if response.json()['status'] == 11:
                return {
                    "status": False,
                    "message": "OTP code is Invalid"
                }
            
            elif response.json()['status'] == 2 and response.json()['suspended']:
                token = {
                    "phone": phone,
                    "access_token": response.json()["installationId"]
                }

                SaveData.SetData(SaveData, token)
                return {
                    "status": False,
                    "message": "Opps!... Your account got suspended. Try another number :("
                }
            else:
                token = {
                    "phone": phone,
                    "access_token": response.json()["installationId"]
                }

                SaveData.SetData(SaveData, token)
                return {
                    "status": True,
                    "message": "Validation success!"
                }
            
        except Exception as ex:
            Logger.Log(Logger, self.ValidateOTP.__name__, str(ex))
            return {
                "status": False,
                "message": "Failed to validate OTP!"
            }

    def search_phonenumber(self, phone, countryCode, authToken):
        params = {
            'q':phone,
            'countryCode':countryCode,
            'type':'4',
            'locAddr':'',
            'placement':'SEARCHRESULTS,HISTORY,DETAILS',
            'encoding':'json'
        }

        headers = {
            'content-type':'application/json; charset=UTF-8',
            'accept-encoding':'gzip',
            'user-agent':'Truecaller/11.75.5 (Android;10)',
            'clientsecret':'lvc22mp3l1sfv6ujg83rd17btt',
            'authorization':'Bearer ' + authToken
        }

        try:
            Logger.Log(Logger, self.search_phonenumber.__name__, self.GetPhoneNumberUsingAuthToken(authToken), True)
            Logger.Log(Logger, "Test", str(phone))
            response = requests.get("https://search5-noneu.truecaller.com/v2/search", headers=headers, params=params)
            Logger.Log(Logger, "res==> ", str(response))
            Logger.Log(Logger, "this ==> ", str(response.content))
            Logger.Log(Logger, "status ==> ", str(response.json().get('status')))
            if response.json().get('status'):
                Logger.Log(Logger, self.search_phonenumber.__name__, str(response.json()))
                return {
                    "status": False,
                    "message": "Failed to get user info"
                }
            else:
                Logger.Log(Logger, "Suc==> ", str(response.content))
                return {
                    "status": True,
                    "message": "User details found",
                    "data": json.loads(response.content)
                }

        except Exception as ex:
            Logger.Log(Logger, self.search_phonenumber.__name__, str(ex))
            return {
                "status": False,
                "message": "Failed to get user details"
            }
        
    def GetPhoneNumberUsingAuthToken(token: str):
        try:
            with open("./UserData/SavedData.json","r") as file:
                info = json.load(file)
        except FileNotFoundError:
            info = []
        
        for data in info:
            if data["access_token"] == token:
                return data["phone"]

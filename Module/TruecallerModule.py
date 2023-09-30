import requests
import json
import random
import os

class TruecallerModule:
    
    def __init__(self) -> None:
        pass

    def SendOTPForLogin(self, phone):
        NUMS = '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
        LETTS = 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        json = {'countryCode':'','dialingCode':None,'installationDetails':{'app':{'buildVersion':5,'majorVersion':11,'minorVersion':75, 'store':'GOOGLE_PLAY'},'device':{'deviceId':''.join(random.choices(NUMS+LETTS, k=16)),'language':'en','manufacturer':'Xiaomi','mobileServices':['GMS'],'model':'M2010J19SG','osName':'Android','osVersion':'10','simSerials':[''.join(random.choices(NUMS, k=19)), ''.join(random.choices(NUMS, k=20))]},'language':'en','sims':[{'imsi':''.join(random.choices(NUMS, k=15)),'mcc':'413','mnc':'2','operator':None}]},'phoneNumber':phone,'region':'region-2','sequenceNo':2}
        headers = {'content-type':'application/json; charset=UTF-8','accept-encoding':'gzip','user-agent':'Truecaller/11.75.5 (Android;10)','clientsecret':'lvc22mp3l1sfv6ujg83rd17btt'}

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

        response = requests.post('https://account-asia-south1.truecaller.com/v1/verifyOnboardingOtp', headers=headers, json=json)

        if response.json()['status'] == 11:
            return {
                "status": False,
                "message": "OTP code is Invalid"
            }
        elif response.json()['status'] == 2 and response.json()['suspended']:
            return {
                "status": False,
                "message": "Opps!... Your account got suspended. Try another number :("
            }
        else:
            os.environ["InstallationID"] = response.json()['installationId']
            return {
                "status": True,
                "message": "Validation success!"
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

        response = requests.get("https://search5-noneu.truecaller.com/v2/search", headers=headers, params=params)
        if response.json().get('status'):
            return None
        else:
            return json.loads(response.content)
        
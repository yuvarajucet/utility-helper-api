import json

from Logger.ErrorLog import Logger

class SaveData:

    def __init__(self) -> None:
        pass

    def SetData(self, tokenObject):
        try:
            existingData = self.GetData(self)
            existingData.append(tokenObject)
            with open("./UserData/SavedData.json","w") as file:
                json.dump(existingData, file, indent=4)

        except Exception as ex:
            Logger.Log(Logger, self.SetData.__name__, str(ex))

    def GetData(self):
        try:
            with open("./UserData/SavedData.json", "r") as file:
                data = json.load(file)
                return data

        except Exception as ex:
            Logger.Log(Logger, self.GetData.__name__, str(ex))
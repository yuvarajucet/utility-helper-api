from datetime import datetime

class Logger:

    def __init__(self) -> None:
        pass

    def Log(self, method, data, isTokenUsage = False):
        try:
            with open("./Logger/log.txt", "a+") as file:
                currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                if not isTokenUsage:
                    file.write(currentTime + " ==> " + method + " ==> " + data + "\n")
                else:
                    file.write(currentTime + " ==> " + method + " ==> CurrentToken ==> " + data + "\n")

        except Exception as ex:
            with open("./Logger/log.txt", "a+") as file:
                currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                file.write(currentTime + " ==> " + method + " ==> " + str(ex) + "\n")
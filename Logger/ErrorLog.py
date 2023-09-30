from datetime import datetime

class Logger:

    def __init__(self) -> None:
        pass

    def Log(self, method, exception):
        try:
            with open("./Logger/log.txt", "w") as file:
                currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                file.write(currentTime + "==>" + method + "==>" + exception + "\n")

        except Exception as ex:
            with open("./Logger/log.txt", "w") as file:
                currentTime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                file.write(currentTime + "==>" + method + "==>" + str(ex) + "\n")
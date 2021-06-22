from time import gmtime, strftime

def createlog(data, message):
        f = open("logfile.log", "a")
        f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " :: " + data + " :: " + message + "\n")
        f.close()
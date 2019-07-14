class Info:
    def __init__(self, infostatus, infomsg="", infodata={}):
        self.infostatus = infostatus
        self.infomsg = infomsg
        self.infodata = infodata

    def todict(self):
        return {"infostatus": self.infostatus, 
                "infomsg": self.infomsg, 
                "infodata": self.infodata}
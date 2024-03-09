class Usuario:
    
    def __init__(self, email):
        self.email = email
        self.pwd = []

    def getListaNotas(self):
        return self.pwd;

    def to_dict (self):
        return {"email" : self.email, "pwd" : self.pwd } 
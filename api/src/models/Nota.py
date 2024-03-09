import datetime
import uuid

class Nota:

    def __init__(self,titulo, texto, isTerminado : bool, isImportante : bool):
        self.id = uuid.uuid4()
        self.titulo = titulo
        self.texto = texto
        self.fechaCreacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.fechaUltimaModifcacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.isTerminado = isTerminado
        self.isImportante = isImportante

    def to_dict(self):
        return {
            "id": str(self.id),
            "titulo": self.titulo,
            "texto": self.texto,
            "fechaCreacion": self.fechaCreacion,
            "fechaUltimaModificacion": self.fechaUltimaModificacion,
            "isTerminado": self.isTerminado,
            "isImportante": self.isImportante
        }
    
    def updateFecha (self):
        self.fechaUltimaModifcacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    

from typing import Iterable, Optional
from models.Nota import Nota

import mariadb
from datetime import datetime

class NotasRepositoryMaria():
    def __init__(self,table,db_user,db_password):
        self.table = table
        print("Connecting...")
        try:
            self.conn = mariadb.connect(
                host="mariadb",
                port=3306,
                user=db_user,
                password=db_password,
                database="testdb"
            )
            self.cursor = self.conn.cursor()
            print("Connected")
            self.create_tables()
        except mariadb.Error as e:
            print(f"Error {e}")  

    def create_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS users (user_id VARCHAR(100) PRIMARY KEY)")
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS notas (id VARCHAR(100) PRIMARY KEY, titulo VARCHAR(100), contenido VARCHAR(100), fecha_creacion VARCHAR(100),fecha_modificacion VARCHAR(100), cheked BOOLEAN,important BOOLEAN,FOREIGN KEY (user_id) REFERENCES users(user_id))")
        self.conn.commit()

    def find_all(self, user_id):
        self.cursor.execute(f"SELECT * FROM notas WHERE user_id = '{user_id}'")
        notas = [nota(titulo=nota[1], contenido=nota[2], fecha_creacion=nota[3], fecha_modificacion=nota[4], cheked=bool(nota[5]), important=bool(nota[6]), create_date=nota[7]) for nota in self.cursor]
        return notas
    
       

    def find_byid(self, user_id, id):
        self.cursor.execute(f"SELECT * FROM notas WHERE user_id = '{user_id}' AND id = '{id}'")
        task = self.cursor.fetchone()
        if task is not None:
            return nota(titulo=Nota[1], contenido=nota[2], fecha_creacion=nota[3], fecha_modificacion=nota[4], cheked=bool(nota[5]), important=bool(nota[6]), create_date=nota[7]) 
        else:
            return None

    def save(self, nota,user_id):
        #modificamos la fecha de modificacion de la nota
        nota.mod_fecha()
        #buscamos la nota en la db
        find = self.find_byid(nota.id, user_id)
        #si existe modificamos valores 
        if find != None:       
            updata = (nota.titulo, nota.contenido, nota.fecha_modificacion, nota.cheked,nota.important)
            self.cursor.execute(f"UPDATE notas SET titulo = ?, contenido = ?, fecha_modificacion = ?, cheked = ?, important = ? WHERE user_id = {user_id} AND id = {nota.id}", updata)
            self.conn.commit()
            if self.cursor.rowcount > 0:
                return nota
        else:
           #si no existe se crea la nueva nota  
            fecha_creacion  = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            data = (nota.id,nota.titulo,nota.contenido,fecha_creacion,nota.cheked,nota.important,fecha_creacion,user_id)
            self.cursor.execute(f"INSERT INTO notas (id,titulo,contenido,fecha_creacion,cheked,important,fecha_modificacion,user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
            self.conn.commit()
            if self.cursor.rowcount > 0:
                return nota

    def delete_byid(self, id):
        self.cursor.execute(f"DELETE FROM notas WHERE id ='{id}'")
        self.conn.commit()

    def delete(self,nota):
        self.delete_byid(nota.id)

    def delete_all(self, user_id):
        self.cursor.execute(f"DELETE FROM notas WHERE user_id = '{user_id}'")
        self.conn.commit()
        
    def count(self, user_id):
        self.cursor.execute(f"SELECT COUNT(*) FROM notas WHERE user_id = '{user_id}'")
        return self.cursor.fetchone()[0]

    def close(self):
        self.cursor.close()
        self.conn.close()
from tkinter.constants import FALSE
import pymysql 

class db():

    def __init__(self):
        self.conexion = pymysql.connect(user="root", password="root", host="localhost",db="pibd")

    def conectardb(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print ("Database version : {0}".format(data))

    def escribirdb_archivos(self, nom, llave64, user):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO archivos(id, nombre_archivo, llave64en, usuario, shared) \
                VALUES (NULL,%s,%s,%s,'-1')"
            #"INSERT INTO prueba(id, nombre_archivo, key64) \
            #VALUES (NULL,'"+nom+"','"+k64+"')"
            #VALUES (NULL,'a','c')"
            
        try:
            cursor.execute(sql,(nom, llave64, user))

            self.conexion.commit()
        except:
            self.conexion.rollback()
    
    def escribirdb_compartidos(self, nom, llave64, user, shared):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO archivos(id, nombre_archivo, llave64en, usuario, shared) \
                VALUES (NULL,%s,%s,%s,%s)"
            #"INSERT INTO prueba(id, nombre_archivo, key64) \
            #VALUES (NULL,'"+nom+"','"+k64+"')"
            #VALUES (NULL,'a','c')"
            
        try:
            cursor.execute(sql,(nom, llave64, user, shared))

            self.conexion.commit()
        except:
            self.conexion.rollback()
    
    def getArchivo(self, id):
        cursor = self.conexion.cursor()
        sql = "SELECT nombre_archivo FROM archivos WHERE id = %s"
        global bool_db
        try:
            cursor.execute(sql,(id))

            if cursor.rowcount == 0:
                print("El archivo no está en la base de datos")
                bool_db= False
                return bool_db
            else:
                bool_db = True
                auxId=cursor.fetchone()[0]
                return auxId
            
        except:
            self.conexion.rollback()
    

    def getAdmin(self):
        cursor = self.conexion.cursor()
        sql = "SELECT id FROM usuarios WHERE usuario = 'admin'"
        global boolAdmin
        try:
            cursor.execute(sql)

            if cursor.rowcount == 0:
                print("El usuario no existe")
                boolAdmin = False
                return boolAdmin
            else:
                aux_key_db =  cursor.fetchone()[0]
                return aux_key_db
                
        except:
            self.conexion.rollback()
    
    
    def getUser(self, nom):
        cursor = self.conexion.cursor()
        sql = "SELECT id FROM usuarios WHERE usuario = %s"
        try:
            cursor.execute(sql,(nom))
            if cursor.rowcount == 0:
                return False
            else:
                aux_id =  cursor.fetchone()[0]
                return aux_id

        except:
            self.conexion.rollback()

    def getUserShared(self, nom):
        cursor = self.conexion.cursor()
        sql = "SELECT shared FROM archivos WHERE id = %s"
        try:
            cursor.execute(sql,(nom))
            if cursor.rowcount == 0:
                return False
            else:
                aux_id =  cursor.fetchone()[0]
                return aux_id

        except:
            self.conexion.rollback()


    def getIdUser(self, nom):
        cursor = self.conexion.cursor()
        sql = "SELECT id FROM usuarios WHERE usuario = %s"
        try:
            cursor.execute(sql,(nom))
            if cursor.rowcount == 0:
                return False
            else:
                aux_id =  cursor.fetchone()[0]
                return aux_id

        except:
            self.conexion.rollback()

    def getNomUser(self, nom):
        cursor = self.conexion.cursor()
        sql = "SELECT usuario FROM usuarios WHERE id = %s"
        try:
            cursor.execute(sql,(nom))
            if cursor.rowcount == 0:
                return False
            else:
                aux_id =  cursor.fetchone()[0]
                print(aux_id)
                return aux_id

        except:
            self.conexion.rollback()


    def setAdmin(self, nom, hash, clavePub, clavePriv):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO usuarios(id, usuario, password, clavePublica, clavePrivada) \
                VALUES (NULL,%s,%s,%s,%s)"
            #"INSERT INTO prueba(id, nombre_archivo, key64) \
            #VALUES (NULL,'"+nom+"','"+k64+"')"
            #VALUES (NULL,'a','c')"
            
        try:
            cursor.execute(sql,(nom, hash, clavePub, clavePriv))

            self.conexion.commit()
        except:
            self.conexion.rollback()
        
    def setUser(self, nom, hash, clavePub, clavePriv):
        cursor = self.conexion.cursor()
        sql = "INSERT INTO usuarios(id, usuario, password, clavePublica, clavePrivada) \
                VALUES (NULL,%s,%s,%s,%s)"
            #"INSERT INTO prueba(id, nombre_archivo, key64) \
            #VALUES (NULL,'"+nom+"','"+k64+"')"
            #VALUES (NULL,'a','c')"
            
        try:
            cursor.execute(sql,(nom, hash, clavePub, clavePriv))

            self.conexion.commit()
        except:
            self.conexion.rollback()
    

    
    def getPass(self, aux_user):
        cursor = self.conexion.cursor()
        sql = "SELECT password FROM usuarios WHERE id = %s"
        global boolAdmin
        try:
            cursor.execute(sql,(aux_user))

            if cursor.rowcount == 0:
                print("La contraseña no existe")
                boolAdmin = False
                return boolAdmin
            else:
                aux_key_db =  cursor.fetchone()[0]
                return aux_key_db
                
        except:
            self.conexion.rollback()

    
    def getPublica(self, idUser):
        cursor = self.conexion.cursor()
        sql = "SELECT clavePublica FROM usuarios WHERE id = %s"
        try:
            cursor.execute(sql,(idUser))

            if cursor.rowcount == 0:
                print("El usuario no existe")
                return False
            else:
                aux_key_db =  cursor.fetchone()[0]
                return aux_key_db
                
        except:
            self.conexion.rollback()

    def getPrivada(self, idUser):
        cursor = self.conexion.cursor()
        sql = "SELECT clavePrivada FROM usuarios WHERE id = %s"
        try:
            cursor.execute(sql,(idUser))

            if cursor.rowcount == 0:
                print("clave privada no existe")
                return False
            else:
                aux_key_db =  cursor.fetchone()[0]
                return aux_key_db
                
        except:
            self.conexion.rollback()

    
    def get64En(self, idArch):
        cursor = self.conexion.cursor()
        sql = "SELECT llave64En FROM archivos WHERE id = %s"
        global bool_db
        try:
            cursor.execute(sql,(idArch))

            if cursor.rowcount == 0:
                print("El archivo no está en la base de datos")
                bool_db= False
                return bool_db
            else:
                aux_key_db =  cursor.fetchone()[0]
                return aux_key_db
            
        except:
            self.conexion.rollback()


    def leerNombre(self, nom):
        cursor = self.conexion.cursor()
        sql = "SELECT nombre_archivo FROM archivos WHERE nombre_archivo = %s"
        global bool_db
        try:
            cursor.execute(sql,(nom))

            if cursor.rowcount == 0:
                print("El archivo no está en la base de datos")
                bool_db= False
                return bool_db
            else:
                bool_db = True
                return bool_db
            
        except:
            self.conexion.rollback()


    def getArchivosPropios(self, idUser):
        cursor = self.conexion.cursor()
        sql = "SELECT id, nombre_archivo FROM archivos WHERE usuario = %s AND shared = '-1'"
        global bool_db
        try:
            cursor.execute(sql,(idUser))
            id = cursor.fetchall()
            return id
            
        except:
            self.conexion.rollback() 

    
    def getCompartidos(self, idUser):
        cursor = self.conexion.cursor()
        sql = "SELECT id, nombre_archivo FROM archivos WHERE shared = %s"
        global bool_db
        try:
            cursor.execute(sql,(idUser))
            id = cursor.fetchall()
            return id
            
        except:
            self.conexion.rollback() 


    def guardarPrivada(self, cPriv, pswd):
        cursor = self.conexion.cursor()
        sql = "UPDATE usuarios SET claveHash= %s WHERE password = %s"
        try:
            cursor.execute(sql,(cPriv, pswd))
            self.conexion.commit()
            
        except:
            self.conexion.rollback()         
    

    # def borrarRegistro(self, nom):
    #     cursor = self.conexion.cursor()
    #     auxvar = self.leerId(nom)
    #     sql = "DELETE FROM archivos WHERE archivos.id = %s"
    #     try:
    #         cursor.execute(sql,(auxvar))
    #         self.conexion.commit()
    #     except:
    #         self.conexion.rollback()
    
    def borrarRegistroId(self, id):
        cursor = self.conexion.cursor()
        sql = "DELETE FROM archivos WHERE archivos.id = %s"
        try:
            cursor.execute(sql,(id))
            self.conexion.commit()
        except:
            self.conexion.rollback()

    def cerrardb(self):
        self.conexion.close()
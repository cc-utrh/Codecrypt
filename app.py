import base64
from ctypes import sizeof
import eel
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP 
from Crypto.Util.Padding import pad, unpad
import Crypto.Random
import binascii
from base64 import b64encode, b64decode #convertir llave a base 64
from db import db
import hashlib
import os
from pathlib import Path, PureWindowsPath

########################################################### 

KEYSIZE = 16

def getKey(keysize):#genera llave aleatoria
    key=os.urandom(keysize)        
    return key

def key64(key0):#pasa la llave a base 64
    key64 = base64.b64encode(key0)
    return key64 

def dKey64(key64):
    dKey0 = base64.b64decode(key64)
    return dKey0

def generateKeyRSA():
    global keyPair
    keyPair = RSA.generate(1024)
    setearKeys(keyPair)
    
def setearKeys(keyPair):
    global pubKey
    pubKey = keyPair.publickey()
    global pubKeyPEM
    pubKeyPEM = pubKey.exportKey().decode()
    global privKeyPEM
    privKeyPEM = keyPair.exportKey().decode()
    global privadoLlave
    privadoLlave = keyPair.exportKey()

    #######FUNCIONES RSA#########

def encrypt_rsa(nombA, g_k64, clavePub, aux_user):
    print(clavePub)
    clavePubB = RSA.import_key(clavePub)
    encryptor = PKCS1_OAEP.new(clavePubB)
    encrypted = encryptor.encrypt(g_k64)
    llave64en = base64.b64encode(encrypted)
    conexion.escribirdb_archivos(nombA, llave64en, aux_user)

def decrypt_rsa(pk, k64en):
    print(k64en)
    k64full = base64.b64decode(k64en)
    
    print(k64full)
    print("estoy en el decrypt rsa")
    print(pk)
    llavePrivDes = RSA.import_key(pk)
    decryptor = PKCS1_OAEP.new(llavePrivDes)
    decrypted = decryptor.decrypt(k64full) #cambiar encrypted por el archivo añadir a ambos el método de leer
    return decrypted


    #######HASH########

def hashPass(password):
    hashed = str.encode(password)
    hashed = hashlib.sha256(hashed).hexdigest()
    return hashed


    ########COMPROBAR PASSWORD########

def comprobarPass(passH, passDb):
    if passH == passDb:
        return True
    else:
        return False



########ENCRIPTACION DE LA CLAVE PRIVADA EN AES###########

def encrypt_privada(clavePriv, password):
    passBytes = str.encode(password)
    pass0 = base64.b64decode(passBytes)
    sizeSalt = 16 - len(pass0)
    salt = bytes(sizeSalt)
    bA = bytearray(pass0)
    bA.extend(salt)
    password_full = bytes(bA)
    cipher = AES.new(password_full, AES.MODE_ECB)
    clavePrivEn = cipher.encrypt(pad(clavePriv, 16))
    print(clavePriv)
    print(clavePrivEn)
    claveGuardar = base64.b64encode(clavePrivEn)
    return claveGuardar






###########ENCRIPTACION##############
@eel.expose
def preEncrypt(user, pswd):
    aux_user = conexion.getIdUser(user)
    if aux_user == False:
        pass
        # user = "admin"
        # password = "password"
        # generateKeyRSA()
        # ph = hashPass(password)
        # privkeydb = encrypt_privada(privadoLlave, password)
        # conexion.setAdmin(user, ph, pubKeyPEM, privkeydb) #¿como pasar las claves?
        # preEncrypt(pswd)
    else:
        passdb = conexion.getPass(aux_user)
        ph = hashPass(pswd)
        aux_p = comprobarPass(ph, passdb)
        if aux_p == False:
            print("Las contraseñas no coinciden")
        else :
            clavePub = conexion.getPublica(aux_user)
            global g_k0
            g_k0 = getKey(KEYSIZE)
            global g_k64 
            g_k64 = key64(g_k0)
            encrypt(g_k0, g_k64, clavePub, aux_user)
    



def encrypt(g_k0, g_k64, clavePub, aux_user):
    encrypted_filename=nombreArchivo
    nomUsu = conexion.getNomUser(aux_user)
    if(os.path.exists(os.getcwd() +"\encrypted_files\\"+nomUsu)):
        pass
    else:
        os.mkdir(os.getcwd() +"\encrypted_files\\"+nomUsu)
    with open(rutaArchivo+"/"+nombreArchivo, "rb") as file1:
        data=file1.read()
        cipher=AES.new(g_k0, AES.MODE_ECB)
        ciphertext=cipher.encrypt(pad(data, 16))
        with open(os.getcwd() +"\encrypted_files\\"+nomUsu+"\\"+nombreArchivo, "wb") as file2:
            file2.write(ciphertext)
        encrypt_rsa(nombreArchivo, g_k64, clavePub, aux_user)

        return encrypted_filename






##########DESENCRIPTACION DE LA CLAVE PRIVADA AES############

def decrypt_privada(clavePriv, password):
    passBytes = str.encode(password)
    pass0 = base64.b64decode(passBytes)
    sizeSalt = 16 - len(pass0)
    salt = bytes(sizeSalt)
    bA = bytearray(pass0)
    bA.extend(salt)
    password_full = bytes(bA)
    cipher2 = AES.new(password_full, AES.MODE_ECB)
    claveDecoded = base64.b64decode(clavePriv)
    claveDecBy = bytes(bytearray(claveDecoded))
    clavePrivDe = unpad(cipher2.decrypt(claveDecoded), 16)
    claveDevolver = clavePrivDe.decode()
    return claveDevolver


########DESENCRIPTACION#######
@eel.expose
def preDecrypt(downloadId, nomUser, pswd):
    aux_db = conexion.getArchivo(downloadId)
    if aux_db!=False:
        # user = "admin"
        # password = "password"
        aux_user = conexion.getUser(nomUser)
        passdb = conexion.getPass(aux_user)
        ph = hashPass(pswd)
        aux_p = comprobarPass(ph, passdb)
        if aux_p == False:
            print("la contraseña es incorrecta")
        else:
            clavePrivadaEn = conexion.getPrivada(aux_user)
            clavePrivadaDe = decrypt_privada(clavePrivadaEn, pswd)
            llave64En = conexion.get64En(downloadId)
            nombreArchivoDe = conexion.getArchivo(downloadId)
            key64De = decrypt_rsa(clavePrivadaDe, llave64En)
            k0De = dKey64(key64De)
            decrypt(k0De, nombreArchivoDe, aux_user)
            

def decrypt(k0, nombreDe, aux_user):
    decrypted_filename=nombreDe
    nomUsu = conexion.getNomUser(aux_user)
    if(os.path.exists(os.getcwd() +"\decrypted_files\\"+nomUsu)):
        pass
    else:
        os.mkdir(os.getcwd() +"\decrypted_files\\"+nomUsu)
    rutaEn = os.getcwd()+"\encrypted_files\\"+nomUsu+"\\"+nombreDe
    #pathE = rutaEn.replace(os.sep, '/')
    #print(pathE)
    rutaDe = os.getcwd()+"\decrypted_files\\"+nomUsu+"\\"+nombreDe
    pathDe = Path(rutaDe)
    
    with open(rutaEn, "rb") as file1:
        data=file1.read()
        cipher2=AES.new(k0, AES.MODE_ECB)

        decrypted_data=unpad(cipher2.decrypt(data), 16)
        with open(pathDe, "wb") as file2:
           file2.write(decrypted_data)
        
        return decrypted_filename



###############MÉTODOS DE COMPARTIR ARCHIVOS############

def encrypt_rsa_shared(nombA, g_k64, clavePub, aux_user, aux_share):
    clavePubB = RSA.import_key(clavePub)
    encryptor = PKCS1_OAEP.new(clavePubB)
    encrypted = encryptor.encrypt(g_k64)
    llave64en = base64.b64encode(encrypted)
    conexion.escribirdb_compartidos(nombA, llave64en, aux_user, aux_share)
    

def encryptShared(g_k0, g_k64, clavePub, aux_user, aux_shared, nomArchivo, archivo):
    
    nomUsu = conexion.getNomUser(aux_user)
    nomShared = conexion.getNomUser(aux_shared)
    encrypted_filename= nomUsu+"_"+nomArchivo
    print(encrypted_filename)
    if(os.path.exists(os.getcwd() +"\encrypted_files\\"+nomShared)):
        print("existo fuera")
        if(os.path.exists(os.getcwd() +"\encrypted_files\\"+nomShared+"\Shared")):
            print("existo dentro")
        else:
            os.mkdir(os.getcwd() +"\encrypted_files\\"+nomShared+"\Shared")
            print("creo dentro")
    else:
        os.mkdir(os.getcwd() +"\encrypted_files\\"+nomShared)
        os.mkdir(os.getcwd() +"\encrypted_files\\"+nomShared+"\Shared")
    data=archivo
    print("llego a data")
    cipher=AES.new(g_k0, AES.MODE_ECB)
    ciphertext=cipher.encrypt(pad(data, 16))
    with open(os.getcwd() +"\encrypted_files\\"+nomShared+"\Shared\\"+encrypted_filename, "wb") as file2:
        file2.write(ciphertext)
    print(encrypted_filename)
    encrypt_rsa_shared(encrypted_filename, g_k64, clavePub, aux_user, aux_shared)

    return encrypted_filename

@eel.expose
def Share(shareId, nomUser, nomShared, pswd):
    aux_db = conexion.getArchivo(shareId)
    if aux_db!=False:
        aux_user = conexion.getUser(nomUser)
        aux_shared = conexion.getUser(nomShared)
        passdb = conexion.getPass(aux_user)
        ph = hashPass(pswd)
        aux_p = comprobarPass(ph, passdb)
        if aux_p == False:
            print("la contraseña es incorrecta")
        else:
            clavePrivadaEn = conexion.getPrivada(aux_user)
            clavePrivadaDe = decrypt_privada(clavePrivadaEn, pswd)
            llave64En = conexion.get64En(shareId) #devuelve none
            nombreArchivoDe = conexion.getArchivo(shareId)
            key64De = decrypt_rsa(clavePrivadaDe, llave64En)
            k0De = dKey64(key64De)
            data = decryptShared(k0De, nombreArchivoDe, aux_user)
            clavePubShared = conexion.getPublica(aux_shared)
            encryptShared(k0De, key64De, clavePubShared, aux_user, aux_shared, nombreArchivoDe, data)

@eel.expose
def preDecryptShared(downloadId, nomUser, pswd):
    aux_db = conexion.getArchivo(downloadId)
    if aux_db!=False:
        # user = "admin"
        # password = "password"
        aux_user = conexion.getUserShared(downloadId)
        print(aux_user)
        print(downloadId)
        passdb = conexion.getPass(aux_user)
        ph = hashPass(pswd)
        aux_p = comprobarPass(ph, passdb)
        if aux_p == False:
            print("la contraseña es incorrecta")
        else:
            clavePrivadaEn = conexion.getPrivada(aux_user)
            clavePrivadaDe = decrypt_privada(clavePrivadaEn, pswd)
            llave64En = conexion.get64En(downloadId)
            nombreArchivoDe = conexion.getArchivo(downloadId)
            key64De = decrypt_rsa(clavePrivadaDe, llave64En)
            k0De = dKey64(key64De)
            decryptShared2(k0De, nombreArchivoDe, aux_user)


def decryptShared(k0, nombreDe, aux_user):
    nomUsu = conexion.getNomUser(aux_user)
    if(os.path.exists(os.getcwd() +"\decrypted_files\\"+nomUsu)):
        pass
    else:
        os.mkdir(os.getcwd() +"\decrypted_files\\"+nomUsu)
    rutaEn = os.getcwd()+"\encrypted_files\\"+nomUsu+"\\"+nombreDe
    #pathE = rutaEn.replace(os.sep, '/')
    #print(pathE)
    rutaDe = os.getcwd()+"\decrypted_files\\"+nomUsu+"\\"+nombreDe
    
    
    with open(rutaEn, "rb") as file1:
        data=file1.read()
        cipher2=AES.new(k0, AES.MODE_ECB)

        decrypted_data=unpad(cipher2.decrypt(data), 16)
        # with open(pathDe, "wb") as file2:
        #    file2.write(decrypted_data)
        
        return decrypted_data


def decryptShared2(k0, nombreDe, aux_user):
    decrypted_filename=nombreDe
    nomUsu = conexion.getNomUser(aux_user)
    if(os.path.exists(os.getcwd() +"\decrypted_files\\"+nomUsu)):
        print("existo fuera")
        if(os.path.exists(os.getcwd() +"\decrypted_files\\"+nomUsu+"\Shared")):
            print("existo dentro")
        else:
            os.mkdir(os.getcwd() +"\decrypted_files\\"+nomUsu+"\Shared")
            print("creo dentro")
    else:
        os.mkdir(os.getcwd() +"\decrypted_files\\"+nomUsu)
        os.mkdir(os.getcwd() +"\decrypted_files\\"+nomUsu+"\Shared")
    rutaEn = os.getcwd()+"\encrypted_files\\"+nomUsu+"\Shared\\"+nombreDe
    #pathE = rutaEn.replace(os.sep, '/')
    #print(pathE)
    rutaDe = os.getcwd()+"\decrypted_files\\"+nomUsu+"\Shared\\"+nombreDe
    pathDe = Path(rutaDe)
    
    with open(rutaEn, "rb") as file1:
        data=file1.read()
        cipher2=AES.new(k0, AES.MODE_ECB)

        decrypted_data=unpad(cipher2.decrypt(data), 16)
        with open(pathDe, "wb") as file2:
           file2.write(decrypted_data)
        
        return decrypted_filename


#______________________________________________________________________________________________________________

conexion = db()
try:
    conexion.conectardb()
except Exception as e:
    print("No se ha podido conectar con la base de datos.")
    input("Pulsa cualquier tecla para continuar...")

eel.init(os.getcwd() + "\web")
#eel.init("C:/Users/Jaxti/OneDrive/Escritorio/Practica_2/web")


# Declaración de funciones que podrán llamarse desde javascript


@eel.expose
def check_log_py(user, password):
    aux_user= conexion.getUser(user)
    if aux_user == False:
        generateKeyRSA()
        ph = hashPass(password)
        privkeydb = encrypt_privada(privadoLlave, password)
        conexion.setUser(user, ph, pubKeyPEM, privkeydb)
        return user
        #check_log_py(user, password)
    else:
        passdb = conexion.getPass(aux_user)
        ph = hashPass(password)
        aux_p = comprobarPass(ph, passdb)
        if aux_p == False:
            
            print("la contraseña es incorrecta")
            return False
        else:            
            return True

@eel.expose
def getSharedUser(user):
    aux_user= conexion.getUser(user)
    if aux_user == False:
        return False
    else:       
        return True



@eel.expose
def auxbool():
    eel.go_to("/index.html")

@eel.expose
def auxlogout():
    eel.go_logout("/login.html")

# Esta función abre el seleccionador de archivos para
# más tarde pasar por parámetro el archivo seleccionado y
# simular que es javascript el encargado de hacer esta acción

@eel.expose
def eliminarFila(id, user, password):
    aux_user = conexion.getUser(user)
    passdb = conexion.getPass(aux_user)
    ph = hashPass(password)
    aux_p = comprobarPass(ph, passdb)
    if aux_p==True:
        conexion.borrarRegistroId(id)
        return True
    else:
        return False


@eel.expose
def select_file_py():
    # Preparamos la interfaz de selección de archivos
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    # Ejecutamos el seleccionador de archivos y guardamos
    # la ruta del archivo seleccionado
    global filepath
    filepath = askopenfilename()
    global nombreArchivo
    nombreArchivo = os.path.basename(filepath)
    global rutaArchivo
    rutaArchivo= os.path.dirname(filepath)
    # Enviamos el archivo seleccionado a javascript para
    # que actualice los valores correspondientes del formulario
    eel.select_file_js(filepath)

@eel.expose
def get_encrypted_files_list(usuario):
    id_user = conexion.getUser(usuario)
    archivos = conexion.getArchivosPropios(id_user)
    array = []
    for archivo in archivos:
        array.append(
            {
                "id":archivo[0],
                "name":archivo[1]
            }
        )
    return array

@eel.expose
def get_shared_files_list(usuario):
    id_user = conexion.getUser(usuario)
    archivos = conexion.getCompartidos(id_user)
    array = []
    for archivo in archivos:
        array.append(
            {
                "id":archivo[0],
                "name":archivo[1]
            }
        )
    return array
   

eel.start("login.html", port=8015)


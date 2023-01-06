from ModuloDeRecomendaciones.Usuario import Usuario
from ModuloDeConexionDeBaseDeDatos.Recomendacion import Recomendacion
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from datetime import datetime


def inicializar():
    if not firebase_admin._apps:
        cred = credentials.Certificate('C:/Users\SrDeLorean\Downloads\memoria-20027-firebase-adminsdk-ga3q6-da0abef5dc.json') 
        app = firebase_admin.initialize_app(cred, {'dbURL' : 'https://memoria-20027-default-rtdb.firebaseio.com/'})

def cargaDeDatos():
    usuarios = {}
    resp = db.reference('usuarios', None, 'https://memoria-20027-default-rtdb.firebaseio.com/').get()
    if(resp==None):
        return usuarios
    for element in resp:
        usuario = Usuario()
        usuario.idUsuario = resp[element]['idUsuario']
        usuario.nombre = resp[element]['nombre']
        usuario.apellido = resp[element]['apellido']
        usuario.idRecomendacion = 0
        usuario.estado = -1
        if('plantillas' in resp[element]):
            recomendaciones = {}
            for item in resp[element]['plantillas']:
                recomendacion = Recomendacion()
                recomendacion.nombre = resp[element]['plantillas'][item]['nombre']
                recomendacion.latitud = resp[element]['plantillas'][item]['latitud']
                recomendacion.tipoDeSuelo = resp[element]['plantillas'][item]['tipoDeSuelo']
                recomendacion.tipoDeCultivo = resp[element]['plantillas'][item]['tipoDeCultivo']
                recomendacion.ppredregocidad = resp[element]['plantillas'][item]['ppredregocidad']
                recomendacion.distanciaEntrePlantas = resp[element]['plantillas'][item]['distanciaEntrePlantas']
                recomendacion.distanciaEntreGotero = resp[element]['plantillas'][item]['distanciaEntreGotero']
                recomendacion.litosPorHora = resp[element]['plantillas'][item]['litosPorHora']
                recomendacion.mes = resp[element]['plantillas'][item]['mes']
                recomendacion.etapaDeCultivo = resp[element]['plantillas'][item]['etapaDeCultivo']
                recomendacion.profundidad = resp[element]['plantillas'][item]['profundidad']
                recomendacion.tiempoDeInfiltracion = resp[element]['plantillas'][item]['tiempoDeInfiltracion']            
                recomendaciones[recomendacion.nombre] = recomendacion
            usuario.recomendaciones = recomendaciones
        else:
            usuario.recomendaciones = {}
        usuarios[usuario.idUsuario] = usuario
    return usuarios

def getInformacionDb():
    resp = db.reference('estaciones', None, 'https://memoria-20027-default-rtdb.firebaseio.com/').get()
    return resp

def getTemperatura(estacion):
    resp = getInformacionDb()
    for element in resp:
        if(element == estacion):
            temperatura = 0
            temperaturaMenor = 1000
            temperaturaMayor = 0
            cantidad = 0
            for value in resp[element]:
                temperatura = temperatura + resp[element][value]["temperatura"]
                cantidad = cantidad + 1
                if(temperaturaMenor > resp[element][value]["temperatura"]):
                    temperaturaMenor = resp[element][value]["temperatura"]
                if(temperaturaMayor < resp[element][value]["temperatura"]):
                    temperaturaMayor = resp[element][value]["temperatura"]
            temperatura = temperatura/cantidad
            resultado = {"temperatura": temperatura, "temperaturaMenor": temperaturaMenor, "temperaturaMayor": temperaturaMayor}
            break
    return resultado
            
def getParametro(estacion, parametro):
    resp = getInformacionDb()
    respuesta = {}
    for element in resp: 
        if(element == estacion):
            x=0
            if(parametro == "viento"):
                respuesta["fecha"] = " direccion_viento" + " velocidad_viento" + " presion"
                for value in resp[element]:
                    identificador = resp[element][value]["fecha"] + " " + resp[element][value]["hora"]
                    respuesta[identificador] = resp[element][value]["direccion_viento"] + " " + str(resp[element][value]["velocidad_viento"]) + " " + str(resp[element][value]["presion"])
                    x=x+1
                    if(x==5):
                        break
            elif(parametro == "temperatura"):
                respuesta["fecha"] = " temperatura" + " luminosidad"
                for value in resp[element]:
                    identificador = resp[element][value]["fecha"] + " " + resp[element][value]["hora"]
                    temperatura = round(resp[element][value]["temperatura"], 1)
                    respuesta[identificador] = str(temperatura) + " " + str(resp[element][value]["luminosidad"])
                    x=x+1
                    if(x==5):
                        break
            else:
                for value in resp[element]:
                    respuesta["fecha"] = " " + parametro
                    identificador = resp[element][value]["fecha"] + " " + resp[element][value]["hora"]
                    respuesta[identificador] = str(resp[element][value][parametro])
                    x=x+1
                    if(x==5):
                        break
            break
    return respuesta

def getObtenerUsuarios(estacion, parametro):
    resp = getInformacionDb()
    respuesta = {}
    for element in resp: 
        if(element == usuarios):
            for value in resp[element]:
                respuesta["fecha"] = " " + parametro
                identificador = resp[element][value]["id"]
                respuesta[identificador] = str(resp[element][value][parametro])
    return respuesta

def postRegistrarUsuario(usuario):
    ref = db.reference('usuarios/'+str(usuario.idUsuario), None, 'https://memoria-20027-default-rtdb.firebaseio.com/')
    datos ={
            #
            "idUsuario": usuario.idUsuario,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "plantilla": [],
    }
    ref.set(datos)
    
   
def postPlantilla(idUsuario, plantilla):
    datos ={
        #variable con cambio casi imposible
        "nombre": plantilla.nombre,
        "latitud": plantilla.latitud,
        "tipoDeSuelo": plantilla.tipoDeSuelo,
        #variables con cambio poco comun
        "tipoDeCultivo": plantilla.tipoDeCultivo,
        "ppredregocidad": plantilla.ppredregocidad,
        "distanciaEntrePlantas": plantilla.distanciaEntrePlantas,
        "distanciaEntreGotero": plantilla.distanciaEntreGotero,
        "litosPorHora": plantilla.litosPorHora,
        #variables cambiantes
        "mes": plantilla.mes,
        "etapaDeCultivo": plantilla.etapaDeCultivo,
        "profundidad": plantilla.profundidad,
        "tiempoDeInfiltracion": plantilla.tiempoDeInfiltracion,
    }
    ref = db.reference('usuarios/'+str(idUsuario)+'/plantillas/'+plantilla.nombre, None, 'https://memoria-20027-default-rtdb.firebaseio.com/').set(datos)

def postRecomendacion(datoUsuario, datoPlantilla, datoRecomendacion):
    datos ={
        'usuario': {
            "idUsuario": datoUsuario.idUsuario,
            "nombre": datoUsuario.nombre,
            "apellido": datoUsuario.apellido,
        },
        'plantilla': {
            "nombre": datoPlantilla.nombre,
            "latitud": datoPlantilla.latitud,
            "tipoDeSuelo": datoPlantilla.tipoDeSuelo,
            "tipoDeCultivo": datoPlantilla.tipoDeCultivo,
            "ppredregocidad": datoPlantilla.ppredregocidad,
            "distanciaEntrePlantas": datoPlantilla.distanciaEntrePlantas,
            "distanciaEntreGotero": datoPlantilla.distanciaEntreGotero,
            "litosPorHora": datoPlantilla.litosPorHora,
            "mes": datoPlantilla.mes,
            "etapaDeCultivo": datoPlantilla.etapaDeCultivo,
            "profundidad": datoPlantilla.profundidad,
            "tiempoDeInfiltracion": datoPlantilla.tiempoDeInfiltracion
        },
        'recomendacion': {
            "eto": datoRecomendacion[0],
            "riegoBotadoFrecuencia": datoRecomendacion[1],
            "riegoBotadoTiempo": datoRecomendacion[2],
            "riegoGoteoFrecuencia": datoRecomendacion[3],
            "riegoGoteoTiempo": datoRecomendacion[4],
        }
    }
    dia = (datetime.today().strftime('%Y-%m-%d'))
    ref = db.reference('recomendaciones/'+str(datoUsuario.idUsuario)+':'+datoPlantilla.nombre+':'+dia, None, 'https://memoria-20027-default-rtdb.firebaseio.com/').set(datos)
    
def deleteRecomendacion(idUsuario, idRecomendacion):
    ref = db.reference('usuarios/'+str(idUsuario)+'/'+idRecomendacion, None, 'https://memoria-20027-default-rtdb.firebaseio.com/').delete()



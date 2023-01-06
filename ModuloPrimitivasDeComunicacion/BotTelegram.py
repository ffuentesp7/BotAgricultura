import logging
import json
from telegram.ext import *
from telegram import *
import sys 
import os
sys.path.append(os.path.abspath(""))
print(sys.path)
import ModuloDeProcesamientoDelLenguajeNatural.ProcesamientoDelLenguaje
import ModuloDeRecomendaciones.Recomendacion
from ModuloDeRecomendaciones.Recomendacion import Recomendacion
from ModuloDeRecomendaciones.Usuario import Usuario
import ModuloDeRecomendaciones.Decisiones 
import ModuloDeConexionDeBaseDeDatos.ConexionFirebase

API_KEY = '1946797475:AAGSHCt5sYhJI3QmitL6lvAxXEO8nX78cEc'
usuarios = {}

# Set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

#comando para inicializar al bot
def start_command(update, context):
    global usuarios
    if(usuarios.get(update.message.chat.id) == None):
        usuarios[update.message.chat.id] = Usuario() 
        usuarios[update.message.chat.id].idUsuario = update.message.chat.id
        usuarios[update.message.chat.id].nombre = update.message.chat.first_name
        usuarios[update.message.chat.id].apellido = update.message.chat.last_name
        ModuloDeConexionDeBaseDeDatos.ConexionFirebase.postRegistrarUsuario(usuarios[update.message.chat.id])
        update.message.reply_text('Hola, soy Sebastian, como es tu primera vez que entras te explicare en que te puedo ayudar:' + '\nPuedes preguntarme por variables como lo son la evapotranspiración, temperatura, humedad del suelo, precipitaciones y velocidad del viento del predio.' + '\nTambién te puedo dar recomendaciones de cuándo y cuánto regar por riego botado y goteo.' + '\nIntenta preguntarme algo…')
    else:
        update.message.reply_text('Hola de nuevo, soy Sebastian, usted ya se encuentra registrado, le volvere a repetir lo que puede hacer:' + '\nPuedes preguntarme por variables como lo son la evapotranspiración, temperatura, humedad del suelo, precipitaciones y velocidad del viento del predio.' + '\nTambién te puedo dar recomendaciones de cuándo y cuánto regar por riego botado y goteo.' + '\nIntenta preguntarme algo…')

def help_command(update, context):
    update.message.reply_text('Try typing anything and I will do my best to respond!')

def custom_command(update, context):
    update.message.reply_text('This is a custom command, you can add whatever text you want here.')

def handle_message(update, context):
    global usuarios
    entrada = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {entrada}')
    #procesamiento del lenguaje natural
    procesamiento = ModuloDeProcesamientoDelLenguajeNatural.ProcesamientoDelLenguaje.procesarPregunta(entrada);
    #procesamiento de recomendaciones
    lista = ModuloDeRecomendaciones.Decisiones.recomendacion(procesamiento)
    print(lista)
    if("riego" in lista):
        #pedir latitud
        groups = list()
        groups.append([InlineKeyboardButton(text='Nueva recomendacion', callback_data="new")])
        for recomendacion in usuarios[update.message.chat.id].recomendaciones:
            groups.append(
                [InlineKeyboardButton(text=usuarios[update.message.chat.id].recomendaciones[recomendacion].nombre,
                                      callback_data=recomendacion)]
            )
        update.message.reply_text(
            text='Selecciona la recomendación que desea utilizar:',
            reply_markup=InlineKeyboardMarkup(groups)
        )
        usuarios[update.message.chat.id].estado=0
    elif(usuarios[update.message.chat.id].estado==6):
        try:
            usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].profundidad = float(entrada)
            retorno = "Por favor, ingrese el porcentaje de pedregosidad (Ej: 20)"
            usuarios[update.message.chat.id].estado=7
        except ValueError:
            retorno = "Error al ingresar el dato, se le solicitaba un numero"
        update.message.reply_text(retorno)
    elif(usuarios[update.message.chat.id].estado==7):
        try:
            if(usuarios[update.message.chat.id].idRecomendacion=="new"):
                usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].ppredregocidad = float(entrada)
                usuarios[update.message.chat.id].estado=8
            else:
                usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].profundidad = float(entrada)
                usuarios[update.message.chat.id].estado=11
            retorno = "Por favor, ingrese la cantidad de minutos demora el agua de riego en infiltrar " + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].profundidad) + " centímetros"
        except ValueError:
            retorno = "Error al ingresar el dato, se le solicitaba un numero"
        update.message.reply_text(retorno)
    elif(usuarios[update.message.chat.id].estado==8):
        try:
            usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].tiempoDeInfiltracion = float(entrada)
            retorno = "Por favor, ingrese la distancia entre plantas en metros (Ej: 2.5)"
            usuarios[update.message.chat.id].estado=9
        except ValueError:
            retorno = "Error al ingresar el dato, se le solicitaba un numero"
        update.message.reply_text(retorno)
    elif(usuarios[update.message.chat.id].estado==9):
        try:
            usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].distanciaEntrePlantas = float(entrada)
            retorno = "Por favor, ingrese la distancia entre goteo en metros (Ej: 1.2)"
            usuarios[update.message.chat.id].estado=10
        except ValueError:
            retorno = "Error al ingresar el dato, se le solicitaba un numero"
        update.message.reply_text(retorno)
    elif(usuarios[update.message.chat.id].estado==10):
        try:
            usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].distanciaEntreGotero = float(entrada)
            retorno = "Por favor, ingrese la cantidad de litros por hora que expulsa un gotero (Ej: 2.2)"
            usuarios[update.message.chat.id].estado=11
        except ValueError:
            retorno = "Error al ingresar el dato, se le solicitaba un numero"
        update.message.reply_text(retorno)
    elif(usuarios[update.message.chat.id].estado==11):
        try:
            if(usuarios[update.message.chat.id].idRecomendacion=="new"):
                usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].litosPorHora = float(entrada)
            else:
                usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].tiempoDeInfiltracion = float(entrada)
            mensaje = ""
            mensaje = mensaje + 'Plantilla ' + str(usuarios[update.message.chat.id].idRecomendacion) + '\n'
            mensaje = mensaje + 'Latitud: ' +  str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].latitud) + "\n"
            mensaje = mensaje + 'Mes: ' + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].mes) + "\n"
            mensaje = mensaje + 'Tipo de suelo: ' + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].tipoDeSuelo) + "\n"
            mensaje = mensaje + 'Tipo de cultivo: ' +  str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].tipoDeCultivo) + "\n"
            mensaje = mensaje + 'Etapa del cultivo: ' + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].etapaDeCultivo) + "\n"
            mensaje = mensaje + 'Profundidad: ' + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].profundidad) + "\n"
            mensaje = mensaje + '% de pedregosidad: ' + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].ppredregocidad) + "\n"
            mensaje = mensaje + 'Tiempo de infiltración: ' + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].tiempoDeInfiltracion) + "\n"
            mensaje = mensaje + 'Distancia entre plantas: ' + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].distanciaEntrePlantas) + "\n"
            mensaje = mensaje + 'Distancia entre goteros: ' + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].distanciaEntreGotero) + "\n"
            mensaje = mensaje + 'Litros por hora: ' + str(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].litosPorHora) + "\n"
            update.message.reply_text(mensaje)
            recomendacion = usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].recomendacion()
            retorno = 'Recomendación' + '\n -Evapotranspiración ' + str(recomendacion[0]) + '\nRiego botado: ' + '\n -Frecuencia de riego ' + str(recomendacion[1]) + ' veces por semana' + '\n -Tiempo de riego: ' + str(recomendacion[2]) + ' minutos por hilera' + '\nRiego tecnificado: ' + '\n -Frecuencia de riego ' + str(recomendacion[3]) + ' veces por semana' + '\n -Tiempo de riego: ' + str(recomendacion[4]) + ' horas por semana'
            ModuloDeConexionDeBaseDeDatos.ConexionFirebase.postRecomendacion(usuarios[update.message.chat.id], usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion], recomendacion)
            if(usuarios[update.message.chat.id].idRecomendacion=="new"):
                retorno = retorno + '\n \n ¿Desea guardar esta plantilla de recomendación?'
                usuarios[update.message.chat.id].estado=12
            else:  
                usuarios[update.message.chat.id].estado=-1
        except ValueError:
            retorno = "Error al ingresar el dato, se le solicitaba un numero"
        update.message.reply_text(retorno)
    elif(usuarios[update.message.chat.id].estado==12):
        if(entrada=="si"):
            retorno = "Por favor, ingrese un nombre para la plantilla"
            usuarios[update.message.chat.id].estado=13
        else:
            retorno = "No se guardó esta plantilla de recomendación"
            del usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion]
            usuarios[update.message.chat.id].estado=-1
        update.message.reply_text(retorno)
    elif(usuarios[update.message.chat.id].estado==13):
        usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].nombre = entrada
        usuarios[update.message.chat.id].estado=-1
        retorno = "Se ha guardado la plantilla con el nombre: " + entrada
        update.message.reply_text(retorno)
        usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion].nombre = entrada
        ModuloDeConexionDeBaseDeDatos.ConexionFirebase.postPlantilla(update.message.chat.id, usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion])
        usuarios[update.message.chat.id].recomendaciones[entrada] = usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion]
        del(usuarios[update.message.chat.id].recomendaciones[usuarios[update.message.chat.id].idRecomendacion])
    else:
        #obtencion de datos
        if(not lista):
            text = "no entendí la pregunta, la puede repetir por favor"
            update.message.reply_text(text)
        else:
            text = ""
            for solicitud in lista:
                datos = ModuloDeConexionDeBaseDeDatos.ConexionFirebase.getParametro("curico", solicitud)
                text = text + json.dumps(datos)
            update.message.reply_text(text)



def recuperar_dato_botones(update, context):
    global usuarios
    if(usuarios[update.callback_query.message.chat.id].estado==0):
            #pedir latitud
        entrada = update.callback_query.data
        if(entrada=="new"):
            usuarios[update.callback_query.message.chat.id].nuevaRecomendacion(Recomendacion())
            update.callback_query.message.reply_text(
                text='Seleccione la región a la que pertenece:',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text='Arica y Parinacota', callback_data='-18'), InlineKeyboardButton(text='Tarapacá', callback_data='-21')],
                    [InlineKeyboardButton(text='Antofagasta', callback_data='-24'), InlineKeyboardButton(text='Atacama', callback_data='-27')],
                    [InlineKeyboardButton(text='Coquimbo', callback_data='-30'), InlineKeyboardButton(text='Valparaíso', callback_data='-32')],
                    [InlineKeyboardButton(text='Santiago', callback_data='-33'), InlineKeyboardButton(text='OHiggins', callback_data='-34')],
                    [InlineKeyboardButton(text='Maule', callback_data='-35'), InlineKeyboardButton(text='Ñuble', callback_data='-36')],
                    [InlineKeyboardButton(text='Biobío', callback_data='-37'), InlineKeyboardButton(text='La Araucanía norte', callback_data='-38')],
                    [InlineKeyboardButton(text='La Araucanía sur', callback_data='-39'), InlineKeyboardButton(text='Los Ríos', callback_data='-40')],
                    [InlineKeyboardButton(text='Los Lagos norte', callback_data='-42'), InlineKeyboardButton(text='Los Lagos sur', callback_data='-43')],
                    [InlineKeyboardButton(text='Aysén', callback_data='-45'), InlineKeyboardButton(text='Magallanes', callback_data='-52')],
                ])
            )
            usuarios[update.callback_query.message.chat.id].estado=1
        else:
            usuarios[update.callback_query.message.chat.id].idRecomendacion = entrada
            update.callback_query.message.reply_text(
                text='Selecciona el mes del año:',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text='Enero', callback_data='1'), InlineKeyboardButton(text='Julio', callback_data='7')],
                    [InlineKeyboardButton(text='Febrero', callback_data='2'), InlineKeyboardButton(text='Agosto', callback_data='8')],
                    [InlineKeyboardButton(text='Marzo', callback_data='3'), InlineKeyboardButton(text='Septiembre', callback_data='9')],
                    [InlineKeyboardButton(text='Abril', callback_data='4'), InlineKeyboardButton(text='Octubre', callback_data='10')],
                    [InlineKeyboardButton(text='Mayo', callback_data='5'), InlineKeyboardButton(text='Noviembre', callback_data='11')],
                    [InlineKeyboardButton(text='Junio', callback_data='6'), InlineKeyboardButton(text='Diciembre', callback_data='12')],
                ])
            )
            usuarios[update.callback_query.message.chat.id].estado=4
    elif(usuarios[update.callback_query.message.chat.id].estado==1):
        #pedir mes
        callback_data = update.callback_query.data

        usuarios[update.callback_query.message.chat.id].recomendaciones[usuarios[update.callback_query.message.chat.id].idRecomendacion].latitud = int(callback_data)
        update.callback_query.message.reply_text(
            text='Selecciona el mes del año:',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Enero', callback_data='1'), InlineKeyboardButton(text='Julio', callback_data='7')],
                [InlineKeyboardButton(text='Febrero', callback_data='2'), InlineKeyboardButton(text='Agosto', callback_data='8')],
                [InlineKeyboardButton(text='Marzo', callback_data='3'), InlineKeyboardButton(text='Septiembre', callback_data='9')],
                [InlineKeyboardButton(text='Abril', callback_data='4'), InlineKeyboardButton(text='Octubre', callback_data='10')],
                [InlineKeyboardButton(text='Mayo', callback_data='5'), InlineKeyboardButton(text='Noviembre', callback_data='11')],
                [InlineKeyboardButton(text='Junio', callback_data='6'), InlineKeyboardButton(text='Diciembre', callback_data='12')],
            ])
        )
        usuarios[update.callback_query.message.chat.id].estado=2
    elif(usuarios[update.callback_query.message.chat.id].estado==2):
        #tipo de suelo
        callback_data = update.callback_query.data
        usuarios[update.callback_query.message.chat.id].recomendaciones[usuarios[update.callback_query.message.chat.id].idRecomendacion].mes = int(callback_data)
        update.callback_query.message.reply_text(
            text='Selecciona el tipo de suelo:',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Arenoso', callback_data='arenoso')],
                [InlineKeyboardButton(text='Franco', callback_data='franco')],
                [InlineKeyboardButton(text='Franco arenoso', callback_data='franco arenoso')],
                [InlineKeyboardButton(text='Franco arcilloso', callback_data='franco arcilloso')],
                [InlineKeyboardButton(text='Arcilloso arenoso', callback_data='arcilloso arenoso')],
                [InlineKeyboardButton(text='Arcilloso', callback_data='arcilloso')],
            ])
        )
        usuarios[update.callback_query.message.chat.id].estado=3
    elif(usuarios[update.callback_query.message.chat.id].estado==3):
        #tipo de cultivo
        callback_data = update.callback_query.data
        usuarios[update.callback_query.message.chat.id].recomendaciones[usuarios[update.callback_query.message.chat.id].idRecomendacion].tipoDeSuelo = callback_data
        update.callback_query.message.reply_text(
            text='Selecciona el tipo de cultivo:',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Ajo', callback_data='Ajo'), InlineKeyboardButton(text='Alfalfa', callback_data='Alfalfa'), InlineKeyboardButton(text='Almendro', callback_data='Almendro')],
                [InlineKeyboardButton(text='Arándano 1°año', callback_data='Arándano 1°año'), InlineKeyboardButton(text='Arándano 2°año', callback_data='Arándano 2°año'), InlineKeyboardButton(text='Arándano 3°año', callback_data='Arándano 3°año')],
                [InlineKeyboardButton(text='Arveja, fresca', callback_data='Arveja, fresca'), InlineKeyboardButton(text='Cebolla seca', callback_data='Cebolla seca'), InlineKeyboardButton(text='Cebolla verde', callback_data='Cebolla verde')],
                [InlineKeyboardButton(text='Ciruelo', callback_data='Ciruelo'), InlineKeyboardButton(text='Coliflor', callback_data='Coliflor'), InlineKeyboardButton(text='Duraznero', callback_data='Duraznero')],
                [InlineKeyboardButton(text='Espárragos', callback_data='Espárragos'), InlineKeyboardButton(text='Frambuesa', callback_data='Frambuesa'), InlineKeyboardButton(text='Kiwi', callback_data='Kiwi')],
                [InlineKeyboardButton(text='Maíz dulce', callback_data='Maíz dulce'), InlineKeyboardButton(text='Maíz grano', callback_data='Maíz grano'), InlineKeyboardButton(text='Maní', callback_data='Maní')],
                [InlineKeyboardButton(text='Manzano', callback_data='Manzano'), InlineKeyboardButton(text='Maravilla', callback_data='Maravilla'), InlineKeyboardButton(text='Nectarino', callback_data='Nectarino')],
                [InlineKeyboardButton(text='Nogal', callback_data='Nogal'), InlineKeyboardButton(text='Olivo', callback_data='Olivo'), InlineKeyboardButton(text='Palto', callback_data='Palto')],
                [InlineKeyboardButton(text='Papa', callback_data='Papa'), InlineKeyboardButton(text='Peral', callback_data='Peral'), InlineKeyboardButton(text='Pimentón', callback_data='Pimentón')],
                [InlineKeyboardButton(text='Poroto seco', callback_data='Poroto seco'), InlineKeyboardButton(text='Poroto verde', callback_data='Poroto verde'), InlineKeyboardButton(text='Pradera', callback_data='Pradera')],
                [InlineKeyboardButton(text='Remolacha', callback_data='Remolacha'), InlineKeyboardButton(text='Sandia', callback_data='Sandia'), InlineKeyboardButton(text='Tabaco', callback_data='Tabaco')],
                [InlineKeyboardButton(text='Tomate', callback_data='Tomate'), InlineKeyboardButton(text='Tngo', callback_data='Tngo'), InlineKeyboardButton(text='Vid', callback_data='Vid')],
            ])
        )
        usuarios[update.callback_query.message.chat.id].estado=4
    elif(usuarios[update.callback_query.message.chat.id].estado==4):
        #tipo de cultivo
        callback_data = update.callback_query.data
        if(usuarios[update.callback_query.message.chat.id].idRecomendacion=="new"):
            usuarios[update.callback_query.message.chat.id].recomendaciones[usuarios[update.callback_query.message.chat.id].idRecomendacion].tipoDeCultivo = callback_data
        else:
            usuarios[update.callback_query.message.chat.id].recomendaciones[usuarios[update.callback_query.message.chat.id].idRecomendacion].mes = int(callback_data)
        update.callback_query.message.reply_text(
            text='Selecciona la etapa del cultivo:',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Inicial', callback_data='Inicial')],
                [InlineKeyboardButton(text='Desarrollo', callback_data='Desarrollo')],
                [InlineKeyboardButton(text='Medios', callback_data='Medios')],
                [InlineKeyboardButton(text='Finales', callback_data='Finales')],
                [InlineKeyboardButton(text='Cosecha', callback_data='Cosecha')]
            ])
        )
        usuarios[update.callback_query.message.chat.id].estado=5
    elif(usuarios[update.callback_query.message.chat.id].estado==5):
        #tipo de cultivo
        callback_data = update.callback_query.data
        usuarios[update.callback_query.message.chat.id].recomendaciones[usuarios[update.callback_query.message.chat.id].idRecomendacion].etapaDeCultivo = callback_data
        if(usuarios[update.callback_query.message.chat.id].idRecomendacion=="new"):
            usuarios[update.callback_query.message.chat.id].estado=6
        else:
            usuarios[update.callback_query.message.chat.id].estado=7
        update.callback_query.message.reply_text("Por favor, ingrese la profundidad de las raíces en el campo en centímetros")

def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')

def cargarRecomendaciones():
    #recomendaciones[]
    datos = ModuloDeConexionDeBaseDeDatos.ConexionFirebase.getParametro("usuarios", "")
    text = text + json.dumps(datos)

# Run the programme
if __name__ == '__main__':
    ModuloDeConexionDeBaseDeDatos.ConexionFirebase.inicializar()
    usuarios = ModuloDeConexionDeBaseDeDatos.ConexionFirebase.cargaDeDatos()
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))
    dp.add_handler(CallbackQueryHandler(recuperar_dato_botones) )
    

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()
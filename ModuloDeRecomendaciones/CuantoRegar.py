import pandas as pd
import ModuloDeRecomendaciones.Hargreaves as Hargreaves

pathArchivo = 'ModuloDeRecomendaciones/Coeficientesdecultivosreferencial.xlsx'

#Para utilizar esta funcion se necesita lo siguiente
#tipoDeCultivo => tipo de cultivo del predio
#etapaDeCultivo => etapa en que se encuentra el cultivo
def cuantoRegar(tipoDeCultivo, etapaDeCultivo, eto):
    etapaDeCultivoArchivo = 0
    if(etapaDeCultivo == 'Inicial'):
        etapaDeCultivoArchivo = 1
    elif(etapaDeCultivo == 'Desarrollo'):
        etapaDeCultivoArchivo = 2
    elif(etapaDeCultivo == 'Medios'):
        etapaDeCultivoArchivo = 3
    elif(etapaDeCultivo == 'Finales'):
        etapaDeCultivoArchivo = 4
    elif(etapaDeCultivo == 'Cosecha'):
        etapaDeCultivoArchivo = 5
    #cargar archivo con valores de kc
    archivo = pd.read_excel(pathArchivo, sheet_name='Hoja1')
    pivote = archivo.iloc[:, 0]
    columna = archivo.iloc[:, etapaDeCultivoArchivo]
    i=0
    largo = len(pivote)
    while(i<largo):
        if(pivote[i] == tipoDeCultivo):
            #extraer valor de kc
            if(columna[i]!='-'):
                valores = columna[i].split("-")
                suma = 0
                i = 0
                for valor in valores:
                    suma = suma+float(valor)
                    i = i + 1
                kc = suma/i
                break
            else:
                kc = 0.3
                break
        i=i+1
    #obtener la eto
    #eto = Hargreaves.calcularEvotranspiracion()
    #calculo de etc en mm/semana
    resultado = eto*kc*7
    #devolver el resultado
    return resultado


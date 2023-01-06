import ModuloDeRecomendaciones.CuantoRegar as CuantoRegar
import ModuloDeRecomendaciones.Hargreaves as Hargreaves
import ModuloDeRecomendaciones.HumedadAprovechable as HumedadAprovechable
import ModuloDeRecomendaciones.RiegoBotado as RiegoBotado
import ModuloDeRecomendaciones.RiegoPorGoteo as RiegoPorGoteo
import math

class Recomendacion():
    
    #variable con cambio casi imposible
    nombre = "Por definir"
    latitud = 0
    tipoDeSuelo = 0
    #variables con cambio poco comun
    tipoDeCultivo = 0
    ppredregocidad = 0
    distanciaEntrePlantas = 0
    distanciaEntreGotero = 0
    litosPorHora = 0
    #variables cambiantes
    mes = 0
    etapaDeCultivo = 0
    profundidad = 0
    tiempoDeInfiltracion = 0
    #variable utilizada por el bot para determinar el estado

    def recomendacion(self):
        respuesta = 'Recomendacion: \n frecuencia de riego: 1 vez \n tiempo de riego: 100 minutos' 


        eto = Hargreaves.calcularEvotranspiracion(self.mes, self.latitud)

        etcmmsemana = CuantoRegar.cuantoRegar(self.tipoDeCultivo, self.etapaDeCultivo, eto)

        ha = HumedadAprovechable.calcularHumedadAprovechable(self.tipoDeSuelo, self.profundidad, self.ppredregocidad)

        riegoBotadoFrecuencia = RiegoBotado.frecuenciaDeRiego(ha, etcmmsemana)
        riegoBotadoTiempo = RiegoBotado.tiempoDeRiego(self.tiempoDeInfiltracion)

        riegoGoteoFrecuencia = RiegoPorGoteo.frecuenciaDeRiego(ha, etcmmsemana)
        riegoGoteoTiempo = RiegoPorGoteo.tiempoDeRiego(self.distanciaEntrePlantas, self.distanciaEntreGotero, self.litosPorHora, etcmmsemana)

        eto = round(eto, 2)
        etcmmsemana = round(etcmmsemana, 2)
        ha = round(ha, 2)
        riegoBotadoFrecuencia = round(riegoBotadoFrecuencia, 1)
        riegoBotadoTiempo = round(riegoBotadoTiempo, 0)
        riegoGoteoFrecuencia = round(riegoGoteoFrecuencia, 1)
        riegoGoteoTiempo = round(riegoGoteoTiempo, 0)

        
        print('-------------------------------------------------')
        print('etc mm/semana: ', etcmmsemana)
        print('evapotranspiracion: ', eto)
        print('humedad aprovechable: ', ha)
        print('riegoBotadoFrecuencia: ', riegoBotadoFrecuencia)
        print('riegoBotadoTiempo: ', riegoBotadoTiempo)
        print('riegoGoteoFrecuencia: ', riegoGoteoFrecuencia)
        print('riegoGoteoTiempo: ', riegoGoteoTiempo)
        print('-------------------------------------------------')

        respuesta = [eto,riegoBotadoFrecuencia, riegoBotadoTiempo, riegoGoteoFrecuencia, riegoGoteoTiempo]
        return respuesta
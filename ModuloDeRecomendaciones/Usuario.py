import ModuloDeRecomendaciones.CuantoRegar as CuantoRegar
import ModuloDeRecomendaciones.Hargreaves as Hargreaves
import ModuloDeRecomendaciones.HumedadAprovechable as HumedadAprovechable
import ModuloDeRecomendaciones.RiegoBotado as RiegoBotado
import ModuloDeRecomendaciones.RiegoPorGoteo as RiegoPorGoteo
import math

class Usuario():
    
    #variable con cambio casi imposible
    idUsuario = 0
    nombre = ""
    apellido = ""
    idRecomendacion = ""
    estado = -1
    recomendaciones = {}
    
    def nuevaRecomendacion(self, recomendacion):
        print('a')
        self.recomendaciones["new"] = recomendacion
        print('b')
        self.idRecomendacion = "new"
        print('c')
        
    
    def modificarRecomendacion(self, id, recomendacion):
        self.recomendaciones[id] = recomendacion
    
    def eliminarRecomendacion(self, id):
        del self.recomendaciones[id]
    
    def obtenerRecomendacion(self, id):
        respuesta = self.recomendaciones[id]
        return respuesta

    def recomendacion(self, id):
        respuesta = self.recomendaciones[id].recomendacion
        return respuesta
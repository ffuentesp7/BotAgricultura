import stanza
from fuzzywuzzy import process

stopwork = ["a", "acá", "ahí", "ajena", "ajeno", "ajenos", "ajenas", "al", "algo", "algún", "alguna", "alguno", "algunas", "algunos", "allá", "allí", "ambos", "ante", "antes", "aquel", "aquella", "aquello", "aquellas", "aquellos", "aquí", "arriba", "así", "atrás", "aun", "aunque", "bajo", "bastante", "bien", "cabe", "cada", "casi", "cierto", "cierta", "ciertas", "ciertos", "como", "con", "conmigo", "conseguimos", "conseguir", "consigo", "consigue", "consiguen", "consigues", "contigo", "contra", "cual", "cuales", "cualquier", "cualquiera", "cualquieras", "cuan", "cuando", "cuanto", "cuanta", "cuantas", "cuantos", "de", "dejar", "del", "demás", "demasiada", "demasiado", "demasiadas", "demasiados", "dentro", "desde", "donde", "dos", "el", "él", "ella", "ello", "ellas", "ellos", "empleáis", "emplean", "emplear", "empleas", "empleo", "en", "encima", "entonces", "entre", "era", "eras", "éramos", "eran", "eres", "es", "esa", "ese", "eso", "esas", "eses", "esos", "esta", "estas", "estaba", "estado", "estáis", "estamos", "están", "estar", "este", "esto", "estés", "estos", "estoy", "etc", "fin", "fue", "fueron", "fui", "fuimos", "gue", "no", "ha", "hace", "haces", "hacéis", "hacemos", "hacen", "hacer", "hacia", "hago", "hasta", "incluso", "intenta", "intentas", "intentáis", "intentamos", "intentan", "intentar", "intento", "ir", "jamás", "junto", "juntos", "la", "lo", "las", "los", "largo", "más", "me", "menos", "mi", "mis", "mía", "mías", "mientras", "mío", "míos", "misma", "mismo", "mismas", "mismo", "modo", "mucha", "muchas", "muchísima", "muchísimo", "muchísimas", "muchísimos", "mucho", "muchos", "muy", "nada", "ni", "ningún", "ninguna", "ninguno", "ningunas", "ningunos", "no", "nos", "nosotras", "nosotros", "nuestra", "nuestro", "nuestras", "nuestros", "nunca", "os", "otra", "otro", "otras", "otros", "para", "parecer", "pero", "poca", "poco", "pocos", "pocas", "podéis", "podemos", "poder", "podría", "podrías", "podríais", "podríamos", "podrían", "por", "porque", "primero", "puede", "pueden", "puedo", "pues", "que", "qué", "querer", "quién", "quiénes", "quienes", "quiera", "quien", "quizá", "quizás", "sabe",  "sabes", "saben", "sabéis", "sabemos", "saber", "se", "según", "ser", "si", "sí", "siempre", "siendo", "sin", "sino", "so", "sobre", "sois", "solamente", "solo", "sólo", "somos", "soy", "sr", "sra", "sres", "sta", "su", "sus", "suya", "suyo", "suyas", "suyos", "tal", "tales", "también", "tampoco", "tan", "tanta", "tanto", "tantas", "tantos", "te", "tenéis", "tenemos", "tener", "tengo", "ti", "tiempo", "tiene", "tienen", "toda", "todo", "todas", "todos", "tomar", "trabaja", "trabajo", "trabajáis", "trabajamos", "trabajan", "trabajar", "trabajas", "tras", "tú", "tu", "tus", "tuya", "tuyo", "tuyas", "tuyos", "último", "ultimo", "un", "una", "uno", "unas", "unos", "usas", "usáis", "usamos", "usan", "usar", "uso", "usted", "ustedes", "va", "van", "vais", "valor", "vamos", "varias", "varios", "vaya", "verdadera", "vosotras", "vosotros", "voy", "vuestra", "vuestro", "vuestras", "vuestros", "y", "ya", "yo"]
campo = ["campo", "sector", "superficie", "zona", "tierra", "suelo"]
riego=["regar", "inundación", "boca", "abertura", "caudal", "compuerta", "fertirriego", "llave", "mezcla", "nebulización", "pie", "pivote", "quimiorriego", "ramal", "bomba", "riego", "terminal", "técnica", "toma", "pulverización", "puesta"]
temperatura= ["temperatura", "calor", "calentamiento", "bochorno", "calidez", "tibieza", "calorcillo", "incandescencia", "quemazón", "achicharramiento", "escaldadura", "recalentamiento", "sofoco", "sofocación", "agobio", "abrasador", "caluroso", "quemar"]
humedadDelSuelo= ["seco", "reseco", "humedad", "absorción", "aspiración", "déficit", "demanda", "disponibilidad", "estrés", "filtración", "profunda", "humectación", "infiltración", "matricial", "necesidad", "pantano", "percolación", "permeabilidad", "profundidad", "reserva", "retención"]
evapotranspiracion= ["evapotranspiracion", "absortividad", "pérdidas", "preservación", "marchitamiento"]
precipitaciones=["precipitación", "pluviosidad", "calima", "camanchaca", "celaje", "cellisca", "cencellada", "escarcha", "chaparrón", "diluvio", "granizo", "lluvia", "Nevasca", "niebla", "nieve", "rocío", "tormenta", "aguacero", "precipitación", "chubasco", "temporal", "tempestad", "agua", "sábana", "cortina", "tromba", "turbión", "turbonada", "galerna", "argavieso", "borrasca", "inclemencia", "rociada", "llovizna", "calabobos", "cellisca", "mollizna", "granizo", "pedrisco", "aguanieve", "nevada", "nube", "nubarrada", "nubarrón", "racha", "catarata", "torrente", "inundación", "riada", "mojadura", "caladura", "salpicadura", "helada", "sereno", "relente"]
velocidadDelViento=["velocidad", "viento", "ábrego", "alisios", "cierzo", "galerna", "lebeche", "levante", "mediodía", "mistral", "poniente", "siroco", "solano", "tramontana", "vendaval", "borrasca", "tempestad", "temporal", "inclemencia", "galerna", "huracán", "turbión", "ciclón", "torbellino", "tromba", "remolino", "tornado", "baguio", "tifón", "vendaval", "viento", "viento", "huracanado", "ventarrón", "ventisca", "ráfaga", "ventolera", "cerrazón", "nube", "niebla", "bruma", "exhalación", "relámpago", "trueno", "tronada"]

nlp = stanza.Pipeline('es')

def procesarPregunta(palabras):
    ok=[]
    ok=riego+temperatura+humedadDelSuelo+evapotranspiracion+precipitaciones+velocidadDelViento+campo
    nuevaEntrada = ""
    palabras = palabras.split(' ')
    for palabra in palabras:
        aprox=process.extractOne(palabra, ok)
        aprox2=process.extractOne(palabra, stopwork)
        if(aprox[1]>=80 and len(palabra)>3):
            if aprox2[1]>=95 or palabra in stopwork:
                nuevaEntrada+=palabra + " "
            else:
                nuevaEntrada+=aprox[0] + " "
        else:
            nuevaEntrada+=palabra + " "
    pregunta = nlp(nuevaEntrada)
    verbos = []
    for palabra in pregunta.sentences[0].words:
        if(palabra.upos != "PUNCT"):
            verbos.append(palabra.lemma)
    return verbos
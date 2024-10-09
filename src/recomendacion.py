from pyDatalog import pyDatalog

# Creación de términos
pyDatalog.create_terms('estado, recomendacion, actividad, X, Y')

# Hechos iniciales
+estado('Lulu', 'feliz')

# Reglas para recomendaciones
recomendacion('Lulu', 'dormir') <= estado('Lulu', 'cansado')
recomendacion('Lulu', 'jugar') <= estado('Lulu', 'feliz')
recomendacion('Lulu', 'comer') <= estado('Lulu', 'hambriento')
recomendacion('Lulu', 'ducharse') <= estado('Lulu', 'sucio')

# Actividades disponibles
+actividad('jugar', 'Adivina el Número')
+actividad('jugar', 'Piedra, Papel, Tijeras')
+actividad('dormir', 'Dormir una siesta')
+actividad('comer', 'Preparar una merienda saludable')
+actividad('ducharse', 'Tomar una ducha refrescante')

# Función para obtener recomendaciones
def obtener_recomendaciones():
    resultados = recomendacion('Lulu', X) & actividad(X, Y)
    recomendaciones = [str(Y) for Y in resultados]
    return recomendaciones



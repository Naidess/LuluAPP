from functools import reduce

class EstadoFelicidad:
    def __init__(self, energia, aburrido, salud):
        self.energia = energia
        self.aburrido = aburrido
        self.salud = salud

# Función para calcular la felicidad promedio de Lulu
def calcular_felicidad_promedio(estado_felicidad):
    # Definir los pesos para cada métrica (porcentajes)
    pesos = {
        'energia': 0.4,
        'aburrido': 0.3,
        'salud': 0.3
    }

    # Calcular la felicidad promedio ponderada
    felicidad_promedio = reduce(lambda acc, key: acc + estado_felicidad.__dict__[key] * pesos[key], pesos.keys(), 0)
    
    return felicidad_promedio

#prueba
if __name__ == "__main__":
    estado_lulu = EstadoFelicidad(energia=80, aburrido=20, salud=90)
    felicidad_promedio = calcular_felicidad_promedio(estado_lulu)
    # Mostrar el resultado
    print(f"Felicidad promedio de Lulu: {felicidad_promedio}")

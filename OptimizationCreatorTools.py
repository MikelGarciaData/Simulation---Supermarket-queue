import numpy as np
import matplotlib.pyplot as plt
from Calendario import Calendario
from Reloj import Reloj
from Cola import Cola
from Cajas import Cajas
from solutionCreatorTools import solucionASimulacion, diffConsecutivas
from statisticsAndFunctions import calidad, funcionObjetivo, calcularMedia, calcularPercentil
from simulacion import simulationLoop

def plotSilueta(cola):
    lenCola = np.array(cola.longitudCola)
    plt.title(f"Última hora registrada: {round(lenCola[-1,0], 4)}")
    plt.scatter(lenCola[:,0], lenCola[:,1], s=1)
    plt.xlabel("t")
    plt.ylabel("longitud cola")
    plt.xlim(9, 24)
    plt.ylim()
    plt.show()


def probarSolucion(df, simSolucion):

    # Listas de estadisticos
    areaTotal = []
    percTotal = []

    # Calcular calendario de relevos
    empleadosTurnos = [e[1] for e in simSolucion]

    # Calcular numero de maximo de instancias Cajero
    maximo = max(empleadosTurnos)

    cjrs = Cajas(maximo)


    # Obtener un dia de los datos for day in data...
    days = df["DIA"].unique()
    for i in days:
        dff = df[df["DIA" ] == i]

        # Vectores de eventos
        eventosEntrada = [(row[0], row[1]["Entrada"]) for row in dff.iterrows()]
        eventosFinCompra = [(row[0], row[1]["FinCompra"]) for row in dff.iterrows()]
        TiemposPago = [(row[0], row[1]["TiempoPago"]) for row in dff.iterrows()]
        empleadosTurnos = [e[1] for e in simSolucion]
        difTurnos = diffConsecutivas(empleadosTurnos)

        # Crear una instancia de reloj, calendario y cajas
        # Crear instancias para la simulacion
        rlj = Reloj()
        empleados = empleadosTurnos.pop(0)
        difTurno = difTurnos.pop(0)

        cld = Calendario(eventosEntrada, eventosFinCompra, maximo, empleados, difTurno)
        cola = Cola()

        # Cambiar el estado inicial de los cajeros
        varsCajero = [x for x in vars(cld).keys() if ("cajeroLibre" in x)]
        cajeros = list({k: vars(cld)[k] for k in varsCajero}.items())
        for cajero, caja in zip(cjrs.cajeros.values(), cajeros):
            if caja[1][1 ]==100:
                cajero.setActivo(True)


        # Lanzar simulacion
        cola = simulationLoop(rlj, cld, cjrs, cola, eventosEntrada, eventosFinCompra, TiemposPago, difTurnos, verbose=False)
        #plotSilueta(cola)


        areaTotal.append( calcularMedia(cola) )
        percTotal.append( calcularPercentil(cola) )

        del cola


    areaTotal = np.array(areaTotal)
    percTotal = np.array(percTotal)

    return areaTotal, percTotal

# Path relinking
def path_relinking(df, solucion_a, solucion_b, costeCompleta, maximoObj, minimoObj):
    # Convertir las soluciones a vectores
    vector_a = np.concatenate(solucion_a)
    vector_b = np.concatenate(solucion_b)

    # Calcular la distancia euclidiana entre los vectores
    distancia = np.sqrt(((vector_a - vector_b) ** 2).sum())

    # Si la distancia es menor que 1, las soluciones son iguales
    if distancia < 1:
        return solucion_a

    # Generar una lista de soluciones intermedias
    soluciones_intermedias = [vector_a]

    for alpha in np.linspace(0.1, 0.9, 9):
        soluciones_intermedias.append(np.around( (alpha * vector_a) + ((1 - alpha) * vector_b) ).astype(int))

    soluciones_intermedias.append(vector_b)

    # Seleccionar la mejor solución intermedia
    mejor_solucion = None
    mejor_objetivo = -np.inf

    for solucion_intermedia in soluciones_intermedias:
        # Convertir la solución intermedia a la forma original
        solucion_intermedia = [solucion_intermedia[:5],
                               solucion_intermedia[5:12],
                               solucion_intermedia[12:]]

        # Calcular el valor de la función objetivo para la solución intermedia
        objetivo = funcionObjetivo(solucion_intermedia, costeCompleta)

        simSolucion = solucionASimulacion(solucion_intermedia)
        area, perc = probarSolucion(df, simSolucion)

        areaTotal = area.sum(axis=0)
        areaTotal = areaTotal[0] / areaTotal[1]

        percTotal = perc.sum(axis=0)
        percTotal = percTotal[0] / percTotal[1]

        puntuacion = calidad(maximoObj, minimoObj, objetivo, areaTotal, percTotal)
        print("objetivo solucion intermedia: ", objetivo, areaTotal, percTotal, puntuacion)

        # Actualizar la mejor solución
        if puntuacion > mejor_objetivo:
            mejor_objetivo = puntuacion
            mejor_solucion = solucion_intermedia

    return mejor_solucion



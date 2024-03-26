import numpy as np
from solutionCreatorTools import crearSolucion, solucionASimulacion
from statisticsAndFunctions import funcionObjetivo, lossFunction
from OptimizationCreatorTools import path_relinking, probarSolucion


def main_loop_populated(df, poblacion=10, maxiter=10, maximoEmpleados=2, costeCompleta=100, useLoss=False, random_seed=100):
    np.random.seed(random_seed)
    # Listas para guardar las soluciones
    soluciones = []
    relinking = []

    probabilidades= None

    # Listas para guardar la poblacion y sus parametros
    pplt = []
    objetivos = []
    areas = []
    percentiles = []

    # Definir la solución inicial como la mejor solución encontrada en las iteraciones anteriores
    mejor_solucion = None
    mejor_objval = np.inf

    for i in range(poblacion):
        [objC, objR, objP], simSolucion = crearSolucion(maximoEmpleados)
        objval = funcionObjetivo([objC, objR, objP], costeCompleta)
        area, perc = probarSolucion(df, simSolucion)
        soluciones.append({"solucion": [objC, objR, objP],
                           "obj": objval,
                           "area": area,
                           "perc": perc})

        pplt.append([objC, objR, objP])
        objetivos.append(objval)
        areas.append(area)
        percentiles.append(perc)

        areatotal = area.sum(axis=0)
        perctotal = perc.sum(axis=0)
        print("Simulada: ", objval, areatotal[0] / areatotal[1], perctotal[0] / perctotal[1])

        # Actualizar la mejor solución si la solución actual es mejor
        if objval < mejor_objval:
            mejor_solucion = [objC, objR, objP]
            mejor_objval = objval
            mejor_area = area
            mejor_perc = perc


    # calcular la importancia de cada objetivo
    if useLoss:
        veros = lossFunction(objetivos, areas, percentiles)
        probabilidades = veros/veros.sum()

    # Aplicar Path Relinking
    for i in range(maxiter):
        i1, i2 = np.random.choice(len(pplt), size=2, replace=False, p=probabilidades)
        solucion_a, solucion_b = pplt[i1], pplt[i2]
        solucion_intermedia = path_relinking(df, solucion_a, solucion_b, costeCompleta, max(objetivos), min(objetivos))

        print(solucion_a)
        print(solucion_b)
        print(solucion_intermedia)

        simIntermedia = solucionASimulacion(solucion_intermedia)

        objval_intermedia = funcionObjetivo(solucion_intermedia, costeCompleta)
        area_intermedia, perc_intermedia = probarSolucion(df, simIntermedia)
        areatotal_intermedia = area_intermedia.sum(axis=0)
        perctotal_intermedia = perc_intermedia.sum(axis=0)

        relinking.append({"solucion": solucion_intermedia,
                              "obj": objval_intermedia,
                              "area": area_intermedia,
                              "perc": perc_intermedia})

        print("Relinking", objval_intermedia, areatotal_intermedia[0] / areatotal_intermedia[1],
                  perctotal_intermedia[0] / perctotal_intermedia[1])

        # Actualizar la mejor solución si la solución intermedia es mejor
        if objval_intermedia < mejor_objval:
            mejor_solucion = solucion_intermedia
            mejor_objval = objval_intermedia
            mejor_area = area_intermedia
            mejor_perc = perc_intermedia

    return {"solucion": mejor_solucion, "obj": mejor_objval, "area": mejor_area, "perc": mejor_perc}, soluciones, relinking

#df = pd.read_excel("DatosTrabajoSupermercado_estud.xlsx")
#c = main_loop_populated(df, poblacion=5, maxiter=10, maximoEmpleados=2, costeCompleta=100, random_seed=100)
import numpy as np


def jornada_completa(por_hora ):
    #                       9  10 11 12 13 14 15 16 17 18 10 20
    cronograma = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], # empieza a las 9
                           [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0], # empieza a las 10
                           [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], # empieza a las 11
                           [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0], # empieza a las 12
                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]]  )# empieza a las 13

    por_turno = por_hora * cronograma

    return por_hora.flatten(), por_turno.sum(axis=0)




def jornada_reducida(por_hora):
    #                       9  10 11 12 13 14 15 16 17 18 10 20
    cronograma = np.array([[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], # empieza a las 9
                           [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0], # empieza a las 10
                           [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], # empieza a las 11
                           [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0], # empieza a las 12
                           [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0], # empieza a las 13
                           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0], # empieza a las 14
                           [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]]  )# empieza a las 15

    por_turno = por_hora * cronograma

    return por_hora.flatten(), por_turno.sum(axis=0)


def jornada_parcial(por_hora):
    #                       9  10 11 12 13 14 15 16 17 18 10 20
    cronograma = np.array([[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], # empieza a las 9
                           [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], # empieza a las 10
                           [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0], # empieza a las 11
                           [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0], # empieza a las 12
                           [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0], # empieza a las 13
                           [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0], # empieza a las 14
                           [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0], # empieza a las 15
                           [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0], # empieza a las 16
                           [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]]  )# empieza a las 17

    por_turno = por_hora * cronograma

    return por_hora.flatten(), por_turno.sum(axis=0)


def calcular_solucion(comp, redc, parc):
    return [(hora, cantidad) for hora, cantidad in zip(range(9, 21), comp + redc + parc)]

def diffConsecutivas(array):
    diff = []
    for i in range(1, len(array)):
        diff.append(array[i]-array[i-1])
    diff.append(0)
    return diff

def crearSolucion(maximoEmpleados):
    # Crear solucion

    # Obtener num empleados por hora (obj.) y por turno
    por_hora = np.random.randint(maximoEmpleados, size=5).reshape(-1, 1)
    objC, comp = jornada_completa(por_hora)
    por_hora = np.random.randint(maximoEmpleados, size=7).reshape(-1, 1)
    objR, redc = jornada_reducida(por_hora)
    por_hora = np.random.randint(maximoEmpleados, size=9).reshape(-1, 1)
    objP, parc = jornada_parcial(por_hora)

    # Calculamos la solucion por turnos
    simSolucion = calcular_solucion(comp, redc, parc)

    return [objC, objR, objP], simSolucion

def solucionASimulacion(lista):
    c_hora, r_hora, p_hora = lista

    objC, comp = jornada_completa(c_hora.reshape(-1, 1))
    objR, redc = jornada_reducida(r_hora.reshape(-1, 1))
    objP, parc = jornada_parcial(p_hora.reshape(-1, 1))

    # Calculamos la solucion por turnos
    simSolucion = calcular_solucion(comp, redc, parc)

    return simSolucion

import numpy as np


def sigmoid(x):
    z = 1/(1 + np.exp(-x))
    return z


def funcionObjetivo(list_jornadas, coste_base):

    return (coste_base * list_jornadas[0]).sum()\
            + (0.8 * coste_base * list_jornadas[1]).sum()\
            + (0.6 * coste_base * list_jornadas[2]).sum()


def calidad(maximoObj, minimoObj, obj, area, perc):

    peso = (maximoObj - obj) / (maximoObj - minimoObj)
    return (peso + sigmoid((2 - area) / 2) + sigmoid((perc - 0.9) / 0.9)) / 3



def lossFunction(objetivos, areas, percentiles, instance=None):

    minimoObj = min(objetivos)
    maximoObj = max(objetivos)

    pesos = np.array([(maximoObj - x)/(maximoObj - minimoObj) for x in objetivos])
    facts1 = [a.sum(axis=0) for a in areas]
    facts2 = [p.sum(axis=0) for p in percentiles]
    facts1 = np.array([a[0]/a[1] for a in facts1])
    facts2 = np.array([p[0]/p[1] for p in facts2])

    veros = (pesos + sigmoid((2-facts1)/2) + sigmoid((facts2-0.9)/0.9))/3


    return veros


def calcularMedia(cola):

    lenCola = np.array(cola.longitudCola)
    penalizacion = np.where(lenCola[:, 0] > 21.01, 5*lenCola[:, 0], 0)
    lenCola_penalizada = lenCola[:, 1] + penalizacion
    media = np.trapz(lenCola_penalizada, x=lenCola[:, 0])

    return [media, lenCola[-1, 0]]


def calcularPercentil(cola):
    return [cola.tiemposEspera.count(1), len(cola.tiemposEspera)]
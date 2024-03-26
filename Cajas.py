import numpy as np
from Cajero import Cajero

class Cajas:
    def __init__(self, maximoNumero):
        self._current_index = 0
        self.maximoNumero = maximoNumero
        self.cajeros = {}

        for i in range(maximoNumero):
            self.cajeros[f"cajeroLibre{i}"] = Cajero(caja=i)
            # Tantas instancias como el maximo de cajeros


    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < self.maximoNumero:
            cajero = self.cajeros[self._current_index]
            self._current_index += 1
            return cajero
        raise StopIteration

    def cambiarCajeros(self, cambio):
        if cambio[0] == 1:
            for key in cambio[1]:
                self.cajeros[key].setActivo(True)
        else:
            for key in cambio[1]:
                self.cajeros[key].setActivo(False)

    def algunaOcupada(self):
        algunoOcupado = np.array([cajero.estaOcupado() for cajero in self.cajeros.values()])
        if algunoOcupado.any() == True:
            return True

    def __repr__(self):
        return f'Cajas{vars(self)}'

    def __str__(self):
        return f'Cajas{vars(self)}'
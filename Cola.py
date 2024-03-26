class Cola:
    def __init__(self):
        self.cola = []

        # Variables acumuladoras
        self.tiemposEspera = []
        self.longitudCola = []

    def aumentarCola(self, cliente, reloj):
        self.cola.append((*cliente, reloj.getTiempo()))
        self.longitudCola.append([reloj.getTiempo(), len(self.cola)])

    def actualizar(self, tiempoEspera, instLongitud):
        menos10 = 1
        if tiempoEspera >= 10:
            menos10 = 0

        self.tiemposEspera.append(menos10)
        self.longitudCola.append(instLongitud)

    def pop(self, index):
        return self.cola.pop(index)

    def printCola(self):
        print("Cola actual: ", self.cola)

    def getLen(self):
        return len(self.cola)
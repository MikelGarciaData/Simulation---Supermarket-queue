class Cajero:
    def __init__(self, caja):
        self.idx = caja
        self.ocupado = False
        self.activo = False
        self.cliente = None
        self.cuandoLibre = 100


    def estaActivo(self):
        return self.activo

    def setActivo(self, valor):
        self.activo = valor

    def estaOcupado(self):
        return self.ocupado

    def ocupar(self, cola, reloj):
        self.ocupado = True

        instante = reloj.getTiempo()
        self.cliente = cola.cola.pop(0)
        # anadir tiempo que ha tardado en ser atendido
        #print(instante,  self.cliente[2], instante - self.cliente[2])
        cola.actualizar(instante - self.cliente[2],
                        [instante, cola.getLen()]
                        )

        # print("cliente actual:", self.cliente)

        # Siguiente instante en el que puede atender a un cliente
        self.cuandoLibre = self.cliente[1] + instante

        return self.cliente

    def getCuandoLibre(self):
        return self.cuandoLibre

    def setCuandoLibre(self, cuandoLibre):
        self.cuandoLibre = cuandoLibre

    def updateCuandoLibre(self):
        self.cuandoLibre += self.cliente[1]

    def setCliente(self, cliente):
        self.cliente = cliente

    def getCliente(self, cliente):
        return self.cliente

    def liberar(self):
        self.ocupado = False
        # Siguiente instante en el que puede atender a un cliente
        self.cuandoLibre = 23  # self.cliente[1] + self.cliente[2]
        return self.cliente

    def cerrarCaja(self):
        self.activo = False

    def __str__(self):
        return f'Cajero{self.idx}{self.cliente, self.cuandoLibre, self.ocupado, self.activo}'

    def __repr__(self):
        return f'Cajero{self.idx}{self.cliente, self.cuandoLibre, self.ocupado, self.activo}'
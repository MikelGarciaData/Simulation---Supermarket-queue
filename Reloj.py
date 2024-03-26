class Reloj:
    def __init__(self):
        self.tiempo = 0

    def getTiempo(self):
        return self.tiempo

    def actualizar(self, nuevoTiempo):
        # print("diferencia", nuevoTiempo - self.tiempo)
        if nuevoTiempo > self.tiempo:
            self.tiempo = nuevoTiempo
        elif (nuevoTiempo - self.tiempo) < 0:
            raise Exception("UnorderedTimeException")


    def __str__(self):
        return f'Reloj({self.tiempo})'

    def __repr__(self):
        return f'Reloj({self.tiempo})'
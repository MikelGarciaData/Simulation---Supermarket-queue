import numpy as np

class Calendario:

    def __init__(self, listaEntradas, listaFinCompra, maximoNumero, personalTurno, diferenciaTurno):
        self.entrada = min(listaEntradas, key=lambda e: e[1])
        self.finCompra = min(listaFinCompra, key=lambda f: f[1])
        self.cambioTurno = (diferenciaTurno, 10)

        for i in range(maximoNumero):
            # Tantas variables como el maximo de cajeros
            # 101 la caja esta cerrada, se escogen las de 23
            setattr(self, f"cajeroLibre{i}", (-1, 101))

        # En la solucion miramos en el primer turno [0] la cantidad de cajeros activos
        for i in range(personalTurno):
            # cambiar el codigo para las primeras
            # 100 para evitar invocar el evento cuando no ha estado ocupado
            setattr(self, f"cajeroLibre{i}", (-1, 100))

    def siguienteEvento(self):
        evento = min(vars(self), key=lambda x: vars(self).get(x)[1])
        return (evento, vars(self)[str(evento)])

    def actualizar(self, listaEntradas, listaFinCompra):
        if listaEntradas != []:
            self.entrada = min(listaEntradas, key=lambda e: e[1])
        else:
            self.entrada = (-1, 100)

        if listaFinCompra != []:
            self.finCompra = min(listaFinCompra, key=lambda f: f[1])
        else:
            self.finCompra = (-1, 100)

    def actualizarCajeroLibre(self, cajero):

        # Tiempo que tarda en atender el cliente actual
        if cajero.estaActivo():
            if cajero.estaOcupado():
                setattr(self, f"cajeroLibre{cajero.idx}", (cajero.cliente[0], cajero.getCuandoLibre()))
            else:  # tiempo que tardará en atender al siguiente cliente
                setattr(self, f"cajeroLibre{cajero.idx}", (-1, 100))
        else:
            setattr(self, f"cajeroLibre{cajero.idx}", (-1, 101))

    def cambiarTurno(self, difTurno):
        hora = self.cambioTurno[1]
        self.cambioTurno = (difTurno, hora + 1)

        # Hallar cajas que terminaran su servicio antes
        varsCajero = [x for x in vars(self).keys() if ("cajeroLibre" in x)]
        cajeros = list({k: vars(self)[k] for k in varsCajero}.items())

        if self.cambioTurno[0] > 0:
            # Hallar cajas cerradas
            abrirCajas = sorted(cajeros, key=lambda x: x[1][0])[:difTurno]
            # Obtener nombres de las variables
            abrirCajas = [x[0] for x in abrirCajas]
            # Actualizar su codigo del calendario
            for cajLibre in abrirCajas:
                # Abrir caja
                setattr(self, cajLibre, (-1, 100))

            return (1, abrirCajas)

        elif self.cambioTurno[0] < 0:
            # Hallar cajas abiertas
            cerrarCajas = sorted(cajeros, key=lambda x: x[1][1], reverse=True)[:abs(difTurno)]
            # Obtener nombres de las variables
            cerrarCajas = [x[0] for x in cerrarCajas]
            # Actualizar su codigo del calendario
            for cajLibre in cerrarCajas:
                # Cerrar caja
                setattr(self, cajLibre, (-2, 101))

            return (0, cerrarCajas)

    def finalizarDia(self):
        self.finCompra = (-1, 100)
        self.cambioTurno = (-1, 100)

    def finalizar(self):
        condiciones = [tupla for tupla in vars(self).values()]
        negativa = np.array([tupla[0] for tupla in condiciones])
        magnitud = np.array([tupla[1] for tupla in condiciones])

        if (negativa < 0).all() and (magnitud >= 100).all():
            return True
        else:
            return False

    def __str__(self):
        return f'Calendario{vars(self)}'

    def __repr__(self):
        return f'Calendario{vars(self)}'
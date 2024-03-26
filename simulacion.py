def simulationLoop(rlj, cld, cjrs, cola, eventosEntrada, eventosFinCompra, TiemposPago, difTurnos, verbose=False):
    # inicializar_variables
    flag = True
    while (TiemposPago != []) or cjrs.algunaOcupada():

        tupla = cld.siguienteEvento()

        try:
            rlj.actualizar(tupla[1][1])
        except Exception as e:
            print(e)
            print(rlj)
            print(tupla)
            print(cld)
            break


        if "entrada".__eq__(tupla[0]) and (eventosEntrada != []):
            if verbose:
                print(f"Cliente{tupla[1][0]} entra en supermercado.")
            eventosEntrada.remove(tupla[1])

        elif "finCompra".__eq__(tupla[0]) and (eventosFinCompra != []):
            if verbose:
                print(f"Cliente{tupla[1][0]} ha terminado de comprar.")
            eventosFinCompra.remove(tupla[1])


            clientePago = [tp for tp in TiemposPago if tp[0] == tupla[1][0]][0]

            # Eliminar cliente que va a pagar de tiemposPago
            TiemposPago.remove(clientePago)

            # Aumentar cola en todos los casos, evita condicionales anidadas
            # (id cliente, tiempo para pagar, tiempo incorporacion en cola)
            cola.aumentarCola(clientePago, rlj)

        elif "cajeroLibre" in tupla[0]:

            cjr = cjrs.cajeros[tupla[0]]
            clienteAtendido = cjr.liberar()

            # Actualizar calendario, calculamos el tiempo
            cld.actualizarCajeroLibre(cjr)


            if verbose:
                print(f"Cliente{clienteAtendido[0]} ha sido atendido.")

            del clienteAtendido


        elif "cambioTurno".__eq__(tupla[0]):
            difturno = difTurnos.pop(0)

            cambio = cld.cambiarTurno(difturno)

            if cambio is not None:
                cjrs.cambiarCajeros(cambio)


        for cjr in cjrs.cajeros.values():
            # Si no esta ocupado mirar si hay cola
            if not cjr.estaOcupado() and cjr.estaActivo() and cola.getLen() != 0:
                # Se le pasa cola porque contiene variables acumuladoras
                # ocupar extrae el primer cliente siguiendo una disciplina de cola FIFO
                clienteAtender = cjr.ocupar(cola, rlj)

                if verbose:
                    print(f"Cliente{cjr.cliente[0]} esta siendo atendido.")

                cld.actualizarCajeroLibre(cjr)



        if len(TiemposPago) == 0 and flag:
            cld.finalizarDia()
            flag = False

        cld.actualizar(eventosEntrada, eventosFinCompra)

        if cld.finalizar():
            break


    return cola


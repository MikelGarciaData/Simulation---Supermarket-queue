import matplotlib.pyplot as plt


def scatterPlot(sols, label, fig, ax):
    total = len(sols)
    X = []
    Y = []

    for i in range(total):
        x = sols[i]["obj"]
        y = sols[i]["area"]
        y = y.sum(axis=0)
        y = y[1 ] /y[0]

        X.append(x)
        Y.append(y)
    ax.scatter(X, Y, label = label)
    ax.set_xlabel("Funcion Objetivo")
    ax.set_ylabel("longitud Media Cola")

    return fig, ax


def plot_obj_mean(sols, relink, fig=None, ax=None):
    if fig is None or ax is None:
        fig, ax = plt.subplots(1, 1)

    fig, ax = scatterPlot(sols, "Soluciones Iniciales", fig, ax)

    fig, ax = scatterPlot(relink, "Path Relinking", fig, ax)

    ax.set_title("Mejora observada al utilizar Path Relinking")
    ax.legend()

    return fig, ax
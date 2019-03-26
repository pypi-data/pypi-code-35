"""Funciones para ánalisis del comportamiento a flexión y compresión en HA

    1. fuerza_barra              --> fuerza sobre barra elasto-plástica
    2. beta1                     --> factor beta1 sergún ACI318
    3. factor_reduccion          --> factor de minaoración segun ACI318
    4. puntos_curva_interaccion  --> puntos intermedios curva interacción
    5. compresion_maxima         --> máxima compresión sobre sección
    6. traccion_maxima           --> máxima tracción sobre sección
    7. curva_interaccion_nominal --> curva interacción nominal
    8. curva_interaccion_diseño  --> curva interacción de diseño
    9. fu_directo                --> factor de utilización por método directo
   10. fu_indirecto              --> factor de utilización por método indirecto
   11. factor_utilizacion        --> factor de utilización
"""
import numpy as np
from analisis_geometrico import centro_gravedad, discretiza_poligono
from analisis_geometrico import area_poligono, giro2d


def fuerza_barra(area, Fy, E, es):
    """Fuerza sobre una barra, dada una deformación unitaria.

    Args:
        area (int, float): área de la barra.
        Fy (int, float): tensión de fluencia.
        E (int, float): módulo de élasticidad de la barra.
        es (int, float): deformación unitaria de la barra.

    Returns:
        (int, float): fuerza en la barra.

    """
    assert isinstance(area, (int, float))
    assert isinstance(Fy, (int, float))
    assert isinstance(E, (int, float))
    assert isinstance(es, (int, float))
    assert area >= 0
    assert Fy >= 0
    assert E >= 0

    if np.absolute(es) <= Fy / E:  # Rango élastico
        return E * es * area

    else:  # Rango inelástico
        return Fy * area * np.sign(es)


def beta1(fc):
    """Valor de beta1 según ACI318S-08 pto. 10.2.7.3.

    Args:
        f_c (int, float): Resistencia caracteristica del hormigón en ton/m2.

    Returns:
        (int, float): Beta1
    """
    assert isinstance(fc, (int, float))
    assert fc > 1700, "f'c menor a 17 MPa "

    if fc <= 2800:
        return 0.85
    return max(0.85 - 0.05 / 700 * (fc - 2800), 0.65)


def factor_reduccion(es, fy, E):
    """Factor de reducción según ACI318S-08 pto. 9.3.2.

    Args:
        es (int, float): deformación unitaria.
        fy (int, float): tensión de fluencia.
        E (int, float): módulo de elasticidad.

    Returns:
        (float): factor de reducción fi.
    """
    ey = fy / E

    if es >= 0.005:
        return 0.9

    elif 0.005 > es > ey:
        return 0.25 * (es - 0.005) / (0.005 - ey) + 0.9

    return 0.65


def puntos_curva_interaccion(fc, eu, vertices, barras, puntos=None):
    """Curva interacción nominal para una sección poligonal de HA y
       momento positivo.

    Args:
        fc (float, int): resistencia caracteristica del HA.
        eu (float, int): deformación unitaria máxima del HA.
        vertices (numpy.ndarray): matriz de coordenadas de los vértices del
                                  polígono.
        barras (numpy.ndarray): matriz de nx5 con propiedades de las barras de
                                acero --> [xi, yi, di, Fyi, Ei].
        puntos (int): cantidad de puntos que se desa calcular. 100 puntos por
                      defecto.

    Returns:
        mn (numpy.ndarray): momento nominal.
        pn (numpy.ndarray): esfuerzo axial nominal.
        fi (numpy.ndarray): factor de reducción según ACI318S-08
    """
    ycg = centro_gravedad(vertices)[1]
    ymax = np.max(vertices[:, 1])
    ymin = np.min(vertices[:, 1])

    if puntos is None:
        dy = (ymax - ymin) / 100
    else:
        dy = (ymax - ymin) / puntos

    nbarras = barras.shape[0]
    abarras = barras[:, 2] ** 2 * np.pi / 4
    vertices = discretiza_poligono(vertices)

    eje_neutro = np.arange(ymin, ymax - dy, dy)
    es = np.zeros((len(eje_neutro), nbarras))
    fbarras = np.zeros((len(eje_neutro), nbarras))
    mn, pn = np.zeros(len(eje_neutro)), np.zeros(len(eje_neutro))
    fi = np.zeros(len(eje_neutro))

    for i, y in enumerate(eje_neutro):

        # altura inicial del bloque comprimido según ACI 318S-08 pto. 10.2.7.1
        yy = ymax - beta1(fc) * (ymax - y)
        y_cg_ha = centro_gravedad(vertices[vertices[:, 1] > yy])[1]

        area_acero_comp = np.sum(abarras[barras[:, 1] > yy])
        area_ha_comp =\
            area_poligono(vertices[vertices[:, 1] > yy]) - area_acero_comp

        for j, yb in enumerate(barras[:, 1]):
            # Deformación por ley triangular y secciones planas
            es[i, j] = eu * (yb - y) / (ymax - y)
            fbarras[i, j] =\
                fuerza_barra(abarras[j], barras[j, 3], barras[j, 4], es[i, j])

        mha = area_ha_comp * 0.85 * fc * (y_cg_ha - ycg)
        mas = np.sum(fbarras[i, :] * (barras[:, 1] - ycg))

        mn[i] = mha + mas

        pha = area_ha_comp * 0.85 * fc
        pas = np.sum(fbarras[i, :])

        pn[i] = pha + pas

        # factor de reducción
        fi[i] = factor_reduccion(
            abs(np.min(es[i, :])),  # deformación máxima de tracción
            barras[:, 3][np.argmin(es[i, :])],  # fy de la def máx
            barras[:, 4][np.argmin(es[i, :])])  # Ey de la def máx

    return mn, pn, fi


def compresion_maxima(fc, vertices, barras):
    """Comprasión máxima de una sección de HA según ACI318S-08 pto. 10.3.6.2.

    Args:
        fc (float, int): resistencia caracteristica del HA.
        vertices (numpy.ndarray): matriz de coordenadas de los vértices del
                                  polígono.
        barras (numpy.ndarray): matriz de nx5 con propiedades de las barras de
                                acero --> [xi, yi, di, Fyi, Ei].
    """
    ycg = centro_gravedad(vertices)[1]
    area = area_poligono(vertices)
    abarras = barras[:, 2] ** 2 * np.pi / 4
    area_acero = np.sum(abarras)

    pha = 0.85 * fc * (area - area_acero)
    pas = np.sum(abarras * barras[:, 3])
    pmax = pha + pas

    mmax = np.sum(pas * (barras[:, 1] - ycg))

    return mmax, pmax


def traccion_maxima(vertices, barras):
    """Tracción máxima de una sección de HA.

    Args:
        vertices (numpy.ndarray): matriz de coordenadas de los vértices del
                                  polígono.
        barras (numpy.ndarray): matriz de nx5 con propiedades de las barras de
                                acero --> [xi, yi, di, Fyi, Ei].
    """
    ycg = centro_gravedad(vertices)[1]
    abarras = barras[:, 2] ** 2 * np.pi / 4

    mmin = -np.sum(abarras * barras[:, 3] * (barras[:, 1] - ycg))
    pmin = -np.sum(abarras * barras[:, 3])

    return mmin, pmin


def curva_interaccion_nominal(fc, eu, vertices, barras, puntos=None):
    """Curva de interacción para para momentos positivo y negativo.

       Se calcula la curva para la sección original y rotada en 180°,
       luego se concatena en orden con los pares (M, Pmin) y (M, Pmax).

    Args:
        vertices (numpy.ndarray): matriz de coords. de vértices de la sección.
        barras (numpy.ndarray): matriz de coords. de las barras de acero.
        diametros (numpy.ndarray): vector con los diámetros de cada barra en
                                   metros.
        fy (numpy.ndarray): vector con la tensión de fluencia de cada barra en
                            ton/m2.
        elasticidad (numpy.ndarray): vector con el módulo de élasticidad de
                                     cada barra en ton/m2.
        fc (float, int): resistencia caracteristica del HA a compresión en
                         ton/m2.
        e_u (float, int): deformación del HA en estado último.
        puntos (int): # puntos a calcular en la curva de interacción.
        delta (float, int): distancia en la que se discretiza la sección para
                            integración, en metros.
    """
    # Máximos y mínimos nominales y reducidos
    mmax, pmax = compresion_maxima(fc, vertices, barras)
    mmin, pmin = traccion_maxima(vertices, barras)

    # Curva nominal y reducida para momento positivo
    mn0, pn0, fi0 = puntos_curva_interaccion(fc, eu, vertices, barras, puntos)

    # Giro en 180° de vértices y barras de la sección
    vertices180 = giro2d(vertices, np.pi)
    barras180 = giro2d(barras[:, 0:2], np.pi)
    barras180 = np.append(barras180, barras[:, 2:], axis=1)

    # Curva nominal y reducida para momento negativo
    mn180, pn180, fi180 = puntos_curva_interaccion(
        fc, eu, vertices180, barras180, puntos)

    # Concatenación de las partes de la curva nominal
    mn = np.append(
        np.append(np.append(np.append(mmin, mn0[::-1]), mmax), -mn180), mmin)
    pn = np.append(
        np.append(np.append(np.append(pmin, pn0[::-1]), pmax), pn180), pmin)
    fi = np.append(
        np.append(np.append(np.append(0.9, fi0[::-1]), 0.65), fi180), 0.9)

    return mn, pn, fi


def curva_interaccion_diseño(mn, pn, fi):
    """Retorna la curva de interacción de diseño a partir de la curva nominal.

    Args:
        mn (numpy.ndarray): vector con el momento nominal.
        pn (numpy.ndarray): vector con el esfuerzo axial nominal.
        fi (numpy.ndarray): vector con el factor de reducción.

    Returns:
        fimn (numpy.ndarray) : vector con el momento de diseño.
        fipn (numpy.ndarray) : vector con el esfuerzo axial de diseño.
    """
    fimn = fi * mn
    fipn = fi * pn
    # Esfuerzo axial máximo según ACI318S-08 pto. 10.3.6.2.
    fipn[fipn > 0.8 * fipn.max()] = 0.8 * fipn.max()
    return fimn, fipn


def fu_directo(m, p, s):
    """Calcula factor de utilización por el método directo.

    Args:
        curva (numpy.ndarray): matriz con las coordenadas de la curva de
                               interacción (MxP)
        punto (tupla, numpy.ndarray, list): vector con las coordenadas de la
                                            solicitación
    """
    # Recta que pasa por el origen y el punto en estudio
    pendiente = s[1] / s[0]
    y = [pendiente * i for i in m]

    # Índices de los puntos de la curva que intersectan la recta
    idxs = np.argwhere(np.diff(np.sign(p - y))).flatten()
    for i in idxs:
        pendiente_curva = p[i] / m[i]
        # Condición para que dos puntos estén en el mismo cuadrante
        if pendiente * pendiente_curva > 0 and s[0] * m[i] > 0:
            idx = i
        elif s[1] == 0 and s[0] * m[i] > 0:
            idx = i

    d1 = np.sqrt(s[0]**2 + s[1]**2)
    d2 = np.sqrt(m[idx]**2 + p[idx]**2)
    return d1 / d2


def fu_indirecto(m, p, s):
    """Calcula factor de utilización por el método indirecto.

    Args:
        curva (numpy.ndarray): matriz con las coordenadas de la curva de
                               interacción (MxP)
        punto (tupla, numpy.ndarray, list): vector con las coordenadas de la
                                            solicitación
    """
    dist = [np.sqrt((s[0] - x[0]) ** 2 + (s[1] - x[1]) ** 2)
            for x in np.stack((m, p), axis=-1)]

    # índice del punto más cercano a la curva
    idx = np.argmin(dist)

    d1 = np.sqrt(m[idx]**2 + p[idx]**2)  # distancia a la curva

    alpha = (s[0] * m[idx] + s[1] * p[idx]) / (m[idx] ** 2 + p[idx] ** 2)
    d2 = alpha ** 2 * d1  # distancia del vector proyección del punto en  d1

    fu = d2/d1
    # if barras_en_seccion(curva, [punto]):
    #     assert 0 <= fu <= 1
    # else:
    #     assert fu >= 1

    return fu


def factor_utilizacion(m, p, s, directo=True):
    """Factor de utilización de curva de interacción para una solicitación.

    Args:
        curva (numpy.ndarray): matriz con las coordenadas de la curva de
                               interacción (MxP)
        punto (tupla, numpy.ndarray, list): vector con las coordenadas de la
                                            solicitación
        fu_direc (bool, optional): Defaults to True. forma de calcular el
                                   factor de utlización, True para cuociente
                                   de vectores en la misma pendiente, False
                                   para vector que une el punto más cercano
                                   de la curva a la solicitación
        delta (float, int): valor para discretizar curva, en unidades
                            proporcionales
    """
    mp = discretiza_poligono(np.stack((m, p), axis=-1))
    norma = np.sqrt(mp[:, 0] ** 2 + mp[:, 1] ** 2).max()
    mn = mp[:, 0] / norma
    pn = mp[:, 1] / norma
    sn = s / norma

    if s[0] == 0 and s[1] == 0:
        return 0

    elif directo:
        return fu_directo(mn, pn, sn)

    else:
        return fu_indirecto(mn, pn, sn)


if __name__ == '__main__':
    np.set_printoptions(precision=5, suppress=True)
    import matplotlib.pyplot as plt

    vertices = np.array([[0.0, 0.0],
                         [0.2, 0.0],
                         [0.2, 3.0],
                         [0.0, 3.0],
                         [0.0, 0.0]])

    barras = np.array([[0.03, 0.03, 0.022, 42000, 21000000],
                       [0.17, 0.03, 0.022, 42000, 21000000],
                       [0.17, 2.97, 0.022, 42000, 21000000],
                       [0.03, 2.97, 0.022, 42000, 21000000]])

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    MN, PN, FI = curva_interaccion_nominal(
        2500, 0.003, vertices, barras, puntos=20)
    FIMN, FIPN = curva_interaccion_diseño(MN, PN, FI)

    ax1.plot(MN, PN, label='MN vs PN', linewidth=2)
    ax1.plot(FIMN, FIPN, label='', linewidth=4)

    ax1.scatter(-38, 0)
    ax1.grid()

    ax1.axhline(0)
    ax1.axhline(100)
    ax1.axvline(0)

    plt.grid()

    solicitaciones = np.array([
        [0, 0],
        [200, 200],
        [-200, 200],
        [-51, -24],
        [14, -16],
    ])

    for s in range(1, 1600, 20):
        print('({:10.2f},{:10.2f}){:10.3f}{:10.3f}'.format(
            s,
            100,
            factor_utilizacion(FIMN, FIPN, np.array([s, 100]), directo=True),
            factor_utilizacion(FIMN, FIPN, np.array([s, 100]), directo=False)))

    plt.show()

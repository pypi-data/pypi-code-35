"""Funciones de análisis geometrico.

    1. vertices_rectangulo    --> vértices a partir de ancho x alto
    2. pendiente_recta        --> pendiente de recta a partir de dos puntos
    3. interseccion_rectas    --> intersección entre dos rectas
    4. interseccion_segmentos --> intersección entre dos segmentos
    5. enpoligono             --> si un punto esta dentro de un polígono
    6. centro_gravedad        --> centro de gravedad a partir de vértices
    7. discretiza_segmento    --> discretización de un segmento
    8. discretiza_poligono    --> discretización de un polígono
    9. area_poligono          --> área de un polígono a partir de vértices
   10. giro2d                 --> giro y traslación de coordenadas
"""
import numpy as np


def vertices_rectangulo(ancho, alto, x0=0, y0=0):
    """Calcula los vértices sección rectangular a partir de ancho y alto.

        Las coordenadas se retornan en sentido anti-horario partiendo por el
        origen de coordenadas y terminando en el origen de coordenadas.

    Args:
        ancho (int, float): Ancho de la sección.
        alto (int, float): Alto de la sección.
        x0 (int, float, optional): Defaults to 0. Coordenada X del origen.
        y0 (int, float, optional): Defaults to 0. Coordenada Y del origen.

    Returns:
        numpy.ndarray: Matriz con las 4 coordenadas de los vértices.
    """
    assert isinstance(ancho, (int, float))
    assert isinstance(alto, (int, float))
    assert isinstance(x0, (int, float))
    assert isinstance(y0, (int, float))

    return np.array(
        [
            [x0+0,     y0+0],
            [x0+ancho, y0+0],
            [x0+ancho, y0+alto],
            [x0+0,     y0+alto],
            [x0+0,     y0+0]
        ]
    )


def pendiente_recta(p1, p2):
    """Retorna la pendiente de una recta que pasa por los puntos p1 y p2.

    Args:
        p1 (array like): coordenadas del punto 1.
        p2 (array like): coordenadas del punto 2.

    Returns:
        float: Pendiente de la recta.
    """
    if p2[0] == p1[0]:
        return None
    return (p2[1] - p1[1]) / (p2[0] - p1[0])


def interseccion_rectas(r1, r2):
    """Verifica si existe la intersección entre dos rectas en el plano.

    Args:
        r1 (numpy.ndarray): Matriz de 2x2 con coordenadas en el plano por el
                            que pasa la recta n°1.
        r2 (numpy.ndarray): Matriz de 2x2 con coordenadas en el plano por el
                            que pasa la recta n°2.

    Returns:
        (tuple): tupla con las coordenadas de la intersección. None si no
                 existe intersección.
    """
    assert isinstance(r1, np.ndarray)
    assert isinstance(r2, np.ndarray)
    assert r1.shape == (2, 2)
    assert r2.shape == (2, 2)
    assert not (r1[0] == r1[1]).all(), "Los puntos son iguales"
    assert not (r2[0] == r2[1]).all(), "Los puntos son iguales"

    m1 = pendiente_recta(r1[0], r1[1])
    m2 = pendiente_recta(r2[0], r2[1])

    # Intersección con eje Y:
    if m1 is None:
        n1 = None
    else:
        n1 = r1[0, 1] - m1 * r1[0, 0]

    if m2 is None:
        n2 = None
    else:
        n2 = r2[0, 1] - m2 * r2[0, 0]

    # Si las rectas son paralelas no hay intersección:
    if m1 == m2:
        return None

    # Retorna la intersección:
    if (m1 is None) and (m2 is not None):
        return (r1[0, 0], m2 * r1[0, 0] + n2)

    elif (m1 is not None) and (m2 is None):
        return (r2[0, 0], m1 * r2[0, 0] + n1)

    else:
        return ((n2-n1)/(m1-m2), (m1*(n2-n1))/(m1-m2)+n1)


def interseccion_segmentos(s1, s2):
    """Verifica si existe la intersección entre dos rectas en el plano.

    Args:
        s1 (numpy.ndarray): Matriz de 2x2 con las coordenadas de los puntos
                            que forman el segmento 1.
        s2 (numpy.ndarray): Matriz de 2x2 con las coordenadas de los puntos
                            que forman el segmento 2.

    Returns:
        (tuple): tupla con las coordenadas de la intersección. None si no
                 existe intersección.
    """
    assert isinstance(s1, np.ndarray)
    assert isinstance(s2, np.ndarray)
    assert s1.shape == (2, 2)
    assert s2.shape == (2, 2)
    assert not (s1[0] == s1[1]).all(), "Los puntos son iguales"
    assert not (s2[0] == s2[1]).all(), "Los puntos son iguales"

    p = interseccion_rectas(s1, s2)
    # Si no existe intersección entre las rectas que pasan por los segmentos:
    if p is None:
        return None

    # El punto debe estar dentro del intervalo que conforman los segmentos:
    if (s1[:, 0].min() <= p[0] <= s1[:, 0].max() and
            s2[:, 0].min() <= p[0] <= s2[:, 0].max()):
        return p
    return None


def enpoligono(vertices, punto):
    """Verifica si un punto está dentro de un polígono.

       Utiliza el algoritmo ray casting.

    Args:
        vertices (numpy.ndarray): Matriz de coordenadas de vértices del
                                  polígono.
        punto (array like): vector de 2 elementos con las coordenadas del
                            punto que se desea verificar.

    Returns:
        bool: True si el punto esta dentro del polígono, False en caso
              contrario
    """
    xmin = vertices[:, 0].min()
    xmax = vertices[:, 0].max()
    ymin = vertices[:, 1].min()
    ymax = vertices[:, 1].max()

    # Verifica si el punto esta fuera del rectángulo formado por las
    # coordenadas extremas.
    if ((punto[0] < xmin) or (punto[0] > xmax) or
            (punto[1] < ymin) or (punto[1] > ymax)):
        return False

    p0 = (xmin - (xmax-xmin)/2, (ymax+ymin)/2)
    intersecciones = 0
    for i, _ in enumerate(vertices[:-1]):
        s1 = np.array([vertices[i], vertices[i+1]])
        s2 = np.array([p0, punto])
        if interseccion_segmentos(s1, s2) is not None:
            intersecciones += 1

    # par
    if intersecciones % 2 == 0:
        return False
    # impar
    else:
        return True


def centro_gravedad(vertices):
    """Coordenadas del centro de gravedad de un poligono cualquiera.

    Args:
        vertices (numpy.ndarray): Matriz de coordenadas del polígono.

    Returns:
        tuple: tupla con las coordenadas del centro de gravedad
    """
    # Se eliminan los puntos repetidos.
    unicos = np.unique(vertices, axis=0)
    x = unicos[:, 0]
    y = unicos[:, 1]
    n = x.shape[0]
    return (np.sum(x)/n, np.sum(y)/n)


def discretiza_segmento(segmento, separacion):
    """Discretiza un segmento intervalos de aproximadamente la separación dada.

    Args:
        segmento (numpy.ndarray): matriz de 2x2 con las coordenadas de los
                                  puntos que conforman el segmento.
        separacion (int, float): separación.

    Returns:
        numpy.ndarray: matriz con el segmento discretizado.
    """
    assert isinstance(segmento, np.ndarray)
    assert isinstance(separacion, (float, int))
    dist = np.linalg.norm(segmento[0, :] - segmento[1, :])
    n = dist // separacion + 1
    return np.linspace(segmento[0, :], segmento[1, :], n)


def discretiza_poligono(vertices, separacion=None):
    """Discretiza un polígono.

    Args:
        vertices (numpy.ndarray): matriz de vértices del polígono.
        separacion (int, float) : valor para la separación entre los segmentos
                                  del nuevo polígono. La separación por defecto
                                  corresponde a la centésima parte del lado
                                  menor del rectángulo circunscrito al
                                  polígono.

    Returns:
        numpy.ndarray: matriz con el los vertices del polígono discretizado.
    """
    if separacion is None:
        ancho = vertices[:, 0].max() - vertices[:, 0].min()
        alto = vertices[:, 1].max() - vertices[:, 1].min()
        separacion = min(ancho, alto)/100

    nuevos_vertices = vertices[0:1]
    for i, _ in enumerate(vertices[:-1]):
        nuevo_segmento = discretiza_segmento(vertices[i:i+2], separacion)
        nuevos_vertices = np.concatenate((nuevos_vertices, nuevo_segmento[1:]))
    return nuevos_vertices


def area_poligono(vertices):
    """Área de un polígono a partir de sus vértices.

    Se calcula utilizando la fórmula de área de Gauss. Las coordenadas deben
    estar ordenadas en sentido horario o anti-horario.

    ref: https://es.wikipedia.org/wiki/F%C3%B3rmula_del_%C3%A1rea_de_Gauss

    Args:
        vertices (numpy.ndarray): matriz de coordenadas de los vértices del
                                  polígono.

    Returns:
        (float): área del polígono.
    """
    return 0.5 * np.abs(
        np.dot(vertices[:, 0], np.roll(vertices[:, 1], 1)) -
        np.dot(vertices[:, 1], np.roll(vertices[:, 0], 1)))


def giro2d(puntos, angulo, pivote=np.array([0, 0]), delta=np.array([0, 0])):
    """Traslación y rotación de coordenadas en el plano 2D.

    Args:
        puntos (numpy.ndarray): matriz de coordenadas de los puntos.
        angulo (float, int): ángulo de la rotación.
        pivote (numpy.ndarray, optional): Defaults to np.array([0, 0]).
                                          punto en torno al que se gira.
        delta (numpy.ndarray, optional): Defaults to np.array([0, 0]).
                                         magnitud de la traslación.
    """
    # Matriz de transformación
    mt = np.array([
        [np.cos(angulo), -np.sin(angulo)],
        [np.sin(angulo), np.cos(angulo)]
    ])

    puntos_nuevos = []
    for punto in puntos:
        puntos_nuevos.append(pivote + np.dot(mt, (punto - pivote)) + delta)

    return np.array(puntos_nuevos)


# def barras2capas(barras):
#     """Matriz de coordenadas de barras a matriz de capas de barras.

#     Args:
#         barras (numpy.ndarray): matriz de coordenadas y propiedades
#                                 de las barras.
#     """
#     alturas = set(barras[:, 1])
#     diametros = set(barras[:, 2])
#     fluencias = set(barras[:, 3])
#     elasticidades = set(barras[:, 4])
#     capas = []
#     for y in alturas:
#         for d in diametros:
#             for f in fluencias:
#                 for e in elasticidades:
#                     n = len(
#                         barras[
#                             (barras[:, 1] == y) &
#                             (barras[:, 2] == d) &
#                             (barras[:, 3] == f) &
#                             (barras[:, 4] == e)
#                         ])
#                     if n != 0:
#                         capas.append([n, d, y, f, e])

#     capas = np.array(capas)
#     capas = capas[capas[:, 2].argsort()]
#     return capas


# def capas2barras(capas, ancho, req1=0.03, req2=0.1):
#     """Matriz de capas a matriz de barras.

#     Args:
#         capas (lista de listas): información de la capas.
#         req1 (float): recubrimiento desde el borde de la sección.
#         req2 (float): distancia entre capas de barras.
#     """
#     barras = []
#     for (n, d, y1, y2, s, fy, e) in capas:
#         if n == 1:
#             x = [ancho / 2]
#         else:
#             x = np.arange(req1, ancho, (ancho-2*req1)/(n-1))
#         for coordx in x:
#             if y2 is None:
#                 barras.append([coordx, y1, d, fy, e])
#             else:
#                 y = np.arange(y1, y2+req2, s)
#                 for coordy in y:
#                     barras.append([coordx, coordy, d, fy, e])

#     return np.array(barras)


if __name__ == '__main__':
    pass

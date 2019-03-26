import numpy as np
import matplotlib.pyplot as plt
from analisis_geometrico import vertices_rectangulo, pendiente_recta
from analisis_geometrico import interseccion_rectas, interseccion_segmentos
from analisis_geometrico import enpoligono, centro_gravedad
from analisis_geometrico import discretiza_segmento, discretiza_poligono


if __name__ == '__main__':
    # Vertices de prueba para sección 1x1
    vertices = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    vertices_1_1_o_1_1 = np.array([[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]])
    cuadrado = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])

    # Tests:
    assert np.array_equal(vertices_rectangulo(1, 1), vertices)
    assert np.array_equal(vertices_rectangulo(1, 1, 1, 1), vertices_1_1_o_1_1)

    assert pendiente_recta((0, 0), (1, 1)) == 1
    assert pendiente_recta([0, 0], [1, 1]) == 1
    assert pendiente_recta(np.array([0, 0]), [1, 1]) == 1
    assert pendiente_recta(np.array([0, 0]), np.array([1, 1])) == 1
    assert pendiente_recta((0, 0), (0, 1)) is None

    # Rectas sobre el eje Y
    r1 = np.array([[0, 0], [0, 1]])
    r2 = np.array([[0, 0], [0, 2]])
    assert (interseccion_rectas(r1, r2)) is None

    # Rectas sobre el eje X
    r1 = np.array([[0, 0], [1, 0]])
    r2 = np.array([[0, 0], [-2, 0]])
    assert (interseccion_rectas(r1, r2)) is None

    # Rectas paralelas
    r1 = np.array([[0, 1], [2, 3]])
    r2 = np.array([[0, 2], [2, 4]])
    assert (interseccion_rectas(r1, r2)) is None

    # Una recta paralela a Y
    r1 = np.array([[2, -50], [2, 50]])
    r2 = np.array([[0, 2], [2, 4]])
    assert (interseccion_rectas(r1, r2)) == (2, 4)

    # Dos rectas inclinadas
    r1 = np.array([[0, 1], [2, 3]])
    r2 = np.array([[0, 3], [2, 1]])
    assert (interseccion_rectas(r1, r2)) == (1, 2)

    # Segmentos sobre el eje Y
    s1 = np.array([[0, 0], [0, 1]])
    s2 = np.array([[0, 0], [0, 2]])
    assert (interseccion_segmentos(s1, s2)) is None

    # Segmentos sobre el eje X
    s1 = np.array([[0, 0], [1, 0]])
    s2 = np.array([[0, 0], [-2, 0]])
    assert (interseccion_segmentos(s1, s2)) is None

    # Segmentos paralelas
    s1 = np.array([[0, 1], [2, 3]])
    s2 = np.array([[0, 2], [2, 4]])
    assert (interseccion_segmentos(s1, s2)) is None

    # Un segmento paralela a Y
    s1 = np.array([[2, -50], [2, 50]])
    s2 = np.array([[0, 2], [2, 4]])
    assert (interseccion_segmentos(s1, s2)) == (2, 4)

    # # Dos segmentos inclinadas que se cruzan
    s1 = np.array([[0, 1], [2, 3]])
    s2 = np.array([[0, 3], [2, 1]])
    assert (interseccion_segmentos(s1, s2)) == (1, 2)

    # Dos segmentos inclinadas que no se cruzan
    s1 = np.array([[1, 3], [3, 5]])
    s2 = np.array([[3, 4], [5, 2]])
    assert (interseccion_segmentos(s1, s2)) is None

    # Mismo anterior pero con los segmentos alrrevés
    s2 = np.array([[1, 3], [3, 5]])
    s1 = np.array([[3, 4], [5, 2]])
    assert (interseccion_segmentos(s1, s2)) is None

    # Mismo anterior pero con puntos en otro orden en s1
    s1 = np.array([[3, 5], [1, 3]])
    s2 = np.array([[3, 4], [5, 2]])
    assert (interseccion_segmentos(s1, s2)) is None

    # Mismo anterior pero se alarga s2 para que se crucen
    s1 = np.array([[3, 5], [1, 3]])
    s2 = np.array([[2, 5], [5, 2]])
    assert (interseccion_segmentos(s1, s2)) == (2.5, 4.5)

    vertices = np.array([[1, 1], [5, 3], [4, 6], [2, 6], [1, 1]])
    punto = (3, 3)
    assert enpoligono(vertices, punto) is True
    punto = (4, 3)
    assert enpoligono(vertices, punto) is True
    punto = (2, 2)
    assert enpoligono(vertices, punto) is True
    punto = (1, 1)
    assert enpoligono(vertices, punto) is False
    punto = (-3, 3)
    assert enpoligono(vertices, punto) is False
    punto = (2, 7)
    assert enpoligono(vertices, punto) is False
    punto = (2, -7)
    assert enpoligono(vertices, punto) is False
    punto = (6, 3)
    assert enpoligono(vertices, punto) is False
    punto = (3, 6)
    assert enpoligono(vertices, punto) is False
    punto = (3, 5.99)
    assert enpoligono(vertices, punto) is True
    punto = (3, 6.01)
    assert enpoligono(vertices, punto) is False

    assert centro_gravedad(cuadrado) == (0.5, 0.5)
    assert centro_gravedad(vertices) == (3, 4)

    segmento = np.array([[1, 0], [3, 1]])
    discretiza_segmento(segmento, 0.2)

    vertices = np.array([[-11, 1], [5, 3], [4, 6], [2, 6], [-11, 1]])
    nuevos_vertices = discretiza_poligono(vertices, 0.5)

    plt.scatter(vertices[:, 0], vertices[:, 1])
    plt.scatter(nuevos_vertices[:, 0], nuevos_vertices[:, 1])
    plt.show()

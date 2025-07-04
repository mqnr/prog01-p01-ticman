def nuevo(*parejas):
    """
    Inicializar un nuevo pseudo-mapa con las parejas dadas.

    :param *parejas: una cantidad variable de tuplas, donde cada tupla
        representa una pareja clave-valor
    :returns: una lista de tuplas que representa el pseudo-mapa
    """
    return [*parejas]


def obtener(mapa, clave):
    """
    Obtener el valor asociado con una clave en el pseudo-mapa.

    :param mapa: el pseudo-mapa donde buscar
    :param clave: la clave cuyo valor asociado se desea obtener
    :returns: el valor asociado con la clave dada, o None si la clave
        no se encuentra en el mapa
    """
    for pareja in mapa:
        if pareja[0] == clave:
            return pareja[1]
    return None


def actualizar(mapa, pareja):
    """
    Actualizar una pareja clave-valor en el pseudo-mapa. Si la clave
    no existe, añadir la pareja.

    :param mapa: el pseudo-mapa a actualizar
    :param pareja: la pareja clave-valor a actualizar o añadir
    """
    encontrado = False
    for i, m_pareja in enumerate(mapa):
        if m_pareja[0] == pareja[0]:
            encontrado = True
            mapa[i] = pareja
            break
    if not encontrado:
        mapa.append(pareja)


def remover(mapa, clave):
    """
    Remover una pareja clave-valor del pseudo-mapa basado en la clave proporcionada.

    :param mapa: el pseudo-mapa del cual remover la pareja
    :param clave: la clave de la pareja a remover
    :returns: True si la pareja fue removida, False si la clave no se
        encontró en el mapa
    """
    for pareja in mapa:
        if pareja[0] == clave:
            mapa.remove(pareja)
            return True
    return False

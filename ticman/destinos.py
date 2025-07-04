# constantes representando códigos de destinos
TIC = "TIC"  # código para "Sin destino"
LUN = "LUN"  # código para "Luna"
EUR = "EUR"  # código para "Europa"
TAN = "TAN"  # código para "Titán"


def codigo_a_largo(codigo):
    """
    Convertir un código de destino en su nombre largo correspondiente.

    :param codigo: el código del destino
    :returns: el nombre largo del destino, o una cadena vacía si ninguno coincide
    """
    if codigo == TIC:
        return "Sin destino"
    if codigo == LUN:
        return "Luna"
    if codigo == EUR:
        return "Europa"
    if codigo == TAN:
        return "Titán"
    return ""


def largo_a_codigo(largo):
    """
    Convertir el nombre largo de un destino en su código correspondiente.

    :param largo: el nombre largo del destino
    :returns: el código del destino, o una cadena vacía si ninguno coincide
    """
    if largo == "Sin destino":
        return TIC
    if largo == "Luna":
        return LUN
    if largo == "Europa":
        return EUR
    if largo == "Titán":
        return TAN
    return ""

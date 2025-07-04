import ticman.color as color
import ticman.mapa as mapa
import ticman.destinos as destinos
from ticman.util import tic_imprimir

OCUPADO = "ocupado"
DESOCUPADO = "desocupado"

EJECUTIVO = "Ejecutiva"
ECONOMICO = "Económica"

TARIFAS = mapa.nuevo(
    (
        EJECUTIVO,
        mapa.nuevo(
            (destinos.LUN, 3_000.00),
            (destinos.EUR, 5_250.00),
            (destinos.TAN, 10_500.00),
        ),
    ),
    (
        ECONOMICO,
        mapa.nuevo(
            (destinos.LUN, 2_000.00), (destinos.EUR, 3_500.00), (destinos.TAN, 7_000.00)
        ),
    ),
)

VENTANA = "Ventana"
CENTRO = "Centro"
PASILLO = "Pasillo"


def asiento_vacio(n):
    """
    Asignar un asiento vacío basándose en el número de asiento proporcionado.
    Determinar la clase del asiento (Ejecutivo o Económico) y su ubicación
    (Ventana, Pasillo, Centro) basándose en el número de asiento. El estado del
    asiento se establece como 'desocupado', y se asignan valores predeterminados
    para el destino y el costo.

    :param n: el número de asiento
    :returns: un pseudo-mapa con los detalles del asiento, incluyendo número,
        ubicación, clase, estado, código y destino largo, costo, y pasajero
    """
    ubicacion = ""
    if n in range(1, 5):
        clase = EJECUTIVO
        m = n % 4
        if m in (1, 0):
            ubicacion = VENTANA
        else:
            ubicacion = PASILLO
    else:
        clase = ECONOMICO
        m = (n - 4) % 6
        if m in (1, 0):
            ubicacion = VENTANA
        elif m in (2, 5):
            ubicacion = CENTRO
        else:
            ubicacion = PASILLO

    return mapa.nuevo(
        ("numero", n),
        ("ubicacion", ubicacion),
        ("clase", clase),
        ("estado", "desocupado"),
        ("destino_codigo", destinos.TIC),
        ("destino_largo", destinos.codigo_a_largo(destinos.TIC)),
        ("costo", -1),
        ("pasajero", None),
    )


def asiento_esta_ocupado(asiento):
    """
    Verificar si un asiento está ocupado.

    :param asiento: el asiento
    :returns: True si el asiento está ocupado, de lo contrario False
    """
    return mapa.obtener(asiento, "estado") == OCUPADO


def asiento_numero(asiento):
    """Devuelve el número de un asiento."""
    return mapa.obtener(asiento, "numero")


def calcular_tarifa(clase, destino):
    """
    Calcular la tarifa para un viaje en función de la clase y el destino.
    Utilizar un pseudo-mapa de tarifas predefinido para determinar el costo del
    viaje basado en la clase del asiento y el destino.

    :param clase: la clase del asiento (Ejecutiva o Económica)
    :param destino: el código del destino
    :returns: la tarifa calculada para el viaje
    """
    costos = mapa.obtener(TARIFAS, clase)
    return mapa.obtener(costos, destino)


def asiento_actualizar(asiento, estado=None, destino_codigo=None, pasajero=object()):
    """
    Actualizar los detalles de un asiento. Modificar el estado, destino y
    pasajero del asiento según los parámetros proporcionados. También recalcular
    el costo si el destino cambia.

    :param asiento: el asiento a actualizar
    :param estado: el nuevo estado del asiento (ocupado o desocupado), opcional
    :param destino_codigo: el nuevo código de destino, opcional
    :param pasajero: el nuevo pasajero, opcional
    """
    _sin_valor = object()

    destino_cambiado = False
    if estado in (OCUPADO, DESOCUPADO):
        mapa.actualizar(asiento, ("estado", estado))
    if destino_codigo in (destinos.TIC, destinos.LUN, destinos.EUR, destinos.TAN):
        destino_cambiado = True
        mapa.actualizar(asiento, ("destino_codigo", destino_codigo))
        mapa.actualizar(
            asiento, ("destino_largo", destinos.codigo_a_largo(destino_codigo))
        )
    if pasajero is not _sin_valor:
        mapa.actualizar(asiento, ("pasajero", pasajero))

    if destino_cambiado:
        if destino_codigo == destinos.TIC:
            mapa.actualizar(asiento, ("costo", -1))
            return

        clase = mapa.obtener(asiento, "clase")
        mapa.actualizar(asiento, ("costo", calcular_tarifa(clase, destino_codigo)))


def asiento_desocupar(asiento):
    """
    Desocupar un asiento y restablecer su estado a valores predeterminados.

    :param asiento: el asiento a desocupar
    """
    asiento_actualizar(
        asiento, estado=DESOCUPADO, destino_codigo=destinos.TIC, pasajero=None
    )


def imprimir_pasajero_por_datos(
    asiento, nombre_pasajero, identificacion_pasajero, destino_codigo
):
    print(
        f"• {color.NEGRITAS}{color.NEGRITAS}Nombre del pasajero{color.FIN}: {nombre_pasajero}"
    )
    print(
        f"• {color.NEGRITAS}Identificación del pasajero{color.FIN}: {identificacion_pasajero}"
    )
    print(
        f"• {color.NEGRITAS}Destino del pasajero{color.FIN}: {destinos.codigo_a_largo(destino_codigo)}"
    )
    print(
        f"• {color.NEGRITAS}Clase del asiento{color.FIN}: {mapa.obtener(asiento, 'clase')}"
    )
    print(
        f"• {color.NEGRITAS}Ubicación del asiento{color.FIN}: {mapa.obtener(asiento, 'ubicacion')}"
    )
    print(
        f"• {color.NEGRITAS}Número del asiento{color.FIN}: {mapa.obtener(asiento, 'numero')}"
    )
    costo = calcular_tarifa(mapa.obtener(asiento, "clase"), destino_codigo)
    print(f"• {color.NEGRITAS}Costo del boleto del pasajero{color.FIN}: ${costo:,.2f}")


def imprimir_pasajero_por_asiento(asiento):
    pasajero = mapa.obtener(asiento, "pasajero")

    def op(s):
        return mapa.obtener(pasajero, s)

    def oa(s):
        return mapa.obtener(asiento, s)

    print(f"• {color.NEGRITAS}Nombre del pasajero{color.FIN}: {op('nombre')}")
    print(f"• {color.NEGRITAS}Identificación del pasajero{color.FIN}: {op('id')}")
    print(f"• {color.NEGRITAS}Destino del pasajero{color.FIN}: {oa('destino_largo')}")
    print(f"• {color.NEGRITAS}Clase del asiento{color.FIN}: {oa('clase')}")
    print(f"• {color.NEGRITAS}Ubicación del asiento{color.FIN}: {oa('ubicacion')}")
    print(f"• {color.NEGRITAS}Número del asiento{color.FIN}: {oa('numero')}")
    print(
        f"• {color.NEGRITAS}Costo del boleto del pasajero{color.FIN}: ${oa('costo'):,.2f}"
    )


def imprimir_asientos(asientos):
    def f(asiento):
        destino = mapa.obtener(asiento, "destino_codigo")
        destino = (
            f"{color.OKCIAN}{destino}{color.FIN}"
            if destino != destinos.TIC
            else f"{color.GRIS}{destino}{color.FIN}"
        )
        return (
            f" {color.NEGRITAS}{str(mapa.obtener(asiento, 'numero')).rjust(2)}{color.FIN}"
            f" {destino} "
        )

    def o(n):
        return mapa.obtener(asientos, n)

    def fo(n):
        return f(o(n))

    tic_imprimir("[9]┌────────┬────────┐[3]┌────────┬────────┐")
    tic_imprimir(f"[9]│{fo(1)}│{fo(2)}│[3]│{fo(3)}│{fo(4)}│")
    tic_imprimir("[9]└────────┴────────┘[3]└────────┴────────┘")
    tic_imprimir("┌────────┬────────┬────────┐[3]┌────────┬────────┬────────┐")
    tic_imprimir(f"│{fo(5)}│{fo(6)}│{fo(7)}│[3]│{fo(8)}│{fo(9)}│{fo(10)}│")
    tic_imprimir("├────────┼────────┼────────┤[3]├────────┼────────┼────────┤")
    tic_imprimir(f"│{fo(11)}│{fo(12)}│{fo(13)}│[3]│{fo(14)}│{fo(15)}│{fo(16)}│")
    tic_imprimir("├────────┼────────┼────────┤[3]├────────┼────────┼────────┤")
    tic_imprimir(f"│{fo(17)}│{fo(18)}│{fo(19)}│[3]│{fo(20)}│{fo(21)}│{fo(22)}│")
    tic_imprimir("├────────┼────────┼────────┤[3]├────────┼────────┼────────┤")
    tic_imprimir(f"│{fo(23)}│{fo(24)}│{fo(25)}│[3]│{fo(26)}│{fo(27)}│{fo(28)}│")
    tic_imprimir("└────────┴────────┴────────┘[3]└────────┴────────┴────────┘")


def imprimir_asientos_con_encabezado(asientos):
    print("Mapa de Ocupación:")
    imprimir_asientos(asientos)


def imprimir_asientos_lista(asientos):
    nombre_predeterminado = "*** Disponible ***"
    max_nombre = nombre_predeterminado

    max_identificacion = "Identificación"

    max_destino = "Destino"

    lgt_ubicacion = 11  # longitud de la cadena "del Asiento"

    lgt_clase = 9  # longitud de la cadena "Clase del"

    max_costo = "del Boleto"

    for _, asiento in asientos:
        pasajero = mapa.obtener(asiento, "pasajero")
        if pasajero is None:
            continue

        nombre = mapa.obtener(pasajero, "nombre")
        if nombre is not None:
            if len(nombre) > len(max_nombre):
                max_nombre = nombre

        identificacion = mapa.obtener(pasajero, "id")
        if identificacion is not None:
            if len(identificacion) > len(max_identificacion):
                max_identificacion = identificacion

        destino = mapa.obtener(asiento, "destino_largo")
        if destino is not None:
            if len(destino) > len(max_destino):
                max_destino = destino

        costo = mapa.obtener(asiento, "costo")
        if costo is not None and costo != -1:
            costo_cad = f"{costo:,.2f}"
            if len(costo_cad) > len(max_costo):
                max_costo = costo_cad

    nodel = len("No. del")
    lgt_mn = len(max_nombre)
    lgt_mi = len(max_identificacion)
    lgt_d = len(max_destino)
    lgt_c = len(max_costo)
    encabezado = f"{color.NEGRITAS}{'No. del':^{nodel}} {'':^{lgt_mn}} {'':^{lgt_mi}} {'':^{lgt_d}} {'Clase del':^{lgt_clase}} {'Ubicación':^{lgt_ubicacion}} {'Costo':^{lgt_c}}{color.FIN}"
    lgt_encabezado = len(encabezado)

    print(
        f"{color.NEGRITAS}{color.OKCIAN}{'Transportes Intergalácticos de Cajeme, S.A.':^{lgt_encabezado}}{color.FIN}\n"
    )
    print(
        f"{color.NEGRITAS}{color.OKCIAN}{'Reporte de Reservaciones':^{lgt_encabezado}}{color.FIN}"
    )
    print("─" * len(encabezado))
    print(encabezado)
    print(
        f"{color.NEGRITAS}{'Asiento':^{nodel}} {'Nombre':^{lgt_mn}} {'Identificación':^{lgt_mi}} {'Destino':^{lgt_d}} {'Asiento':^{lgt_clase}} {'del Asiento':^{lgt_ubicacion}} {'del Boleto':^{lgt_c}}{color.FIN}"
    )
    print("─" * len(encabezado))
    for n, asiento in asientos:
        pasajero = mapa.obtener(asiento, "pasajero")

        def op(s):
            if pasajero is None:
                if s == "nombre":
                    return nombre_predeterminado
                return ""

            dev = mapa.obtener(pasajero, s)
            if dev is None:
                return ""
            return dev

        def oa(s):
            return mapa.obtener(asiento, s)

        def i(s):
            print(s, end=" ")

        i(f"{color.NEGRITAS}{n:^{nodel}}{color.FIN}")
        nombre = op("nombre")
        if nombre == nombre_predeterminado:
            i(f"{color.GRIS}{nombre:<{lgt_mn}}{color.FIN}")
        else:
            i(f"{op('nombre'):<{lgt_mn}}")
        i(f"{op('id'):<{lgt_mi}}")
        destino = oa("destino_largo")
        d = destino if oa("destino_codigo") != destinos.TIC else ""
        i(f"{d:^{lgt_d}}")
        i(f"{oa('clase'):^{lgt_clase}}")
        i(f"{oa('ubicacion'):^{lgt_ubicacion}}")
        costo = mapa.obtener(asiento, "costo")
        cc = f"{costo:,.2f}" if costo is not None and costo != -1 else ""
        i(f"{cc:>{lgt_c}}")

        print()

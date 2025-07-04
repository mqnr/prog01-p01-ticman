import ticman.color as color
import ticman.destinos as destinos
import ticman.mapa as mapa
from ticman.asientos import (
    OCUPADO,
    asiento_actualizar,
    asiento_desocupar,
    asiento_esta_ocupado,
    imprimir_asientos,
    imprimir_asientos_con_encabezado,
    imprimir_asientos_lista,
    imprimir_pasajero_por_asiento,
    imprimir_pasajero_por_datos,
)
from ticman.util import (
    entrada_ciclo,
    es_alfabetico,
    esperar_continuar,
    imprimir_encabezado,
    imprimir_error_esperar,
    imprimir_esperar,
    limpiar_pantalla,
    pedir_asiento,
    pedir_respuesta,
    tic_entrada,
    tic_entrada_ciclo,
    tic_entrada_numero_ciclo_inmediato,
)


def comando_registro_de_reservaciones(asientos):
    limpiar_pantalla()
    imprimir_encabezado("Registro de Reservaciones")
    imprimir_asientos_con_encabezado(asientos)

    elegido = pedir_asiento(
        f"Elige el asiento a reservar ({color.CABECERA}0{color.FIN} para volver al menú principal): "
    )

    if elegido == 0:
        return

    asiento = mapa.obtener(asientos, elegido)

    if asiento_esta_ocupado(asiento):
        imprimir_error_esperar("Número del asiento está ocupado.")

        if pedir_respuesta(
            f"¿Se desea continuar con el Registro de Reservaciones, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
        ):
            return comando_registro_de_reservaciones(asientos)
        return

    def es_fin(s):
        return s.lower() == "fin"

    # hay que usar entrada_ciclo en vez de una función más abstraída
    # (como tic_entrada_ciclo) para poder imprimir diferentes mensajes
    # dependiendo de cuál fue la condición que se violó
    nombre = entrada_ciclo(
        funcion_entrada=lambda: tic_entrada(
            "Ingresar el nombre de la persona para esta reservación: ", inmediato=False
        ),
        validador=lambda s: es_alfabetico(s) and not es_fin(s),
        en_invalido=lambda s: imprimir_error_esperar(
            'El pasajero no se puede llamar "fin".'
            if es_fin(s)
            else "Nombre del pasajero inválido."
        ),
        en_error=lambda _: imprimir_error_esperar("Nombre del pasajero inválido."),
    )

    identificacion = tic_entrada(
        "Ingresa la identificación del pasajero: ", inmediato=False
    )

    print("Posibles destinos:")
    print(f"({color.CABECERA}1{color.FIN}) Luna ({color.NEGRITAS}LUN{color.FIN})")
    print(f"({color.CABECERA}2{color.FIN}) Europa ({color.NEGRITAS}EUR{color.FIN})")
    print(f"({color.CABECERA}3{color.FIN}) Titán ({color.NEGRITAS}TAN{color.FIN})")

    opcion = tic_entrada_numero_ciclo_inmediato(
        entrada_texto="--- Presiona uno de los números entre paréntesis --- ",
        validador=lambda x: x in range(1, 4),
        en_invalido="Destino del pasajero inválido.",
    )

    if opcion == 1:
        destino = destinos.LUN
    elif opcion == 2:
        destino = destinos.EUR
    else:
        destino = destinos.TAN

    imprimir_pasajero_por_datos(
        asiento,
        nombre_pasajero=nombre,
        identificacion_pasajero=identificacion,
        destino_codigo=destino,
    )

    if pedir_respuesta(
        f"¿Se confirma el registro de la reservación, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
    ):
        asiento_actualizar(
            asiento,
            estado=OCUPADO,
            destino_codigo=destino,
            pasajero=mapa.nuevo(("nombre", nombre), ("id", identificacion)),
        )

    if pedir_respuesta(
        f"¿Se desea continuar con el Registro de Reservaciones, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
    ):
        return comando_registro_de_reservaciones(asientos)


def comando_eliminacion_de_reservaciones(asientos):
    limpiar_pantalla()
    imprimir_encabezado("Eliminación de Reservaciones")
    imprimir_asientos(asientos)

    elegido = pedir_asiento(
        f"Elige el asiento para el cual eliminar la reservación ({color.CABECERA}0{color.FIN} para regresar al menú principal): "
    )
    if elegido == 0:
        return

    asiento = mapa.obtener(asientos, elegido)
    if not asiento_esta_ocupado(asiento):
        imprimir_esperar("Número del asiento no está ocupado.")

        if pedir_respuesta(
            f"¿Se desea continuar con la Eliminación de Reservaciones, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
        ):
            return comando_eliminacion_de_reservaciones(asientos)
        return

    imprimir_pasajero_por_asiento(asiento)

    if pedir_respuesta(
        f"¿Se confirma la eliminación de la reservación, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
    ):
        asiento_desocupar(asiento)

    if pedir_respuesta(
        f"¿Se desea continuar con la Eliminación de Reservaciones, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
    ):
        return comando_eliminacion_de_reservaciones(asientos)


def comando_modificacion_de_reservaciones(asientos):
    limpiar_pantalla()
    imprimir_encabezado("Modificación de Reservaciones")
    imprimir_asientos(asientos)

    elegido = pedir_asiento(
        f"Elige el asiento a modificar ({color.CABECERA}0{color.FIN} para volver al menú principal): "
    )
    if elegido == 0:
        return

    asiento = mapa.obtener(asientos, elegido)
    if not asiento_esta_ocupado(asiento):
        imprimir_error_esperar("Número del asiento no está ocupado.")

        if pedir_respuesta(
            f"¿Se desea continuar con la Modificación de Reservaciones, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
        ):
            return comando_modificacion_de_reservaciones(asientos)
        return

    imprimir_pasajero_por_asiento(asiento)

    if not pedir_respuesta(
        f"¿Se confirma el ingreso de los datos a modificar, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
    ):
        if pedir_respuesta(
            f"¿Se desea continuar con la Modificación de Reservaciones, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
        ):
            return comando_modificacion_de_reservaciones(asientos)
        return

    nombre = tic_entrada_ciclo(
        entrada_texto="Ingresar el nombre de la persona para esta reservación: ",
        validador=es_alfabetico,
        en_invalido="Nombre del pasajero inválido.",
    )

    identificacion = tic_entrada(
        "Ingresa la identificación del pasajero: ", inmediato=False
    )

    print("Posibles destinos:")
    print(f"({color.CABECERA}1{color.FIN}) Luna ({color.NEGRITAS}LUN{color.FIN})")
    print(f"({color.CABECERA}2{color.FIN}) Europa ({color.NEGRITAS}EUR{color.FIN})")
    print(f"({color.CABECERA}3{color.FIN}) Titán ({color.NEGRITAS}TAN{color.FIN})")

    opcion = tic_entrada_numero_ciclo_inmediato(
        entrada_texto="--- Presiona uno de los números entre paréntesis --- ",
        validador=lambda x: x in range(1, 4),
        en_invalido="Destino del pasajero inválido.",
    )

    if opcion == 1:
        destino = destinos.LUN
    elif opcion == 2:
        destino = destinos.EUR
    else:
        destino = destinos.TAN

    imprimir_pasajero_por_datos(
        asiento,
        nombre_pasajero=nombre,
        identificacion_pasajero=identificacion,
        destino_codigo=destino,
    )

    if pedir_respuesta(
        f"¿Se confirma la modificación de la reservación, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
    ):
        asiento_actualizar(
            asiento,
            estado=OCUPADO,
            destino_codigo=destino,
            pasajero=mapa.nuevo(("nombre", nombre), ("id", identificacion)),
        )

    if pedir_respuesta(
        f"¿Se desea continuar con la Modificación de Reservaciones, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
    ):
        return comando_modificacion_de_reservaciones(asientos)


def comando_submenu_consulta_de_reservaciones(asientos):
    limpiar_pantalla()
    imprimir_encabezado("Submenú Consulta de Reservaciones")

    print("(1) Consulta de Reservaciones por Nombre del Pasajero")
    print("(2) Consulta de Reservaciones por Número del Asiento")
    print("(3) Regresar al Menú Principal")

    opcion = tic_entrada_numero_ciclo_inmediato(
        entrada_texto="--- Presiona uno de los números entre paréntesis --- ",
        validador=lambda x: x in range(1, 4),
        en_invalido="Opción inválida.",
    )

    if opcion == 1:
        return subcomando_submenu_consulta_de_reservaciones_pasajero(asientos)
    elif opcion == 2:
        return subcomando_submenu_consulta_de_reservaciones_asiento(asientos)


def subcomando_submenu_consulta_de_reservaciones_pasajero(asientos):
    limpiar_pantalla()
    imprimir_encabezado("Consulta de Reservaciones por Número del Asiento")

    nombre = tic_entrada_ciclo(
        entrada_texto=(
            'Ingresar el nombre de la persona para esta reservación ("fin" para regresar al menú anterior): '
        ),
        validador=es_alfabetico,
        en_invalido="Nombre del pasajero inválido.",
    ).lower()

    if nombre == "fin":
        return comando_submenu_consulta_de_reservaciones(asientos)

    encontrado = None
    for _, asiento in asientos:
        pasajero = mapa.obtener(asiento, "pasajero")
        if pasajero is None:
            continue

        pnombre = mapa.obtener(pasajero, "nombre")
        # si nuestras invariantes son correctas, pnombre nunca debería
        # ser None, pero incluir este chequeo hace feliz a los
        # comprobadores de tipos
        if pnombre is None:
            continue
        pnombre = pnombre.lower()

        if pnombre == nombre:
            encontrado = asiento
            break

    if not encontrado:
        imprimir_error_esperar("Pasajero no registrado.")

        if pedir_respuesta(
            f"¿Se desea continuar con la Consulta de Reservaciones por Nombre del Pasajero, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
        ):
            return subcomando_submenu_consulta_de_reservaciones_pasajero(asientos)
        return comando_submenu_consulta_de_reservaciones(asientos)

    imprimir_pasajero_por_asiento(encontrado)

    if pedir_respuesta(
        f"¿Se desea continuar con la Consulta de Reservaciones por Nombre del Pasajero, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
    ):
        return subcomando_submenu_consulta_de_reservaciones_pasajero(asientos)
    return comando_submenu_consulta_de_reservaciones(asientos)


def subcomando_submenu_consulta_de_reservaciones_asiento(asientos):
    limpiar_pantalla()
    imprimir_encabezado("Consulta de Reservaciones por Número del Asiento")
    imprimir_asientos(asientos)

    elegido = pedir_asiento(
        f"Elige el asiento a consultar ({color.CABECERA}0{color.FIN} para volver al menú principal): "
    )
    if elegido == 0:
        return comando_submenu_consulta_de_reservaciones(asientos)

    asiento = mapa.obtener(asientos, elegido)

    if not asiento_esta_ocupado(asiento):
        imprimir_error_esperar("Número del asiento no está ocupado.")

        if pedir_respuesta(
            f"¿Se desea continuar con la Consulta de Reservaciones por Número del Asiento, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
        ):
            return subcomando_submenu_consulta_de_reservaciones_asiento(asientos)
        return comando_submenu_consulta_de_reservaciones(asientos)

    imprimir_pasajero_por_asiento(asiento)

    if pedir_respuesta(
        f"¿Se desea continuar con la Consulta de Reservaciones por Número del Asiento, ({color.CABECERA}S{color.FIN}/{color.CABECERA}N{color.FIN})? "
    ):
        return subcomando_submenu_consulta_de_reservaciones_asiento(asientos)
    return comando_submenu_consulta_de_reservaciones(asientos)


def comando_mapa_de_ocupacion(asientos):
    limpiar_pantalla()
    imprimir_encabezado("Mapa de Ocupación")
    imprimir_asientos(asientos)
    esperar_continuar()


def comando_reporte_de_reservaciones(asientos):
    limpiar_pantalla()
    imprimir_encabezado("Reporte de Reservaciones")
    imprimir_asientos_lista(asientos)
    print()

    ocupados = 0
    for _, asiento in asientos:
        if asiento_esta_ocupado(asiento):
            ocupados += 1

    desocupados = 28 - ocupados
    print(f"Total de asientos ocupados: {color.NEGRITAS}{ocupados:>5}{color.FIN}")
    print(f"Total de asientos desocupados: {color.NEGRITAS}{desocupados:>2}{color.FIN}")
    esperar_continuar()

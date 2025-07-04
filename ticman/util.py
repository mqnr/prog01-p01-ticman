import ticman.color as color
import re
import os
import sys
import platform


PLANTILLA = re.compile(r"\[(\d+)\]")


def parsear_plantilla(s: str) -> str:
    def reemplazar(instancia):
        num_spaces = int(instancia.group(1))
        return " " * num_spaces

    return PLANTILLA.sub(reemplazar, s)


def tic_imprimir(plantilla, **kwargs):
    print(parsear_plantilla(plantilla), **kwargs)


def tic_entrada(s=None, inmediato=True, imprimir=False):
    if s is not None:
        print(s, end="", flush=True)
    if not inmediato:
        return input()

    if os.name == "nt":  # para Windows
        import msvcrt

        car = msvcrt.getch().decode()
    else:  # para sistemas Unix-like
        import termios
        import tty
        from select import select

        fd = sys.stdin.fileno()
        atributos_viejos = termios.tcgetattr(fd)
        car = None
        try:
            tty.setraw(sys.stdin.fileno())
            i, _, _ = select([sys.stdin.fileno()], [], [], None)
            if i:
                car = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, atributos_viejos)

    if imprimir:
        print(car)
        return car
    print()
    return car


def entrada_ciclo(
    funcion_entrada=input,
    validador=lambda _: True,
    transformador=lambda x: x,
    en_invalido=lambda _: None,
    excepcion_manejo=Exception,
    en_error=lambda _: None,
):
    """
    Un bucle generalizado para la validación de entradas de usuario.

    Parámetros:
    funcion_entrada (function): Una función para obtener la entrada del usuario.
    validador (function): Una función para validar la entrada. Debe
        devolver True si la entrada es válida.
    transformador (function): Una función para transformar la entrada
        antes de la validación.
    en_invalido (function): Una función para ejecutar cuando la
        entrada no es válida, recibe la entrada transformada.
    excepcion_manejo (Exception): Una excepción a manejar.
    en_error (function): Una función a ejecutar cuando se captura una
        excepción, recibe el objeto de excepción.

    Devuelve:
    La entrada de usuario validada y posiblemente transformada.
    """
    while True:
        try:
            recibido = funcion_entrada()
            recibido = transformador(recibido)
            if validador(recibido):
                return recibido
            else:
                en_invalido(recibido)
        except Exception as e:
            if (
                isinstance(e, KeyboardInterrupt)
                and excepcion_manejo is not KeyboardInterrupt
            ):
                raise

            if isinstance(e, excepcion_manejo):
                en_error(e)


def entrada_numero_ciclo(
    funcion_entrada=input,
    validador=lambda _: True,
    transformador=int,
    en_invalido=lambda _: None,
    excepcion_manejo=ValueError,
    en_error=lambda _: None,
):
    return entrada_ciclo(
        funcion_entrada=funcion_entrada,
        validador=validador,
        transformador=transformador,
        en_invalido=en_invalido,
        excepcion_manejo=excepcion_manejo,
        en_error=en_error,
    )


def iee_ciclo(mensaje):
    def f(_):
        imprimir_error_esperar(mensaje)

    return f


def ticeni_ciclo(mensaje):
    def f():
        return tic_entrada(mensaje, inmediato=False)

    return f


def tic_entrada_ciclo(
    entrada_texto="Ingresar un valor.",
    validador=lambda _: True,
    transformador=lambda x: x,
    en_invalido="Valor inválido.",
    excepcion_manejo=Exception,
    en_error=None,
):
    if en_error is None:
        en_error = en_invalido

    return entrada_ciclo(
        funcion_entrada=ticeni_ciclo(entrada_texto),
        validador=validador,
        transformador=transformador,
        en_invalido=iee_ciclo(en_invalido),
        excepcion_manejo=excepcion_manejo,
        en_error=iee_ciclo(en_error),
    )


def tic_entrada_numero_ciclo_inmediato(
    entrada_texto="Ingresar un número.",
    validador=lambda _: True,
    transformador=int,
    en_invalido="Número inválido.",
    excepcion_manejo=ValueError,
    en_error=None,
):
    if en_error is None:
        en_error = en_invalido

    return entrada_ciclo(
        funcion_entrada=lambda: tic_entrada(entrada_texto),
        validador=validador,
        transformador=transformador,
        en_invalido=iee_ciclo(en_invalido),
        excepcion_manejo=excepcion_manejo,
        en_error=iee_ciclo(en_error),
    )


def tic_entrada_numero_ciclo(
    entrada_texto="Ingresar un número.",
    validador=lambda _: True,
    transformador=int,
    en_invalido="Número inválido.",
    excepcion_manejo=ValueError,
    en_error=None,
):
    if en_error is None:
        en_error = en_invalido

    return entrada_ciclo(
        funcion_entrada=ticeni_ciclo(entrada_texto),
        validador=validador,
        transformador=transformador,
        en_invalido=iee_ciclo(en_invalido),
        excepcion_manejo=excepcion_manejo,
        en_error=iee_ciclo(en_error),
    )


def pedir_asiento(
    texto="Elige el asiento (0 para volver al menú principal): ",
):
    return tic_entrada_numero_ciclo(
        entrada_texto=texto,
        validador=lambda x: x in range(29),
        en_invalido="Número del asiento inválido.",
    )


def pedir_respuesta(texto="¿Se desea continuar, (S/N)? "):
    respuesta = tic_entrada_ciclo(
        entrada_texto=texto,
        validador=lambda x: es_respuesta(x),
        en_invalido="Respuesta inválida.",
    )
    return es_afirmativo(respuesta)


def imprimir_encabezado(s):
    print(f"{color.NEGRITAS}{color.OKAZUL}{s}{color.FIN}")
    print("=" * len(s) + "\n")


def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def mensaje(s):
    return f"*** {s}\n    Presionar {color.CABECERA}<Enter>{color.FIN} para continuar. "


def mensaje_error(s):
    return f"*** {color.ERROR}Error{color.FIN}: {s}\n    Presionar {color.CABECERA}<Enter>{color.FIN} para continuar. "


def imprimir_esperar(s):
    tic_entrada(mensaje(s))


def imprimir_error_esperar(s):
    tic_entrada(mensaje_error(s))


def esperar_continuar():
    tic_entrada(f"Presionar {color.CABECERA}<ENTER>{color.FIN} para continuar. ")


def imprimir_reporte_archivos_cargados(
    argumentos, cargados, errores_archivos, errores_asientos
):
    if "--cargar" in argumentos:
        if len(errores_archivos) > 0:
            print(
                f"{color.ERROR}ERROR: No se pudieron cargar los siguientes archivos (¿existen?){color.FIN}"
            )
            for archivo in errores_archivos:
                print(f"    - {color.NEGRITAS}{archivo}{color.FIN}")
        if len(errores_asientos) > 0:
            print(
                f"{color.ERROR}ERROR: Los siguientes archivos tuvieron entradas mal formadas [nombre del archivo seguido por los índices de entradas]:{color.FIN}"
            )
            for nombre, entradas_fallidas in errores_asientos:
                print(
                    f"    - {color.NEGRITAS}{nombre}{color.FIN}: {', '.join(str(n) for n in entradas_fallidas)}"
                )
    plural = "s" if cargados != 1 else ""
    if cargados > 0:
        print(
            f"{color.OKVERDE}✓ Cargado{plural} {color.NEGRITAS}{cargados}{color.FIN}{color.OKVERDE} asiento{plural} de archivos{color.FIN}"
        )


def es_afirmativo(s):
    """
    Determinar si una cadena de texto entrada por el usuario
    representa una afirmación. Esta función sanitiza su argumento.

    :param s: la cadena del usuario
    :returns: booleano confirmando si es una afirmación
    """
    return s.strip().lower() in ("s", "si", "sí", "y", "yes")


def es_negativo(s):
    """
    Determinar si una cadena de texto entrada por el usuario
    representa una negación. Esta función sanitiza su argumento.

    :param s: la cadena del usuario
    :returns: booleano confirmando si es una negación
    """
    return s.strip().lower() in ("n", "no")


def es_respuesta(s):
    """
    Determinar si una cadena de texto entrada por el usuario
    representa una respuesta, ya sea afirmativa o negativa. Esta
    función sanitiza su argumento.

    :param s: la cadena del usuario
    :returns: booleano confirmando si es una respuesta
    """
    return es_afirmativo(s) or es_negativo(s)


def es_alfabetico(s):
    return all(car.isalpha() or car.isspace() for car in s)

import os
import sys


def color_activado(activar):
    return (
        sys.stdout.isatty()
        and os.environ.get("NO_COLOR") is None
        and os.environ.get("TERM") != "dumb"
        and activar
    )


activar = any(arg == "--color" for arg in sys.argv[1:])
color = color_activado(activar)

CABECERA = "\033[95m" if color else ""
OKAZUL = "\033[94m" if color else ""
OKCIAN = "\033[96m" if color else ""
OKVERDE = "\033[92m" if color else ""
ADVERTENCIA = "\033[93m" if color else ""
GRIS = "\033[0;37m" if color else ""
ERROR = "\033[91m" if color else ""
FIN = "\033[0m" if color else ""
NEGRITAS = "\033[1m" if color else ""
SUBRAYADO = "\033[4m" if color else ""

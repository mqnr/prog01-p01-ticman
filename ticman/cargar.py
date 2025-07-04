from ticman.asientos import OCUPADO, asiento_actualizar, asiento_numero, asiento_vacio
import ticman.mapa as mapa


def cargar_archivos(argumentos):
    asientos_cargados = mapa.nuevo()
    archivos_no_encontrados = []
    asientos_fallados = mapa.nuevo()

    for i in range(len(argumentos)):
        if argumentos[i] == "--cargar" and i + 1 < len(argumentos):
            archivo = argumentos[i + 1]
            try:
                procesar_archivo(archivo, asientos_cargados, asientos_fallados)
            except FileNotFoundError:
                archivos_no_encontrados.append(archivo)

    return asientos_cargados, archivos_no_encontrados, asientos_fallados


def procesar_archivo(archivo, asientos_cargados, asientos_fallados):
    with open(archivo, "r") as f:
        contenido = f.read().split("\n\n")
        fallado = False
        for j, entrada in enumerate(contenido):
            try:
                asiento = analizar_entrada(entrada)
                mapa.actualizar(asientos_cargados, (asiento_numero(asiento), asiento))
            except ValueError:
                manejar_error_entrada(archivo, j, asientos_fallados, fallado)
                fallado = True


def manejar_error_entrada(archivo, indice_entrada, asientos_fallados, fallado):
    archivo_errores = mapa.obtener(asientos_fallados, archivo)
    if archivo_errores is None:
        archivo_errores = [indice_entrada + 1]
        mapa.actualizar(asientos_fallados, (archivo, archivo_errores))
    else:
        archivo_errores.append(indice_entrada + 1)


def analizar_entrada(s):
    partes = s.strip().split("\n")
    if len(partes) != 4:
        raise ValueError(
            f"La cadena de entrada no contiene el número de elementos esperado. Esperado: 4. Obtenido: {len(partes)}"
        )

    numero, nombre, identificacion, destino = partes

    asiento = asiento_vacio(int(numero))
    asiento_actualizar(
        asiento,
        estado=OCUPADO,
        destino_codigo=destino,
        pasajero=mapa.nuevo(("nombre", nombre), ("id", identificacion)),
    )

    return asiento

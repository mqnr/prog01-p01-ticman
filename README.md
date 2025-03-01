# TIC Manager (ticman)

ticman is a CRUD terminal app. It's the first semester's final project for our Software Engineering undergrad. We avoided several useful features of Python because we hadn't seen them in class yet, though we broke this rule in four places, namely in making the program take a `--color` flag to enable colored output, a `--cargar` flag to load seats from files, in using regexes, and in handling exceptions.

## What does it do?

As was said, it's a pretty standard CRUD app. You can create seat reservations for a flight, you can update them, delete them, view the seating map, and whatnot. However, no data is persisted.

## Self-imposed constraints

- Programming in Spanish (even for stuff that isn't user-facing)
- No third-party libraries
- No classes
- No built-in dictionaries
- No type hints
- No features from Python 3.9 onwards--you must be able to run it with Python 3.8
- The project should be portable; it should run the same in cutting-edge terminal emulators in Linux and the Windows command prompt

## On not using built-in dictionaries

This proved to be our most pervasive constraint. We wrote four trivial functions to help us treat lists of two-valued tuples as dictionaries, which we termed "pseudo-maps," and then built abstractions on top of them. Here's what using a pseudo-map looks like:

```python
pmapa = mapa.nuevo((1, "one"), (2, "two"), (3, "three"))

mapa.actualizar(pmapa, (4, "four"))  # adds the key-value pair to the pseudo-map
mapa.actualizar(pmapa, (2, "dos"))  # this modifies the existing key-value pair

print(mapa.obtener(pmapa, 2))  # "dos"
print(mapa.obtener(pmapa, 5))  # None
```

## What does TIC mean?

Transporte Intergaláctico Cajeme, which is Spanish for "Cajeme Intergalactic Transport," the fictional company starring in the project's spec.

## Running

It's pretty straightforward. Clone the repository, and at the root, run the `main.py` file with a Python interpreter.

## Team members

- Oscar Adrián Castán López
- Martín Zamorano Acuña

## License

The MIT License. See `LICENSE` for more.

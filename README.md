# Ejercicios de Factorial en Paralelo

Este directorio contiene versiones de un mismo ejercicio para comparar ejecucion secuencial y paralela en Python.

Objetivo del ejercicio:
- Calcular el factorial de cada numero de una lista.
- Calcular el promedio de esos factoriales de forma secuencial.
- Comparar tiempos entre distintas implementaciones.

## Archivos

- `secuential.py`: version secuencial (baseline).
- `factorial_threadpoolexecutor.py`: paralelo con `ThreadPoolExecutor`.
- `factorial_processpoolexecutor.py`: paralelo con `ProcessPoolExecutor`.
- `factorial_multiprocessing.py`: paralelo con `multiprocessing.Pool`.
- `factorial_threading.py`: paralelo con `threading` manual.
- `factorial_lib.py`: funciones compartidas.
- `factorial.md`: enunciado para estudiantes.

## Requisitos

- Python 3.10+ (recomendado usar el entorno virtual del proyecto).

## Como ejecutar

Desde la raiz del repo:

```bash
source venv/bin/activate
cd factorial
```

Ejecutar baseline secuencial:

```bash
python secuential.py --workers 1
```

Ejecutar variantes paralelas:

```bash
python factorial_threadpoolexecutor.py --workers 4
python factorial_processpoolexecutor.py --workers 4
python factorial_multiprocessing.py --workers 4
python factorial_threading.py --workers 4
```

## Entrada personalizada (opcional)

Todos los scripts aceptan `--numbers` como lista separada por comas:

```bash
python secuential.py --numbers 5,7,10 --workers 1
python factorial_processpoolexecutor.py --numbers 5,7,10 --workers 4
```

Si no se envia `--numbers`, se usa una lista por defecto reproducible definida en `factorial_lib.py`.

## Que comparar en clase

- `Tiempo (segundos)` entre variantes.
- `Promedio final (2 decimales)` para verificar que todas den el mismo resultado.
- Diferencias entre hilos y procesos en una tarea CPU-bound.

# Ejercicio: Factoriales en Paralelo

## Objetivo
Implementar cinco variantes para resolver el mismo problema:

1. Calcular el factorial de cada numero de una lista en paralelo.
2. Calcular el promedio de los factoriales en forma secuencial.

El promedio final no debe paralelizarse.

## Problema
Dada una lista de enteros no negativos, por ejemplo:

- [100, 120, 140, 160, 180, 200, 220, 240]

hacer lo siguiente:

1. Obtener el factorial de cada elemento.
2. Guardar esos resultados en una lista.
3. Calcular el promedio final de esa lista en forma secuencial.

## Librerias y scripts requeridos
Crear tambien una version base secuencial para comparar resultados y tiempos:

1. secuential.py

Crear un script por cada biblioteca:

1. concurrent.futures.ThreadPoolExecutor
2. concurrent.futures.ProcessPoolExecutor
3. multiprocessing
4. threading

Ademas, crear un modulo comun para evitar repetir codigo (por ejemplo, factorial y promedio secuencial).

## Restricciones
1. Usar solo la biblioteca estandar de Python.
2. Mantener el codigo simple y didactico.
3. El promedio final debe ser secuencial en todos los casos.
4. Usar la misma lista de entrada para todas las variantes.

## Entregables
1. Modulo comun con funciones compartidas.
2. Cinco scripts (uno secuencial y cuatro paralelos).
3. Ejecucion de cada script mostrando:
   - cantidad de workers
   - tiempo de ejecucion
   - promedio final

## Verificacion
1. El promedio final debe ser exactamente igual en las cinco variantes.
2. El flujo debe ser: factoriales en paralelo, promedio en secuencial.

## Ejemplo de ejecucion
```bash
python secuential.py --workers 1
python factorial_threadpoolexecutor.py --workers 4
python factorial_processpoolexecutor.py --workers 4
python factorial_multiprocessing.py --workers 4
python factorial_threading.py --workers 4
```

## Pregunta de reflexion
Explicar por que, para este tipo de trabajo CPU-bound en CPython, el uso de procesos suele escalar mejor que el uso de hilos.

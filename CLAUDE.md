# Sistemas Paralelos — UNTDF Fecha límite de entrega: 23 de abril de 2026

Durante las clases trabajamos con distintas estrategias para multiplicar matrices cuadradas NxN
en Python, tanto con la forma tradicional, como transpuesta. Este trabajo requiere la
implementación secuencial tradicional , transpuesta secuencial , threading ,
multiprocessing y numba  . El objetivo de este práctico es que cada
estudiante ejecute los benchmarks en su propia máquina, analice los resultados y los explique
con criterio.

## Consignas

### 1. Ejecución del benchmark

Ejecutar todos los scripts provistos para al menos las siguientes combinaciones de parámetros:
--workers --complexity
1 512
4 512
4 1024
N físicos 1024

> Usar --seed 2026 para establecer la semilla, entonces los resultados serán reproducibles. Registrar todos los tiempos, checksums, speed-ups y eficiencias obtenidos.

### 2. Tabla comparativa

Armar una tabla de resultados similar a la realizada y revisada en el trabajo anterior para cada
combinación ejecutada, incluyendo las columnas: método, tiempo (s), checksum, speed-up y
performance (%).

### 3. Análisis

Responder, siendo breve:
¿Por qué threading no mejora en esta carga de trabajo?
¿Qué explica la mejora de las versiones con matriz transpuesta?
¿El speed-up de multiprocessing es lineal con los workers? ¿Por qué?
¿Qué aporta numba.njit incluso sin paralelismo ( parallel=False )?
¿Se puede superar una eficiencia del 100%? ¿Cómo se interpreta eso?

### 4. Entorno y hardware

Al inicio del informe, incluir:
CPU (modelo, núcleos físicos y lógicos)
RAM disponible
Sistema operativo y versión de Python
Si tienen GPU disponible (CUDA o MPS): reportar también los resultados de PyTorch y
comentar las diferencias.

## Formato de entrega

Un único archivo PDF o Markdown.
Nombre del archivo: apellido_nombre_matrix.pdf (o .md ).
Enviar por email.

## Notas

El checksum debe ser idéntico entre todos los métodos para una misma --complexity . Si
no lo es, hay un error en la implementación.
Si algún script falla en su entorno (p. ej. pytorch sin GPU), indicarlo en el informe y explicar
por qué

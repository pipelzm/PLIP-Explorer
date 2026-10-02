# Validación — PLIP Explorer 0.1.0a4

Actualización: 2026-10-02. Estado: alpha para primera prueba en ChimeraX.

## Actualización 0.1.0a4

Se añaden alemán, francés, chino simplificado y japonés, con ayuda breve en cada
idioma. Las pruebas recorren los siete idiomas y todos los mensajes, verifican
parámetros, preservación de estado y archivos de ayuda en el wheel. Los textos
científicos y las rutas se mantienen sin cambios. No se ha ejecutado la interfaz
nativa en este entorno ni una revisión visual de fuentes CJK dentro de ChimeraX.

Resultado actual: 25 pruebas ejecutadas, 24 correctas y 1 omitida (motor PLIP
no instalado). `test-results.txt` contiene la salida de 0.1.0a4;
`test-results-0.1.0a3.txt` conserva la de 0.1.0a3.

## Actualización 0.1.0a3

El usuario confirmó que 0.1.0a2 abre el panel en ChimeraX 1.12/macOS M1 y
proporcionó capturas. Esto no comprueba todavía la representación molecular.

Se incorporan español, inglés y portugués, preferencia persistente, traducción
sin reconstruir la escena, ayuda breve EN/PT y carga de ejemplos desde el wheel.
Se verifican catálogos y parámetros, conservación del estado del controlador
con adaptadores mínimos (sin Qt), ejemplos y bytes empaquetados.

La ejecución de 0.1.0a3 comprendió 25 pruebas: 24 correctas y una omitida porque
el motor PLIP no está instalado en este entorno. No se ejecutó la nueva interfaz
ni el renderizado dentro de ChimeraX. Ver `test-results.txt`.

## Corrección del registro en 0.1.0a2

El usuario comprobó la instalación de 0.1.0a1 en ChimeraX 1.12/macOS M1 y
detectó el error `bundle forgot to override initialize method`. Se retiró la
declaración innecesaria de inicialización personalizada del XML y del wheel.

La prueba de contrato del bundle reproduce la inconsistencia en 0.1.0a1 y
pasa con la corrección. También se verifica la carga diferida del panel,
el paso de argumentos de la API v1 y la coincidencia entre fuentes y wheel.
Es una comprobación del paquete y sus puntos de entrada con una clase base
mínima de prueba; no ejecuta ChimeraX ni Qt.

En 0.1.0a2 se ejecutaron 21 pruebas: 20 pasaron y una quedó omitida
porque el motor PLIP no está instalado en el entorno actual. El análisis real
de PLIP se comprobó durante la primera entrega, como se detalla abajo.

## Pruebas de la primera entrega (2026-10-01)

18 pruebas automatizadas correctas (`tests/test_core.py`), incluyendo:

- Lectura de ocho categorías, distancias D–A y geometría de puentes de agua.
- Rechazo de XML incorrecto; advertencias para datos no finitos y categorías desconocidas.
- Conservación de sitios sin interacciones y exportación CSV completa.
- PDB incompatible con la estructura/centros del informe: rechazo explícito.
- Restricciones de entrada para conformaciones alternativas y códigos de inserción.
- Rutas con espacios y conservación del ejecutable de un entorno virtual.
- Protección contra reutilizar una carpeta con un informe previo.
- Interrupción de un proceso por cancelación y por tiempo máximo, en POSIX.
- Ejecución real del motor desde el adaptador y comparación con PLIP independiente,
  usando la misma estructura y `--nohydro` para excluir diferencias aleatorias
  de protonación. Se compararon los campos de todas las interacciones.

Pruebas de datos reales con protonación activada:

| Estructura | Resultado | Comprobación |
|---|---|---|
| 1VSN, NFT:A:283 | 13 interacciones | 26 extremos atómicos coinciden con el PDB dentro de 0,025 Å. |
| 1EVE, E20:A:2001 | 10 interacciones | 5 hidrofóbicas, 1 H, 1 agua, 2 π–π y 1 catión–π. |
| 1EVE, todos los sitios | 20 interacciones en 5 sitios | Validación de extremos y centros; incluye un sitio sin interacciones. |

En las tres interacciones entre grupos del ligando E20, los centros calculados
a partir de los IDs del informe coincidieron con los centros informados por
PLIP: el mayor desvío observado fue menor que 0,001 Å (redondeo del XML).

Además se leyó y comprobó un informe 1VSN producido por PLIP 3.0.1.
La configuración externa propuesta para uso inicial emplea PLIP 2.4.0.

Entorno de cálculo observado: Linux x86-64; Python 3.12.14; PLIP 2.4.0;
numpy 2.5.3; lxml 6.1.3; openbabel-wheel 3.1.1.23, que informa Open Babel 3.1.0.
El paquete `openbabel-wheel` se usó en las pruebas de este entorno. La receta
conda de la guía no se ha ejecutado en macOS ni Windows.

Las pruebas del modelo de datos usan coordenadas leídas de los PDB. No simulan
una ejecución de ChimeraX ni certifican su API gráfica. El código Python también
se comprobó sintácticamente y se empaquetó como un wheel Python puro.

## Comprobación pendiente en ChimeraX

No había un ejecutable ni las bibliotecas de ChimeraX en el entorno de desarrollo.
Por ello siguen pendientes:

1. Instalación del wheel 0.1.0a4 y registro en Tools → Structure Analysis (0.1.0a2 confirmado por el usuario).
2. Apertura del panel 0.1.0a4, cambio de idioma y carga de ejemplos integrados.
3. Importar el ejemplo 1VSN y verificar la tabla de 13 filas.
4. Visibilidad de pseudobonds, colores, grosores y etiquetas de distancia.
5. Selección de filas y centrado/etiquetado de residuos.
6. Importar 1EVE y revisar los dos tramos de agua y centros aromáticos.
7. Guardar `.cxs`, cerrar/reabrir y verificar estructura, tabla y filtros.
8. Modificar coordenadas y verificar que las interacciones se ocultan.
9. Ejecutar PLIP desde el panel y verificar la bitácora local.
10. Repetir en cada sistema operativo que se quiera distribuir.

Las categorías salina y metálica se probaron con datos sintéticos para lectura
y construcción de segmentos. Se necesitan complejos reales adicionales para
validar su representación antes de una versión estable.

## Evidencia reproducible

Los XML y PDB usados como ejemplos están en `examples/`. Los tests están en
`tests/`. `test-results.txt` conserva la salida de las pruebas de 0.1.0a4;
`test-results-0.1.0a2.txt` conserva las de 0.1.0a2;
`test-results-0.1.0a1.txt` conserva la ejecución original con PLIP instalado.
Las futuras ejecuciones desde el plugin registran versión de PLIP, argumentos,
opción de protonación, duración, estado, errores y ruta del PDB en `run.json`.

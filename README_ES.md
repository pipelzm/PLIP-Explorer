# PLIP Explorer para ChimeraX

**Versión 0.1.0a4 — prototipo alpha, 2 de octubre de 2026.**

Extensión nativa con panel Qt para ejecutar PLIP localmente e inspeccionar sus
interacciones en el motor 3D de ChimeraX. No requiere PyMOL. El instalador contiene
la extensión; PLIP y Open Babel se configuran en un entorno Python separado.

El núcleo fue probado con PLIP real y estructuras 1VSN y 1EVE. El usuario confirmó
la instalación y apertura del panel 0.1.0a2 en ChimeraX 1.12/macOS M1. La versión
0.1.0a4 añade idiomas y ejemplos integrados; su interfaz, representación 3D y
recuperación de sesiones quedan pendientes de comprobación en ChimeraX. El entorno
de desarrollo no dispone del visor. No se presenta como una versión estable validada.

## 1. Instalar el plugin

Descomprime el paquete completo. En la línea de comandos **de ChimeraX**, ejecuta
lo siguiente, sustituyendo la ruta por la ubicación real del archivo `.whl`:

```text
toolshed install "/ruta/PLIP_Explorer_0.1_alpha/dist/chimerax_plipexplorer-0.1.0a4-py3-none-any.whl"
```

Ejemplo en macOS, si descomprimiste el ZIP en Descargas:

```text
toolshed install "/Users/TU_USUARIO/Downloads/PLIP_Explorer_0.1_alpha/dist/chimerax_plipexplorer-0.1.0a4-py3-none-any.whl"
```

Abre **Tools → Structure Analysis → PLIP Explorer**. También puedes ejecutar:

```text
ui tool show "PLIP Explorer"
```

Si el menú no se actualiza, reinicia ChimeraX. Se dirige a una instalación con
Python ≥3.10 y Qt6 (ChimeraX 1.8 o posterior como objetivo de compatibilidad;
no se ha certificado una matriz de versiones). El `.whl` es Python puro; el motor
PLIP y sus dependencias sí dependen del sistema operativo.

## 2. Primera prueba, sin instalar PLIP

La versión 0.1.0a4 incluye **Ejemplo → 1VSN → Cargar ejemplo**. No necesitas
configurar el motor PLIP para esta prueba. Consulta **ACTUALIZACION_0.1.0a3.md**
para los resultados esperados y la comprobación paso a paso.

También puedes importar manualmente los archivos del ZIP:

1. Pulsa **Importar XML + PDB…**.
2. Selecciona `examples/1VSN/report.xml`.
3. Selecciona `examples/1VSN/1VSN.pdb`.
4. El sitio `NFT:A:283` debe contener **13 interacciones**.
5. Activa/desactiva categorías y pulsa una fila para centrar sus residuos.
6. Prueba **Distancias 3D → Aplicar estilo**, **Exportar CSV…** y
   **Guardar sesión…**.

El segundo ejemplo es `examples/1EVE/`. Su sitio `E20:A:2001` contiene 10
interacciones en el informe incluido: 5 contactos hidrofóbicos, 1 puente de
hidrógeno, 1 puente de agua, 2 apilamientos π–π y 1 interacción catión–π.
Los otros cuatro sitios corresponden a NAG; uno no tiene interacciones.

Estos números describen los informes incluidos. Un análisis nuevo puede variar
por la protonación, la versión del motor o la preparación de la estructura.

### Idiomas

El selector **Idioma** permite usar Español, English, Português, Deutsch,
Français, 简体中文 (chino simplificado) y 日本語, y recuerda la preferencia. Cambia los textos del panel y conserva el sitio, filtros, colores y
datos. Los mensajes externos, identificadores científicos y campos exportados
se mantienen en su formato original. Se incluyen guías breves EN/PT/DE/FR/ZH/JA.
Consulta ACTUALIZACION_0.1.0a4.md para los nuevos idiomas.

## 3. Configurar PLIP para analizar tus complejos

La versión de referencia de este prototipo es **PLIP 2.4.0**. El lector también
se comprobó con un informe de PLIP 3.0.1; la compatibilidad de otras versiones
del motor debe comprobarse. No instales sus dependencias en el Python interno
de ChimeraX.

Si ya tienes un entorno de PLIP funcional, actívalo, ejecuta este comando en una
terminal y pega la ruta obtenida en **Motor PLIP**:

```bash
python -c "import sys; print(sys.executable)"
```

Para crear un entorno, se propone esta receta con conda/Miniforge, en la terminal
del sistema (en Windows, una terminal donde conda esté inicializado):

```bash
conda create -n plip-chimerax -c conda-forge python=3.11 openbabel=3.1.1 numpy lxml pip setuptools wheel
conda activate plip-chimerax
python -m pip install --no-deps --no-build-isolation plip==2.4.0
python -c "import sys; from plip.basic import config; from openbabel import openbabel; print(sys.executable); print('PLIP', config.__version__); print('Open Babel', openbabel.OBReleaseVersion())"
python -m plip.plipcmd -h
```

Se usan `--no-deps` y `--no-build-isolation` porque las dependencias ya están
instaladas en ese entorno y el empaquetado antiguo de PLIP puede intentar
recompilar Open Babel durante la construcción aislada. **La receta conda debe
comprobarse en tu sistema**; las pruebas de esta entrega utilizaron Linux x86-64,
Python 3.12.14, PLIP 2.4.0 y Open Babel 3.1.0 (paquete openbabel-wheel 3.1.1.23).

Para macOS Apple Silicon utiliza un entorno con arquitectura ARM64; para Windows,
un entorno correspondiente a tu instalación de Windows. No se exige Docker.
La extensión no instala paquetes ni descarga estructuras por su cuenta.

## 4. Analizar una estructura

1. Abre en ChimeraX un **único modelo que contenga proteína y ligando**.
2. Abre el plugin y pulsa **Actualizar** si el modelo no aparece.
3. Selecciona ese complejo en el panel.
4. Configura **Motor PLIP** con el ejecutable Python anterior. Conserva la ruta
   del entorno: no sustituyas un enlace simbólico por el Python del sistema.
5. Elige la carpeta de resultados.
6. Decide si PLIP debe añadir hidrógenos polares. Al desmarcar esa opción se usa
   `--nohydro`: debes proporcionar una preparación con hidrógenos apropiada.
7. Pulsa **Analizar complejo**. Después elige un sitio en el desplegable.

La ejecución se realiza localmente, en un proceso separado. El panel permite
cancelar y establece un límite de 10 minutos para esta versión. Se conserva una
carpeta por ejecución con `input.pdb`, `report.xml`, `plip.log`, `run.json` y los
archivos adicionales de PLIP. El programa no transmite estructuras a un servidor.

Se abre una copia del PDB original/corregido indicado por PLIP. Al finalizar un
análisis se oculta el modelo de entrada para evitar superposiciones; puedes
volver a mostrarlo desde el Model Panel. Su estructura no se modifica.

Si tienes receptor y pose como modelos separados, combínalos previamente en un
único complejo, manteniendo sus posiciones relativas. La interfaz alpha aún no
incluye un ensamblador de receptor/ligando ni un selector de átomos para preparar
automáticamente ese complejo.

## 5. Representación y controles

- Ocho categorías de PLIP, con visibilidad y color independientes.
- Pseudobonds nativos entre marcadores situados en las coordenadas del informe.
  Los marcadores son objetos de representación, no nuevos átomos químicos de la
  estructura. Se agrupan bajo la copia analizada en el Model Panel.
- Los puentes de agua tienen dos tramos. Las interacciones entre grupos utilizan
  centros geométricos; no se sustituyen por un átomo cercano.
- Se verifica la correspondencia de los extremos atómicos con el PDB y la de los
  centros con los IDs del informe. Un PDB que no coincide produce un error.
- La tabla conserva el significado de las distancias: D–A para puentes de
  hidrógeno, dos medidas A–W y D–W para puentes de agua, centros para π–π.
- Los datos completos de PLIP están disponibles en las descripciones emergentes
  de las filas y en una columna JSON del CSV.
- Al cambiar las coordenadas, la cantidad de átomos o la numeración de la copia
  analizada, las líneas se ocultan y se requiere recalcular. Mover o rotar el
  modelo completo no altera sus interacciones internas.
- Los filtros afectan la vista y las filas visibles; **el CSV exporta todas las
  interacciones del sitio seleccionado**, incluidas las categorías ocultas.
- La sesión guarda el informe, la estructura, los objetos gráficos y el estado
  del panel. Su restauración requiere el plugin instalado y queda pendiente de
  comprobación en ChimeraX.

El cambio de estados químicos/órdenes de enlace sin cambio de coordenadas no es
una señal fiable para invalidar este análisis. Tras cualquier edición química,
vuelve a ejecutarlo. Al cerrar el panel se detiene la vigilancia de cambios;
los objetos 3D que permanezcan son una representación estática del cálculo.

## 6. Alcance y límites de esta alpha

- Complejos proteína–molécula pequeña, un modelo y una conformación por análisis.
- La entrada al motor es PDB. Un mmCIF abierto puede exportarse solo si cabe en
  las restricciones del PDB estándar.
- Se rechazan cadenas de más de un carácter, más de 99 999 átomos, códigos de
  inserción y conformaciones alternativas sin resolver, para evitar mapeos
  ambiguos. Prepara una copia adecuada antes de analizar esos casos.
- No incluye análisis de trayectorias, cálculo por fotograma, diagrama 2D,
  comparación masiva de poses ni un instalador automático del motor.
- PLIP usa reglas geométricas/químicas. El plugin representa sus resultados;
  no calcula afinidad ni prueba experimentalmente la existencia de un enlace.
- En esta entrega la coordinación metálica y los puentes salinos tienen pruebas
  de lectura sintéticas. La prueba real de las otras seis categorías se realizó
  con los ejemplos incluidos; falta validación gráfica de todas ellas.
- Ante una fila mal formada se informa la omisión en el Log; el panel muestra
  cuántas advertencias produjo la lectura. No se inventan valores faltantes.

## 7. Solución de problemas

| Mensaje o situación | Acción |
|---|---|
| No aparece PLIP Explorer | Reinicia ChimeraX y revisa el Log de instalación. |
| `No module named plip` | El campo Motor PLIP apunta a un Python sin PLIP. Obtén `sys.executable` dentro del entorno correcto. |
| Error de `openbabel` | Comprueba el motor con `python -m plip.plipcmd -h` fuera de ChimeraX. |
| PDB y XML no coinciden | Importa el PDB original/corregido del mismo análisis; no un archivo renumerado. |
| No se detectan ligandos | Revisa los registros HETATM y el filtrado de ligandos de PLIP. |
| Interacciones ocultas tras editar | Selecciona la copia editada en Complejo y ejecuta un análisis nuevo. |
| Error de interfaz o API | Copia el mensaje del Log e indica versión de ChimeraX, sistema operativo y pasos utilizados. |

No elimines el PDB de la carpeta de resultados hasta comprobar que la sesión se
guarda y restaura correctamente en tu instalación.

## 8. Desarrollo y comprobación

Estructura: `src/tool.py` (panel), `src/engine.py` (proceso), `src/report.py`
(lector y datos), `src/render.py` (objetos gráficos), `tests/test_core.py`.

Pruebas independientes del visor:

```bash
python -m unittest discover -s tests -v
```

La prueba que vuelve a ejecutar PLIP se activa con la variable de entorno
`PLIP_TEST_PYTHON`, apuntando al Python del motor. Las pruebas de interrupción
se ejecutan en sistemas POSIX. Ver `VALIDACION.md`.

Para modificar e instalar desde el código, ejecuta en ChimeraX:

```text
devel install "/ruta/PLIP_Explorer_0.1_alpha"
```

Para desinstalar:

```text
toolshed uninstall ChimeraX-PLIPExplorer
```

La extensión se entrega bajo MIT. PLIP y ChimeraX mantienen sus propias
licencias; su código y sus ejecutables no están incluidos en este paquete.
Es un proyecto independiente, sin afiliación oficial con PLIP o UCSF.

## Fuentes y ejemplos

- PLIP: https://github.com/pharmai/plip
- Formato XML: https://github.com/pharmai/plip/blob/master/DOCUMENTATION.md
- API y bundles de ChimeraX: https://chimerax.readthedocs.io/en/latest/tutorials/tutorial_tool_qt.html
- Pseudobonds: https://www.cgl.ucsf.edu/chimerax/docs/user/commands/pbond.html
- Estructura 1VSN: https://www.rcsb.org/structure/1VSN
- Estructura 1EVE: https://www.rcsb.org/structure/1EVE

Los informes de ejemplo fueron calculados con PLIP 2.4.0 y protonación activada.
Solo se normalizaron las rutas `pdbfile`/`filename` de los XML para que los ejemplos
sean portátiles; los datos de interacciones se conservaron. Las estructuras se
descargaron de RCSB PDB. Consulta las fichas PDB y la documentación de PLIP para
atribuir las estructuras y el análisis en trabajos científicos.

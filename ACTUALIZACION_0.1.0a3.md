# PLIP Explorer 0.1.0a3

Esta actualización añade un selector persistente **Español / English / Português**
y un botón **Cargar ejemplo** con resultados precalculados de 1VSN y 1EVE.
Se mantiene la corrección de inicialización de 0.1.0a2.

## Actualizar

Sustituye la carpeta anterior de Descargas por la de este ZIP. Conserva tus
resultados propios aparte. Ejecuta en la línea de comandos de ChimeraX:

```text
toolshed install /Users/pipelzm/Downloads/PLIP_Explorer_0.1_alpha/dist/chimerax_plipexplorer-0.1.0a3-py3-none-any.whl
```

Cierra completamente ChimeraX con **⌘Q**, vuelve a abrirlo y ejecuta:

```text
ui tool show "PLIP Explorer"
```

## Prueba de visualización, sin configurar el motor

1. Selecciona **1VSN** en **Ejemplo** y pulsa **Cargar ejemplo**.
2. En el sitio **NFT:A:283** deben aparecer **13 filas** y líneas en la estructura.
3. Las categorías deben sumar **4 contactos hidrofóbicos + 7 puentes de hidrógeno
   + 2 enlaces de halógeno**.
4. Desmarca **Puente de hidrógeno**: deben quedar **6 filas visibles** y ocultarse
   las líneas de esa categoría. El contador superior sigue mostrando el total.
5. Vuelve a marcarlo. Pulsa una fila: deben seleccionarse y centrarse sus residuos.
6. Marca **Distancias 3D** y pulsa **Aplicar estilo**: comprueba que aparecen
   etiquetas. Un puente de agua utiliza dos tramos; los contactos entre grupos
   aromáticos utilizan centros, no un átomo arbitrario.
7. Cambia **Idioma** a English o Português: deben cambiar los textos y encabezados,
   manteniendo el sitio seleccionado, filtros, colores y datos. La preferencia
   se conserva al volver a abrir el panel.
8. **Exportar CSV…** debe producir 13 registros de datos más el encabezado. Exporta
   todas las interacciones del sitio, también las ocultas por filtros.
9. Para comprobar sesiones, guarda una sesión de prueba `.cxs` y ábrela de nuevo
   en ChimeraX. Comprueba que reaparecen estructura, tabla y filtros.

La segunda prueba es **1EVE**, sitio **E20:A:2001**, con **10 filas**:

| Categoría | Cantidad |
|---|---:|
| Contacto hidrofóbico | 5 |
| Puente de hidrógeno | 1 |
| Puente de agua | 1 |
| Apilamiento π–π | 2 |
| Interacción catión–π | 1 |

1EVE contiene además otros cuatro sitios; no confundas el total de todos ellos
con las 10 interacciones de E20. Los ejemplos se abren como modelos separados.
Si se superponen, oculta el anterior en el panel de modelos de ChimeraX.

## Qué demuestra cada prueba

- La apertura confirmada en 0.1.0a2 demuestra que el bundle se registra y el panel
  se construye en tu ChimeraX 1.12/macOS M1.
- Cargar los ejemplos comprueba importación, correspondencia PDB/XML, tabla y
  representación. **No ejecuta PLIP** y no requiere configurarlo.
- Para comprobar el motor, configura un Python que contenga PLIP según README_ES,
  abre uno de los PDB incluidos, selecciónalo en Complejo y pulsa Analizar complejo.
  El resultado debe generar una carpeta nueva con `report.xml`, `plip.log` y
  `run.json`. En este último debe figurar `status: complete` y la versión de PLIP.
  Repetir con protonación o versiones distintas puede cambiar las cantidades;
  los números anteriores solo son exactos para los informes incluidos.

## Idiomas y datos

Los controles, categorías, estados, mensajes propios y títulos de diálogos se
traducen. Los diálogos nativos pueden usar el idioma de macOS. Los mensajes
externos de ChimeraX/PLIP/Open Babel y sus bitácoras mantienen su texto original.
No se traducen identificadores de residuos, campos XML/JSON, unidades ni claves
del CSV. La guía extensa está en español; se incluyen guías rápidas en inglés y
portugués y ayuda breve en esos idiomas dentro del bundle.

Las pruebas automatizadas no sustituyen la comprobación gráfica en tu Mac.

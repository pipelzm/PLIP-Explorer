# PLIP Explorer 0.1.0a4

Añade **Deutsch, Français, 简体中文 (chino simplificado) y 日本語** a Español,
English y Português. Se traducen controles, categorías, tabla, estados, mensajes
propios y ayuda breve. La preferencia se guarda y puede cambiarse con un informe
abierto, conservando selección de sitio, filtros, colores y datos.

## Instalación en tu Mac

Sustituye la carpeta del ZIP anterior en Descargas. Conserva tus resultados propios
aparte. En la línea de comandos de ChimeraX ejecuta:

```text
toolshed install /Users/pipelzm/Downloads/PLIP_Explorer_0.1_alpha/dist/chimerax_plipexplorer-0.1.0a4-py3-none-any.whl
```

Cierra completamente ChimeraX con **⌘Q**, vuelve a abrirlo y ejecuta:

```text
ui tool show "PLIP Explorer"
```

El encabezado debe indicar **0.1.0a4**. Elige el idioma en el selector superior.
Cada idioma aparece con su nombre nativo, para poder volver a cambiarlo fácilmente.

## Comprobación

1. Carga el ejemplo 1VSN. El sitio NFT:A:283 debe tener 13 interacciones.
2. Cambia entre los siete idiomas. Deben actualizarse los textos sin recalcular
   las interacciones ni mover la cámara.
3. Cierra y vuelve a abrir el panel: debe conservarse el idioma elegido.
4. Comprueba que se muestran correctamente los caracteres chinos y japoneses
   y que puedes acceder a los controles con los textos más largos en alemán.

Los identificadores científicos, coordenadas, unidades y datos exportados no
cambian con el idioma. Los mensajes externos de PLIP, Open Babel y ChimeraX
conservan su texto original; los diálogos nativos pueden seguir el idioma del
sistema operativo.

Se incluyen guías rápidas DE/FR/ZH/JA, además de las anteriores. Las traducciones
se han comprobado por integridad y conservación de parámetros; su visualización
en ChimeraX 1.12/macOS M1 sigue pendiente de comprobación en tu instalación.

# Actualización 0.1.0a2 — ChimeraX 1.12

Corrige el error `bundle forgot to override initialize method` de 0.1.0a1.
El paquete declaraba `customInit=true` sin necesitar ni implementar los métodos
de inicialización/finalización exigidos por ChimeraX. La declaración se retiró
de ambos formatos de metadatos: `bundle_info.xml` y el wheel distribuido.

1. Sustituye la carpeta anterior `PLIP_Explorer_0.1_alpha` de Descargas por la
   carpeta de este ZIP actualizado. Conserva tus carpetas de resultados aparte.
2. En la línea de comandos de ChimeraX, ejecuta:

```text
toolshed install /Users/pipelzm/Downloads/PLIP_Explorer_0.1_alpha/dist/chimerax_plipexplorer-0.1.0a2-py3-none-any.whl
```

3. Cierra completamente ChimeraX con **⌘Q** y vuelve a abrirlo. Esto permite
   cargar el código y los metadatos nuevos en lugar de los retenidos en memoria.
4. Abre el panel:

```text
ui tool show "PLIP Explorer"
```

El encabezado del panel debe indicar **0.1.0a2**. Prueba después
`examples/1VSN/report.xml` y `examples/1VSN/1VSN.pdb` con **Importar XML + PDB…**.

Las pruebas añadidas comprueban la coherencia entre la declaración del bundle
y sus métodos, el encaminamiento del comando de apertura y que el wheel contiene
los metadatos/código corregidos. Estas pruebas no sustituyen la ejecución del
panel ni la visualización en una instalación real de ChimeraX.

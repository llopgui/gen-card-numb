# Recursos gráficos

Opcionalmente puedes añadir:

- **`icon.png`** — icono origen
- **`icon.ico`** — Windows (ventana, barra de tareas y ejecutable empaquetado con PyInstaller)

Si no existen, la aplicación y la compilación con `GenCardNumb.spec` funcionan igual (sin icono personalizado).

Para generar un `.ico` a partir de un PNG (requiere Pillow en `requirements-dev.txt`):

```bash
python tools/generate_icons.py
```

Opciones avanzadas: `python tools/generate_icons.py --help`.

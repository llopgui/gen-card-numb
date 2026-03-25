# Generador números de tarjeta (Luhn) — aplicación de escritorio

**Versión:** 1.0.0 (`APP_VERSION` en [`src/config.py`](src/config.py)).

Aplicación de **escritorio** en Python con interfaz **tkinter** para practicar el **algoritmo de Luhn** (módulo 10): validación y generación de números **ficticios** con fines **didácticos**.

> **Propósito educativo.** Este repositorio es un **ejercicio de programación** y de interfaz de usuario. No sustituye validación de pagos reales, no verifica tarjetas reales y **no está pensado** para entornos de producción ni cumplimiento normativo.

---

## Tabla de contenidos

- [Aviso de uso responsable](#aviso-de-uso-responsable)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Pruebas y calidad](#pruebas-y-calidad)
- [Empaquetado (ejecutable Windows)](#empaquetado-ejecutable-windows)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Licencia](#licencia)

---

## Aviso de uso responsable

Los números generados son **matemáticamente válidos según Luhn** pero **ficticios** respecto a emisores y cuentas reales.

**Queda prohibido** emplear este proyecto para fraude, eludir controles de pago o identidad, acceso no autorizado o cualquier actividad ilegal.

El **autor** no se hace responsable del **uso indebido** del código.

---

## Características

| Área | Descripción |
|------|-------------|
| **Validación** | Comprueba si un número pasa el algoritmo de Luhn. |
| **Generación unitaria** | Número aleatorio con prefijo BIN y longitud 13/16/19 (`secrets`). |
| **Lotes** | Hasta **10.000** números por lote, separadores configurables, exportación. |
| **Interfaz** | Misma línea visual que **gen-dni-esp** (cards, paleta SaaS, aviso legal). |

---

## Requisitos

- **Python 3.10+** (recomendado 3.12+).
- **tkinter** (incluido con Python en Windows en la mayoría de instalaciones).
- **Sin dependencias pip en tiempo de ejecución** (`requirements.txt` vacío a propósito).
- Desarrollo: ver `requirements-dev.txt` o `uv sync --extra dev`.

---

## Instalación

### Opción A: `uv` (recomendado)

```bash
python -m uv sync --extra dev
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

### Opción B: `venv` clásico

```bash
python -m venv .venv --upgrade-deps
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
```

---

## Uso

### Aplicación gráfica

Desde la **raíz del repositorio**:

```bash
python -m src.main
```

Equivalente directo a la GUI:

```bash
python -m src.card_gui
```

### Configuración

Toda la configuración (versión, título, límites de lote, paleta, separadores, prefijos BIN de ejemplo) está en **`src/config.py`**. No se usa fichero `.env`.

Con `DEBUG = True` en `config.py`, `main` activa **logging** en nivel DEBUG.

---

## Pruebas y calidad

```bash
pytest
```

Herramientas: **Black**, **Ruff**, **mypy**, **pytest-cov** (definidas en `requirements-dev.txt` y `pyproject.toml`).

---

## Recursos gráficos y ejecutable

En **`assets/`** puedes colocar **`icon.png`** (origen) e **`icon.ico`** (Windows: ventana, barra de tareas y ejecutable empaquetado). La GUI y el spec resuelven rutas también bajo PyInstaller (`sys._MEIPASS`).

### Regenerar el icono `.ico`

Script en el repositorio (requiere **Pillow**, incluida en `requirements-dev.txt`):

```bash
python tools/generate_icons.py
```

Opciones avanzadas: `python tools/generate_icons.py --help`.

### Generar el `.exe` (Windows, PyInstaller)

Se usa **`GenCardNumb.spec`** (`upx=False`: comprimir el binario con UPX suele **estropear el icono** del ejecutable en Windows).

```bash
python tools/build_exe.py
```

Con limpieza de `build/` antes:

```bash
python tools/build_exe.py --clean
```

Salida esperada: **`dist/GenCardNumb.exe`**. Más detalle en [`assets/README.md`](assets/README.md).

**Nota:** Si `pyinstaller` instalado vía `uv` da problemas, invoca siempre `python -m PyInstaller` (lo hace `tools/build_exe.py`).

---

## Estructura del proyecto

```text
gen-card-numb/
├── assets/              # Iconos opcionales (PNG / ICO)
├── docs/                  # Documentación adicional
├── src/
│   ├── main.py          # Punto de entrada (logging opcional)
│   ├── config.py        # Constantes (versión, ventana, lotes, colores, …)
│   ├── luhn.py          # Algoritmo Luhn (validación, generación)
│   └── card_gui.py      # Interfaz tkinter
├── tests/               # Pruebas automatizadas
├── tools/
│   ├── generate_icons.py   # Generación multi-resolución del .ico
│   └── build_exe.py        # Invocación reproducible de PyInstaller
├── GenCardNumb.spec     # Especificación de empaquetado
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── uv.lock
```

---

## Licencia

Añade un fichero `LICENSE` si publicas el repositorio; el uso del software es bajo tu responsabilidad según el [aviso de uso responsable](#aviso-de-uso-responsable).

---

<p align="center">
  <sub>Proyecto de ejemplo · Python · tkinter · Algoritmo de Luhn</sub>
</p>

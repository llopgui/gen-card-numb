"""
Aplicación gráfica para números de tarjeta con algoritmo de Luhn.

Validación, generación unitaria y por lotes con exportación.
Diseño alineado con gen-dni-esp (cards, paleta, separadores de lote).

ADVERTENCIA: Solo fines educativos. Los números generados son ficticios.
"""

from __future__ import annotations

import logging
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .config import (
    APP_NAME,
    BIN_PRESETS,
    COLORES,
    LOTE_MAX,
    LOTE_MIN,
    SEPARADORES,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_TITLE,
)
from .luhn import (
    format_card_number,
    generate_valid_card_number,
    truncar_para_clipboard,
    validate_luhn,
)

logger = logging.getLogger(__name__)


class CardApp:
    """
    Ventana principal: validar, generar y lotes con algoritmo de Luhn.
    """

    def __init__(self) -> None:
        """Inicializa la ventana y los widgets."""
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.resizable(True, True)
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root.configure(bg=COLORES["fondo"])
        self.root.wm_protocol("WM_DELETE_WINDOW", self._cerrar_seguro)

        self._generando_lote = False
        self._crear_estilos()
        self._crear_widgets()

    def _cerrar_seguro(self) -> None:
        """Cierra la aplicación de forma segura."""
        self.root.quit()
        self.root.destroy()

    def _crear_estilos(self) -> None:
        """Configura estilos modernos para ttk."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Card.TFrame",
            background=COLORES["superficie"],
            relief="flat",
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 11, "bold"),
            foreground=COLORES["texto"],
            background=COLORES["superficie"],
        )

        style.configure(
            "TLabel",
            font=("Segoe UI", 10),
            foreground=COLORES["texto"],
            background=COLORES["superficie"],
        )

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            background=COLORES["primario"],
            foreground="white",
            relief="flat",
        )
        style.map(
            "Primary.TButton",
            background=[("active", COLORES["primario_hover"])],
        )

        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            padding=(10, 6),
            background=COLORES["acento_suave"],
            foreground=COLORES["primario"],
            relief="flat",
        )

        style.configure(
            "TEntry",
            font=("Consolas", 11),
            padding=8,
            relief="flat",
        )

    def _crear_widgets(self) -> None:
        """Crea y organiza todos los widgets de la interfaz."""
        main_container = tk.Frame(
            self.root,
            bg=COLORES["fondo"],
            padx=24,
            pady=24,
        )
        main_container.pack(fill=tk.BOTH, expand=True)

        disclaimer_frame = tk.Frame(main_container, bg="#fef3c7", padx=12, pady=8)
        disclaimer_frame.pack(fill=tk.X, pady=(0, 16))

        tk.Label(
            disclaimer_frame,
            text="⚠️ Aviso: Los números generados son ficticios. "
            "Solo para ejercicios educativos. No usar para transacciones ni fines ilegales.",
            font=("Segoe UI", 9),
            fg="#92400e",
            bg="#fef3c7",
            wraplength=500,
            justify=tk.LEFT,
        ).pack(anchor=tk.W)

        header = tk.Frame(main_container, bg=COLORES["fondo"])
        header.pack(fill=tk.X, pady=(0, 16))

        tk.Label(
            header,
            text="💳 Generador Números de Tarjeta",
            font=("Segoe UI", 18, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["fondo"],
        ).pack(anchor=tk.W)

        tk.Label(
            header,
            text="Valida y genera números con algoritmo de Luhn",
            font=("Segoe UI", 10),
            fg=COLORES["texto_secundario"],
            bg=COLORES["fondo"],
        ).pack(anchor=tk.W)

        # --- Card 1: Validar ---
        card1 = self._crear_card(main_container, "Validar número de tarjeta")

        validar_frame = tk.Frame(card1, bg=COLORES["superficie"])
        validar_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            validar_frame,
            text="Número a validar:",
            font=("Segoe UI", 10),
            fg=COLORES["texto"],
            bg=COLORES["superficie"],
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.entry_validar = ttk.Entry(validar_frame, width=24)
        self.entry_validar.pack(side=tk.LEFT, padx=(0, 8))
        self.entry_validar.insert(0, "4532015112830366")
        self.entry_validar.bind("<Return>", lambda e: self._on_validate())

        ttk.Button(
            validar_frame,
            text="Validar",
            style="Secondary.TButton",
            command=self._on_validate,
        ).pack(side=tk.LEFT)

        self.label_validacion = tk.Label(
            card1,
            text="",
            font=("Segoe UI", 10),
            bg=COLORES["superficie"],
        )
        self.label_validacion.pack(anchor=tk.W, pady=(4, 0))

        # --- Card 2: Generar ---
        card2 = self._crear_card(main_container, "Generar número aleatorio")

        gen_frame = tk.Frame(card2, bg=COLORES["superficie"])
        gen_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            gen_frame,
            text="Prefijo BIN:",
            font=("Segoe UI", 10),
            fg=COLORES["texto"],
            bg=COLORES["superficie"],
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.bin_var = tk.StringVar(value="4")
        self.bin_combo = ttk.Combobox(
            gen_frame,
            textvariable=self.bin_var,
            values=list(BIN_PRESETS.keys()),
            width=18,
            state="readonly",
        )
        self.bin_combo.pack(side=tk.LEFT, padx=(0, 8))
        self.bin_combo.bind("<<ComboboxSelected>>", self._on_bin_selected)

        self.bin_entry = ttk.Entry(gen_frame, width=10)
        self.bin_entry.pack(side=tk.LEFT, padx=(0, 8))
        self.bin_entry.insert(0, "4")

        tk.Label(
            gen_frame,
            text="Longitud:",
            font=("Segoe UI", 10),
            fg=COLORES["texto"],
            bg=COLORES["superficie"],
        ).pack(side=tk.LEFT, padx=(16, 8))

        self.length_var = tk.StringVar(value="16")
        ttk.Combobox(
            gen_frame,
            textvariable=self.length_var,
            values=["13", "16", "19"],
            width=5,
            state="readonly",
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Button(
            gen_frame,
            text="Generar y copiar",
            style="Primary.TButton",
            command=self._on_generate,
        ).pack(side=tk.LEFT, padx=(8, 0))

        self.label_resultado = tk.Label(
            card2,
            text="",
            font=("Consolas", 13, "bold"),
            fg=COLORES["primario"],
            bg=COLORES["superficie"],
        )
        self.label_resultado.pack(anchor=tk.W, pady=(4, 0))

        # --- Card 3: Lotes ---
        card3 = self._crear_card(main_container, "Generar por lotes")

        lote_frame = tk.Frame(card3, bg=COLORES["superficie"])
        lote_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(
            lote_frame,
            text="Prefijo BIN:",
            font=("Segoe UI", 10),
            fg=COLORES["texto"],
            bg=COLORES["superficie"],
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.batch_bin = ttk.Entry(lote_frame, width=10)
        self.batch_bin.pack(side=tk.LEFT, padx=(0, 8))
        self.batch_bin.insert(0, "4")

        tk.Label(
            lote_frame,
            text="Cantidad:",
            font=("Segoe UI", 10),
            fg=COLORES["texto"],
            bg=COLORES["superficie"],
        ).pack(side=tk.LEFT, padx=(16, 8))

        self.batch_count = tk.Spinbox(
            lote_frame,
            from_=LOTE_MIN,
            to=LOTE_MAX,
            width=8,
            font=("Consolas", 12),
            justify=tk.CENTER,
        )
        self.batch_count.delete(0, tk.END)
        self.batch_count.insert(0, "10")
        self.batch_count.pack(side=tk.LEFT, padx=(0, 8))
        self.batch_count.bind("<KeyRelease>", self._filtrar_spinbox_lote)

        tk.Label(
            lote_frame,
            text="Longitud:",
            font=("Segoe UI", 10),
            fg=COLORES["texto"],
            bg=COLORES["superficie"],
        ).pack(side=tk.LEFT, padx=(16, 8))

        self.batch_length = ttk.Combobox(
            lote_frame,
            values=["13", "16", "19"],
            width=5,
            state="readonly",
        )
        self.batch_length.set("16")
        self.batch_length.pack(side=tk.LEFT, padx=(0, 8))

        self._btn_generar_lote = ttk.Button(
            lote_frame,
            text="Generar lote",
            style="Primary.TButton",
            command=self._on_batch_generate,
        )
        self._btn_generar_lote.pack(side=tk.LEFT, padx=(8, 8))

        ttk.Button(
            lote_frame,
            text="Copiar todo",
            style="Secondary.TButton",
            command=self._copy_batch,
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Button(
            lote_frame,
            text="Exportar archivo",
            style="Secondary.TButton",
            command=self._export_batch,
        ).pack(side=tk.LEFT, padx=(0, 8))

        ttk.Button(
            lote_frame,
            text="Limpiar",
            style="Secondary.TButton",
            command=self._clear_batch,
        ).pack(side=tk.LEFT)

        sep_frame = tk.Frame(card3, bg=COLORES["superficie"])
        sep_frame.pack(fill=tk.X, pady=(4, 0))

        tk.Label(
            sep_frame,
            text="Formato exportación / unión:",
            font=("Segoe UI", 9),
            fg=COLORES["texto_secundario"],
            bg=COLORES["superficie"],
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.var_separador = tk.StringVar(value="Línea nueva")
        for sep_nombre in SEPARADORES:
            rb = tk.Radiobutton(
                sep_frame,
                text=sep_nombre,
                variable=self.var_separador,
                value=sep_nombre,
                font=("Segoe UI", 9),
                fg=COLORES["texto"],
                bg=COLORES["superficie"],
                selectcolor=COLORES["acento_suave"],
                activebackground=COLORES["superficie"],
            )
            rb.pack(side=tk.LEFT, padx=(0, 12))

        container_texto = tk.Frame(card3, bg=COLORES["superficie"])
        container_texto.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        scrollbar = tk.Scrollbar(container_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.batch_text = tk.Text(
            container_texto,
            height=8,
            font=("Consolas", 10),
            wrap=tk.NONE,
            fg=COLORES["texto"],
            bg="#fafafa",
            relief=tk.FLAT,
            padx=8,
            pady=8,
            yscrollcommand=scrollbar.set,
        )
        self.batch_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.batch_text.yview)

        self.batch_text.insert(tk.END, "Los números generados aparecerán aquí...")
        self.batch_text.config(fg=COLORES["texto_secundario"])

        self.label_status_lote = tk.Label(
            card3,
            text="",
            font=("Segoe UI", 9),
            fg=COLORES["texto_secundario"],
            bg=COLORES["superficie"],
        )
        self.label_status_lote.pack(anchor=tk.W, pady=(4, 0))

        self._generated_batch: list[str] = []

        # --- Footer ---
        footer = tk.Label(
            main_container,
            text="secrets.SystemRandom · Algoritmo de Luhn · Solo uso educativo",
            font=("Segoe UI", 9),
            fg=COLORES["texto_secundario"],
            bg=COLORES["fondo"],
        )
        footer.pack(anchor=tk.W, pady=(16, 0))

    def _crear_card(self, parent: tk.Widget, titulo: str) -> tk.Frame:
        """Crea una tarjeta (card) con título y borde sutil."""
        card = tk.Frame(
            parent,
            bg=COLORES["superficie"],
            highlightbackground=COLORES["borde"],
            highlightthickness=1,
            padx=16,
            pady=16,
        )
        card.pack(fill=tk.X, pady=(0, 16))

        lbl = tk.Label(
            card,
            text=titulo,
            font=("Segoe UI", 11, "bold"),
            fg=COLORES["texto"],
            bg=COLORES["superficie"],
        )
        lbl.pack(anchor=tk.W, pady=(0, 12))

        return card

    def _filtrar_spinbox_lote(self, _event: tk.Event) -> None:
        """Limita el spinbox de cantidad a solo dígitos (máx 5)."""
        contenido = self.batch_count.get()
        nuevo = "".join(c for c in contenido if c.isdigit())[:5]
        if nuevo != contenido:
            self.batch_count.delete(0, tk.END)
            self.batch_count.insert(0, nuevo)

    def _obtener_separador_actual(self) -> str:
        """Devuelve el carácter separador según la selección del usuario."""
        return SEPARADORES.get(self.var_separador.get(), "\n")

    def _on_bin_selected(self, event: tk.Event) -> None:
        """Actualiza el campo BIN según el preset seleccionado."""
        key = self.bin_var.get()
        if key in BIN_PRESETS:
            val = BIN_PRESETS[key]
            self.bin_entry.delete(0, tk.END)
            self.bin_entry.insert(0, val)

    def _on_validate(self) -> None:
        """Ejecuta la validación del número ingresado."""
        number = self.entry_validar.get().strip()
        if not number:
            self._mostrar_error(
                self.label_validacion,
                "Introduce un número a validar.",
            )
            return

        is_valid = validate_luhn(number)
        if is_valid:
            formatted = format_card_number(number)
            if len(formatted) > 50:
                formatted = formatted[:47] + "..."
            self._mostrar_exito(
                self.label_validacion,
                f"✓ Válido según algoritmo de Luhn: {formatted}",
            )
        else:
            self._mostrar_error(
                self.label_validacion,
                "✗ No válido. El número no pasa la validación de Luhn.",
            )

    def _copiar_al_portapapeles(self, texto: str) -> tuple[bool, bool]:
        """
        Copia texto al portapapeles de forma segura.

        Returns:
            Tupla (se_copió_algo, contenido_fue_truncado).
        """
        try:
            if not isinstance(texto, str) or not texto:
                return (False, False)

            texto_final, fue_truncado = truncar_para_clipboard(texto)
            if not texto_final:
                return (False, fue_truncado)

            self.root.clipboard_clear()
            self.root.clipboard_append(texto_final)
            self.root.update()

            if fue_truncado:
                logger.warning("Texto truncado al copiar (límite excedido)")
            return (True, fue_truncado)
        except Exception as e:
            logger.exception("Error al copiar al portapapeles: %s", e)
            return (False, False)

    def _on_generate(self) -> None:
        """Genera un número de tarjeta válido y lo copia."""
        prefix = self.bin_entry.get().strip() or "4"
        try:
            length = int(self.length_var.get())
        except ValueError:
            length = 16
        length = max(13, min(19, length))

        self._last_generated = generate_valid_card_number(prefix, length)
        formatted = format_card_number(self._last_generated)
        copiado, truncado = self._copiar_al_portapapeles(self._last_generated)
        if copiado and not truncado:
            msg = f"{formatted}  ✓ copiado"
        elif copiado and truncado:
            msg = f"{formatted}  ✓ (copiado parcial)"
        else:
            msg = f"{formatted}  ✓"
        self.label_resultado.config(text=msg, fg=COLORES["exito"])

    def _on_batch_generate(self) -> None:
        """Inicia la generación de lote en un hilo secundario."""
        if self._generando_lote:
            return

        try:
            cantidad_str = self.batch_count.get().strip()
            if not cantidad_str:
                self._mostrar_error_lote("Introduce una cantidad.")
                return

            cantidad = int(cantidad_str)
            if not LOTE_MIN <= cantidad <= LOTE_MAX:
                self._mostrar_error_lote(
                    f"La cantidad debe estar entre {LOTE_MIN} y {LOTE_MAX}.",
                )
                return

            prefix = self.batch_bin.get().strip() or "4"
            length = int(self.batch_length.get() or "16")

            self._generando_lote = True
            self._deshabilitar_boton_lote(True)
            self.label_status_lote.config(
                text="⏳ Generando...",
                fg=COLORES["primario"],
            )
            self.batch_text.config(state=tk.NORMAL, fg=COLORES["texto_secundario"])
            self.batch_text.delete(1.0, tk.END)
            self.batch_text.insert(tk.END, "Generando números, por favor espera...")

            def worker() -> None:
                try:
                    batch = [
                        generate_valid_card_number(prefix, length)
                        for _ in range(cantidad)
                    ]
                except Exception as e:
                    logger.exception("Error en generación de lote: %s", e)
                    msg_err = str(e)
                    self.root.after(
                        0,
                        lambda m=msg_err: self._on_lote_worker_terminado_error(m),
                    )
                else:
                    self.root.after(
                        0,
                        lambda b=batch: self._on_lote_worker_terminado_exito(b),
                    )

            threading.Thread(target=worker, daemon=True).start()

        except ValueError as e:
            self._mostrar_error_lote(str(e))
            self._generando_lote = False
            self._deshabilitar_boton_lote(False)

    def _on_lote_worker_terminado_exito(self, batch: list[str]) -> None:
        """Aplica resultado del lote en el hilo principal."""
        self._finalizar_lote(batch)
        self._deshabilitar_boton_lote(False)
        self._generando_lote = False

    def _on_lote_worker_terminado_error(self, mensaje: str) -> None:
        """Muestra error de lote y libera el estado."""
        self._mostrar_error_lote(f"Error: {mensaje}")
        self._deshabilitar_boton_lote(False)
        self._generando_lote = False

    def _finalizar_lote(self, batch: list[str]) -> None:
        """Actualiza la UI con los números generados."""
        self._generated_batch = batch
        separador = self._obtener_separador_actual()
        texto = separador.join(batch)

        self.batch_text.config(fg=COLORES["texto"])
        self.batch_text.delete(1.0, tk.END)
        self.batch_text.insert(tk.END, texto)

        copiado, truncado = self._copiar_al_portapapeles(texto)
        if copiado and not truncado:
            self.label_status_lote.config(
                text=f"✓ {len(batch)} números generados y copiados",
                fg=COLORES["exito"],
            )
        elif copiado and truncado:
            self.label_status_lote.config(
                text=f"✓ {len(batch)} números generados (portapapeles truncado; exporta para el lote completo)",
                fg=COLORES["exito"],
            )
        else:
            self.label_status_lote.config(
                text=f"✓ {len(batch)} números generados (exporta a archivo para copiar todo)",
                fg=COLORES["exito"],
            )

    def _deshabilitar_boton_lote(self, deshabilitar: bool) -> None:
        """Habilita o deshabilita el botón de generar lote."""
        state = "disabled" if deshabilitar else "normal"
        self._btn_generar_lote.config(state=state)

    def _mostrar_error_lote(self, mensaje: str) -> None:
        """Muestra un mensaje de error en el área de lote."""
        self.batch_text.config(state=tk.NORMAL, fg=COLORES["error"])
        self.batch_text.delete(1.0, tk.END)
        self.batch_text.insert(tk.END, mensaje)
        self.label_status_lote.config(text=f"✗ {mensaje}", fg=COLORES["error"])

    def _copy_batch(self) -> None:
        """Copia el contenido actual del área de lote al portapapeles."""
        try:
            contenido = self.batch_text.get(1.0, tk.END).strip()
            if not contenido or "aparecerán aquí" in contenido or "Generando" in contenido:
                self.label_status_lote.config(
                    text="No hay números para copiar",
                    fg=COLORES["error"],
                )
                return

            copiado, truncado = self._copiar_al_portapapeles(contenido)
            if copiado and not truncado:
                self.label_status_lote.config(
                    text="✓ Lote copiado al portapapeles",
                    fg=COLORES["exito"],
                )
            elif copiado and truncado:
                self.label_status_lote.config(
                    text="✓ Copiado truncado. Exporta para el lote completo.",
                    fg=COLORES["exito"],
                )
            else:
                self.label_status_lote.config(
                    text="No se pudo copiar al portapapeles",
                    fg=COLORES["error"],
                )
        except Exception as e:
            logger.exception("Error al copiar lote: %s", e)
            self.label_status_lote.config(
                text="Error al copiar",
                fg=COLORES["error"],
            )

    def _export_batch(self) -> None:
        """Exporta el contenido del lote a un archivo."""
        try:
            contenido = self.batch_text.get(1.0, tk.END).strip()
            if not contenido or "aparecerán aquí" in contenido or "Generando" in contenido:
                messagebox.showwarning(
                    "Sin datos",
                    "No hay números para exportar. Genera un lote primero.",
                )
                return

            default_name = f"card_numbers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Archivo de texto", "*.txt"),
                    ("CSV", "*.csv"),
                    ("Todos los archivos", "*.*"),
                ],
                title="Guardar números",
                initialfile=default_name,
            )

            if path and path.strip():
                path_obj = Path(path).resolve()
                cabecera = (
                    "# Números generados para pruebas - NO SON REALES\n"
                    f"# Solo uso educativo - {APP_NAME}\n"
                    f"# Generado: {datetime.now().isoformat()}\n"
                    "# " + "=" * 50 + "\n\n"
                )
                path_obj.write_text(cabecera + contenido, encoding="utf-8")
                self.label_status_lote.config(
                    text=f"✓ Exportado a {path_obj}",
                    fg=COLORES["exito"],
                )
        except Exception as e:
            logger.exception("Error al exportar: %s", e)
            messagebox.showerror(
                "Error",
                "No se pudo guardar el archivo. Inténtalo de nuevo.",
            )

    def _clear_batch(self) -> None:
        """Limpia el área de resultados del lote."""
        self._generated_batch = []
        self.batch_text.config(fg=COLORES["texto_secundario"])
        self.batch_text.delete(1.0, tk.END)
        self.batch_text.insert(tk.END, "Los números generados aparecerán aquí...")
        self.label_status_lote.config(text="")

    def _mostrar_exito(self, label: tk.Label, mensaje: str) -> None:
        """Muestra un mensaje de éxito en verde."""
        label.config(text=mensaje, fg=COLORES["exito"])

    def _mostrar_error(self, label: tk.Label, mensaje: str) -> None:
        """Muestra un mensaje de error en rojo."""
        label.config(text=mensaje, fg=COLORES["error"])

    def run(self) -> None:
        """Inicia el bucle principal de la aplicación."""
        self.root.mainloop()


def main() -> None:
    """Punto de entrada para la aplicación gráfica."""
    app = CardApp()
    app.run()


if __name__ == "__main__":
    main()

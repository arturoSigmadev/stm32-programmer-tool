# programmer.py - Programador simple para STM32 usando OpenOCD
import subprocess
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class STM32Programmer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("STM32 Programmer Tool")
        self.root.geometry("500x400")

        # Variables
        self.firmware_path = ""
        self.target_device = tk.StringVar(value="stm32g4x")
        self.programmer_type = tk.StringVar(value="stlink")

        self.create_widgets()

    def create_widgets(self):
        # Título
        title_label = tk.Label(self.root, text="STM32 Programmer Tool",
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Selección de archivo de firmware
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(file_frame, text="Archivo de Firmware:").pack(anchor="w")
        self.file_entry = tk.Entry(file_frame, width=50)
        self.file_entry.pack(side="left", padx=(0, 10))
        self.file_entry.config(state="readonly")

        browse_btn = tk.Button(file_frame, text="Buscar", command=self.browse_file)
        browse_btn.pack(side="right")

        # Selección de dispositivo
        device_frame = tk.Frame(self.root)
        device_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(device_frame, text="Dispositivo STM32:").pack(anchor="w")
        device_combo = ttk.Combobox(device_frame, textvariable=self.target_device,
                                   values=["stm32g4x", "stm32f1x", "stm32f4x", "stm32h7x"])
        device_combo.pack(fill="x")

        # Selección de programador
        prog_frame = tk.Frame(self.root)
        prog_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(prog_frame, text="Tipo de Programador:").pack(anchor="w")
        prog_combo = ttk.Combobox(prog_frame, textvariable=self.programmer_type,
                                 values=["stlink", "jlink", "cmsis-dap"])
        prog_combo.pack(fill="x")

        # Botón de programación
        program_btn = tk.Button(self.root, text="Programar Firmware",
                               command=self.start_programming, bg="green", fg="white",
                               font=("Arial", 12, "bold"))
        program_btn.pack(pady=20)

        # Área de progreso
        self.progress_var = tk.StringVar(value="Listo para programar")
        progress_label = tk.Label(self.root, textvariable=self.progress_var,
                                 wraplength=400, justify="center")
        progress_label.pack(pady=10)

        # Barra de progreso
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal",
                                           length=400, mode="indeterminate")
        self.progress_bar.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de firmware",
            filetypes=[("Archivos HEX", "*.hex"), ("Archivos BIN", "*.bin"),
                      ("Todos los archivos", "*.*")]
        )
        if file_path:
            self.firmware_path = file_path
            self.file_entry.config(state="normal")
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, os.path.basename(file_path))
            self.file_entry.config(state="readonly")

    def start_programming(self):
        if not self.firmware_path:
            messagebox.showerror("Error", "Por favor selecciona un archivo de firmware")
            return

        # Deshabilitar botón durante programación
        self.progress_bar.start()
        self.progress_var.set("Programando...")

        # Ejecutar en hilo separado para no bloquear UI
        threading.Thread(target=self.program_firmware, daemon=True).start()

    def program_firmware(self):
        try:
            # Construir comando OpenOCD
            openocd_cmd = self.build_openocd_command()

            self.progress_var.set("Conectando al dispositivo...")

            # Ejecutar OpenOCD
            process = subprocess.Popen(
                openocd_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(self.firmware_path)
            )

            # Leer salida en tiempo real
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.progress_var.set(f"Programando: {output.strip()}")

            # Verificar resultado
            return_code = process.poll()
            if return_code == 0:
                self.progress_var.set("✅ Programación exitosa!")
                messagebox.showinfo("Éxito", "Firmware programado correctamente")
            else:
                stderr = process.stderr.read()
                self.progress_var.set("❌ Error en programación")
                messagebox.showerror("Error", f"Error al programar:\n{stderr}")

        except Exception as e:
            self.progress_var.set("❌ Error inesperado")
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")

        finally:
            self.progress_bar.stop()

    def build_openocd_command(self):
        """Construir comando OpenOCD basado en configuración"""
        base_cmd = ["openocd"]

        # Configurar programador
        if self.programmer_type.get() == "stlink":
            base_cmd.extend(["-f", "interface/stlink.cfg"])
        elif self.programmer_type.get() == "jlink":
            base_cmd.extend(["-f", "interface/jlink.cfg"])
        elif self.programmer_type.get() == "cmsis-dap":
            base_cmd.extend(["-f", "interface/cmsis-dap.cfg"])

        # Configurar dispositivo
        if self.target_device.get() == "stm32g4x":
            base_cmd.extend(["-f", "target/stm32g4x.cfg"])
        elif self.target_device.get() == "stm32f1x":
            base_cmd.extend(["-f", "target/stm32f1x.cfg"])
        elif self.target_device.get() == "stm32f4x":
            base_cmd.extend(["-f", "target/stm32f4x.cfg"])
        elif self.target_device.get() == "stm32h7x":
            base_cmd.extend(["-f", "target/stm32h7x.cfg"])

        # Comando de programación
        firmware_name = os.path.basename(self.firmware_path)
        program_cmd = f"program {firmware_name} verify reset exit"

        base_cmd.extend(["-c", program_cmd])

        return base_cmd

def main():
    app = STM32Programmer()
    app.root.mainloop()

if __name__ == "__main__":
    main()
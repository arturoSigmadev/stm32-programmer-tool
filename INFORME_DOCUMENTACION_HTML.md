# 📚 INFORME COMPLETO: Sistema de Documentación HTML

## 🔍 TAREA 1: ANÁLISIS DEL PROCESO DE COMPILACIÓN

### Hallazgos del Análisis

#### 1. **Estructura de Archivos Descubierta**

```
docs/docs/sw-Stm32Programmer/uqomm_stm32_programer_guide/
├── uqomm_firmware_update_guide_SOURCE.html  ← NUEVO: Archivo fuente editable
├── uqomm_firmware_update_guide.html         ← Archivo HTML final (standalone)
├── embed_images.ps1                          ← Script PowerShell de conversión
├── BUILD_README.md                           ← NUEVO: Documentación del proceso
├── adapt.bat                                 ← Script auxiliar FFmpeg (no usado actualmente)
└── assets/
    ├── 0-debugger.png         ← Imagen del programmer ST-LINK
    ├── 0-debugger_2.png       ← ✨ NUEVA imagen agregada
    ├── 1-init.png             ← Pantalla inicial STM32CubeProgrammer
    ├── 2-select_debugger.png  ← Selección de debugger
    ├── 3-connect.png          ← Conexión al dispositivo
    ├── 4-open_file.png        ← Carga de firmware
    └── 5-download.png         ← Programación y verificación
```

#### 2. **Proceso de Compilación Identificado**

**⚠️ Hallazgo Importante:** El sistema **NO utiliza Markdown** ni generadores como Sphinx, MkDocs o Jekyll.

**Flujo de trabajo:**

```
┌─────────────────────────────────────────┐
│ 1. EDICIÓN MANUAL                       │
│    uqomm_firmware_update_guide_SOURCE.html │
│    (HTML con referencias locales)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 2. CONVERSIÓN DE IMÁGENES               │
│    Script: embed_images.ps1             │
│    • Lee imágenes PNG de assets/        │
│    • Convierte cada imagen a Base64     │
│    • Crea data URIs                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 3. EMBEDDING                            │
│    • Reemplaza src="assets/xxx.png"     │
│    • Por src="data:image/png;base64..." │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 4. ARCHIVO FINAL                        │
│    uqomm_firmware_update_guide.html     │
│    (standalone, ~1MB, incluye todo)     │
└─────────────────────────────────────────┘
```

#### 3. **Detalles Técnicos del Script `embed_images.ps1`**

```powershell
# Paso 1: Define mapeo de imágenes
$images = @{
    "0-debugger" = "assets\0-debugger.png"
    "0-debugger_2" = "assets\0-debugger_2.png"
    # ... más imágenes
}

# Paso 2: Convierte a Base64
foreach ($key in $images.Keys) {
    $imageBytes = [System.IO.File]::ReadAllBytes($imagePath)
    $base64 = [System.Convert]::ToBase64String($imageBytes)
    $base64Images[$key] = "data:image/png;base64,$base64"
}

# Paso 3: Reemplaza en HTML
$htmlContent = $htmlContent -replace 'src="assets/0-debugger\.png"', 
                                      "src=""$($base64Images['0-debugger'])"""

# Paso 4: Guarda archivo final
[System.IO.File]::WriteAllText("uqomm_firmware_update_guide.html", 
                                $htmlContent, $utf8NoBom)
```

---

## ✅ TAREA 2: MODIFICACIÓN DE LA GUÍA

### Cambios Realizados

#### 1. **Imagen Agregada**
- **Archivo:** `assets/0-debugger_2.png` (ya existía en el repositorio)
- **Ubicación:** Sección "Hardware Setup - Programmer Connection" (Paso 3)
- **Propósito:** Mostrar descripción detallada de pines del ST-LINK V2

#### 2. **Contenido HTML Actualizado**

Se agregó en la sección de Hardware Setup:

```html
<p style="margin-top: 10px;"><strong>Pin Description Reference:</strong></p>
<img src="assets/0-debugger_2.png" alt="ST-LINK Pin Description" class="step-image small">

<div class="note" style="margin-top: 15px;">
    <div class="note-title">🔌 Connection Guide</div>
    <p style="margin: 5px 0 0;">
        • <strong>RST</strong> (Pin 1-2): Reset line - connects to target NRST<br>
        • <strong>SWDIO</strong> (Pin 2): Serial Wire Debug I/O - bidirectional data<br>
        • <strong>GND</strong> (Pin 3-4): Ground reference - must be common<br>
        • <strong>SWCLK</strong> (Pin 5-6): Serial Wire Clock<br>
        • <strong>3.3V/5.0V</strong> (Pin 7-8-10): Power supply (verify target voltage!)
    </p>
</div>

<div class="alert" style="margin-top: 15px;">
    <div class="alert-title">⚡ Important Safety Notes</div>
    <p style="margin: 5px 0 0;">
        1. <strong>Power OFF</strong> the target device before connecting the programmer<br>
        2. Verify voltage compatibility (3.3V vs 5.0V) before connecting power<br>
        3. Double-check all pin connections - incorrect wiring can permanently damage the device<br>
        4. Only power ON after all connections are verified
    </p>
</div>
```

#### 3. **Script `embed_images.ps1` Actualizado**

```powershell
# Agregada nueva imagen al diccionario
$images = @{
    "0-debugger" = "assets\0-debugger.png"
    "0-debugger_2" = "assets\0-debugger_2.png"  # ← NUEVA
    "1-init" = "assets\1-init.png"
    # ... resto de imágenes
}

# Agregado nuevo reemplazo
$htmlContent = $htmlContent -replace 'src="assets/0-debugger_2\.png"', 
                                      "src=""$($base64Images['0-debugger_2'])"""

# Corregido nombre del archivo fuente
$htmlContent = [System.IO.File]::ReadAllText("uqomm_firmware_update_guide_SOURCE.html", 
                                               [System.Text.Encoding]::UTF8)

# Corregido nombre del archivo de salida
$outputFile = "uqomm_firmware_update_guide.html"
```

#### 4. **Nuevos Archivos Creados**

1. **`uqomm_firmware_update_guide_SOURCE.html`**
   - Archivo fuente editable
   - Contiene referencias a imágenes locales
   - Incluye la nueva imagen `0-debugger_2.png`
   - HTML limpio y mantenible

2. **`BUILD_README.md`**
   - Documentación completa del proceso de compilación
   - Instrucciones paso a paso
   - Workflow claramente definido
   - Notas importantes y mejores prácticas

---

## 🚀 COMANDO PARA RECONSTRUIR EL HTML

### Opción 1: Ejecutar directamente (requiere cambiar política de ejecución)

```powershell
cd docs\docs\sw-Stm32Programmer\uqomm_stm32_programer_guide
.\embed_images.ps1
```

### Opción 2: Bypass de política de ejecución (recomendado)

```powershell
cd docs\docs\sw-Stm32Programmer\uqomm_stm32_programer_guide
powershell -ExecutionPolicy Bypass -File embed_images.ps1
```

### Salida Esperada

```
Converting images to Base64...
  Converted: assets\0-debugger.png
  Converted: assets\0-debugger_2.png
  Converted: assets\1-init.png
  Converted: assets\2-select_debugger.png
  Converted: assets\3-connect.png
  Converted: assets\4-open_file.png
  Converted: assets\5-download.png

Standalone HTML created: uqomm_firmware_update_guide.html
File size: 0.98 MB

You can now share this single file - no assets folder needed!
```

---

## 📝 WORKFLOW COMPLETO PARA FUTURAS MODIFICACIONES

### Paso 1: Editar el Archivo Fuente
```powershell
# Abrir en tu editor preferido
code uqomm_firmware_update_guide_SOURCE.html
```

### Paso 2: Agregar/Actualizar Imágenes (si es necesario)
```powershell
# Copiar nuevas imágenes PNG a la carpeta assets/
copy nueva-imagen.png assets\
```

### Paso 3: Actualizar Script (solo si agregaste nuevas imágenes)
```powershell
# Editar embed_images.ps1
# Agregar nueva entrada al diccionario $images
# Agregar nueva línea de reemplazo
```

### Paso 4: Compilar HTML Final
```powershell
powershell -ExecutionPolicy Bypass -File embed_images.ps1
```

### Paso 5: Verificar Resultado
```powershell
# Abrir en navegador
start uqomm_firmware_update_guide.html
```

### Paso 6: Commit a Git
```powershell
# Dentro del submodule docs
git add BUILD_README.md uqomm_firmware_update_guide_SOURCE.html uqomm_firmware_update_guide.html embed_images.ps1
git commit -m "Update programming guide: [descripción de cambios]"

# En el repositorio principal
cd ../../..
git add docs
git commit -m "Update docs submodule: [descripción de cambios]"
```

---

## 📊 RESUMEN DE CAMBIOS REALIZADOS

### Archivos Modificados
- ✅ `embed_images.ps1` - Script actualizado para incluir nueva imagen
- ✅ `uqomm_firmware_update_guide.html` - HTML final regenerado con nueva imagen

### Archivos Creados
- ✅ `uqomm_firmware_update_guide_SOURCE.html` - Archivo fuente editable
- ✅ `BUILD_README.md` - Documentación del proceso de compilación

### Commits Realizados
1. **En submodule docs:**
   - `6d912ec` - "Add 0-debugger_2.png image to Hardware Setup section with build process documentation"

2. **En repositorio principal:**
   - `7e56990` - "Update docs submodule: Add debugger pin description image to programming guide"

---

## ⚠️ NOTAS IMPORTANTES

1. **NUNCA edites directamente** `uqomm_firmware_update_guide.html` 
   - Todos los cambios se perderán al regenerar el archivo

2. **SIEMPRE edita** `uqomm_firmware_update_guide_SOURCE.html`
   - Este es el archivo fuente de verdad

3. **Tamaño del archivo final**
   - ~980KB debido a imágenes Base64 embebidas
   - Ideal para distribución (no requiere carpeta assets)

4. **Formato de imágenes**
   - Solo PNG es soportado actualmente
   - Para JPG, modificar el tipo MIME en el script

---

## 📧 SOPORTE

Para preguntas técnicas sobre este sistema:
- Revisar `BUILD_README.md` en la carpeta de la guía
- Consultar este documento
- Contactar al equipo de documentación

---

**Fecha de creación:** 24 de Noviembre de 2025  
**Versión del documento:** 1.0  
**Autor:** GitHub Copilot (Claude Sonnet 4.5)

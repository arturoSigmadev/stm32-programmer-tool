# 📦 Paquete de Programación UQOMM - STM32

## 🎯 Contenido del Paquete

Este paquete contiene todo lo necesario para programar dispositivos UQOMM:

### 1️⃣ Herramienta de Programación STM32
- **Ubicación:** `dist/STM32_Programmer_Portable.zip`
- **Descripción:** Herramienta automática para programar firmware
- **Modo de uso:** Extraer y ejecutar `STM32_Programmer.exe`

### 2️⃣ STM32CubeProgrammer (Oficial)
- **Ubicación:** `uqomm_stm32_programer_guide/stm32cubeprg-win64-v2-20-0.zip`
- **Descripción:** Software oficial de STMicroelectronics
- **Modo de uso:** Instalar antes de usar la herramienta

### 3️⃣ Guía de Usuario HTML
- **Ubicación:** `uqomm_stm32_programer_guide/stm32_firmware_guide_standalone.html`
- **Descripción:** Manual interactivo con imágenes paso a paso
- **Modo de uso:** Abrir con cualquier navegador web

### 4️⃣ Documentación Técnica
- **Ubicación:** `docs/`
- **Contenido:**
  - Manual de usuario completo
  - Lista de elementos necesarios
  - Alternativas de programadores

---

## 🚀 Inicio Rápido

### Para Usuarios Nuevos:

1. **Instalar STM32CubeProgrammer:**
   - Abrir `uqomm_stm32_programer_guide/stm32cubeprg-win64-v2-20-0.zip`
   - Ejecutar el instalador
   - Seguir las instrucciones

2. **Abrir la Guía HTML:**
   - Doble clic en `uqomm_stm32_programer_guide/stm32_firmware_guide_standalone.html`
   - Seguir paso a paso las instrucciones

3. **Usar la Herramienta (Opcional):**
   - Extraer `dist/STM32_Programmer_Portable.zip`
   - Ejecutar `STM32_Programmer.exe`
   - Seleccionar firmware y programar

### Para Usuarios Experimentados:

- **Método Rápido:** Usar STM32CubeProgrammer directamente
- **Método Automático:** Usar `STM32_Programmer.exe` para programación automatizada

---

## 📋 Requisitos

- ✅ **Windows 10/11** (64-bit)
- ✅ **Programador ST-LINK V2+** o compatible
- ✅ **Cable USB** tipo A a Mini-B
- ✅ **Dispositivo UQOMM** a programar
- ✅ **Archivo de firmware** (.hex o .bin) con número serial correspondiente

---

## ⚠️ Notas Importantes

### Sobre el Firmware:
- **Cada binario contiene el número serial del producto** al que se le carga
- **Verificar que el firmware corresponda al dispositivo** antes de programar
- **No intercambiar firmwares** entre diferentes dispositivos

### Sobre la Conexión:
- **El equipo debe estar desenergizado** al conectar el programador
- **Conectar primero el programador al PC**, luego al dispositivo
- **Verificar las conexiones SWD** (SWDIO, SWCLK, GND, 3.3V)

### Durante la Programación:
- **No desconectar** el programador durante el proceso
- **No interrumpir** la alimentación del dispositivo
- **Esperar** a que se complete la verificación

---

## 📞 Soporte Técnico

### En caso de problemas:

1. **Revisar la Guía HTML** - Tiene soluciones a problemas comunes
2. **Verificar las conexiones** - El 90% de errores son de conexión
3. **Instalar drivers** - [ST-LINK Drivers](https://www.st.com/en/development-tools/stsw-link009.html)
4. **Contactar soporte** - Con capturas de pantalla y mensaje de error exacto

### Información útil para soporte:
- Versión de Windows
- Modelo del programador ST-LINK
- Número de serie del dispositivo UQOMM
- Mensaje de error completo

---

## 📄 Estructura del Paquete

```
sw-Stm32Programmer/
├── dist/
│   ├── STM32_Programmer.exe              # Herramienta portable
│   └── STM32_Programmer_Portable.zip     # Paquete completo
├── uqomm_stm32_programer_guide/
│   ├── stm32_firmware_guide_standalone.html  # Guía interactiva ⭐
│   ├── stm32cubeprg-win64-v2-20-0.zip       # Software oficial ⭐
│   └── assets/                               # Imágenes de la guía
├── docs/
│   ├── manual_usuario.md                 # Manual detallado
│   ├── elementos_necesarios.md           # Lista de requisitos
│   └── alternativas_programadores.md     # Opciones de programadores
├── INSTALAR.bat                          # Instalador automático
├── README.md                             # Información técnica
├── GUIA_INSTALACION_CLIENTE.md          # Guía de instalación
└── LEEME_CLIENTE.md                     # Este archivo ⭐
```

---

## ✅ Lista de Verificación Pre-Programación

Antes de programar, verifica:

- [ ] STM32CubeProgrammer instalado
- [ ] Programador ST-LINK conectado al PC
- [ ] Drivers ST-LINK instalados
- [ ] Dispositivo UQOMM desenergizado
- [ ] Conexiones SWD verificadas
- [ ] Firmware correcto para el número serial
- [ ] Guía HTML abierta como referencia

---

## 🎓 Recursos Adicionales

- **Guía HTML:** `uqomm_stm32_programer_guide/stm32_firmware_guide_standalone.html`
- **Manual PDF:** Exportar desde la guía HTML (Ctrl+P → Guardar como PDF)
- **Documentación ST:** https://www.st.com/en/development-tools/stm32cubeprog.html

---

**UQOMM - Underground Communication Systems**  
*Más de 30 años de excelencia en soluciones digitales mineras*

**Versión del Paquete:** 1.0  
**Fecha:** Noviembre 2025

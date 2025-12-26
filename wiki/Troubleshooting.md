# Troubleshooting Guide

[English](#english) | [Español](#español)

---

<a name="english"></a>
## 🇬🇧 English

### Common Issues

#### GUI Won't Launch

**Symptom:** Error when running `python gui.py`

**Solutions:**
1. Verify Tkinter is installed:
   ```bash
   python -m tkinter
   ```
   A window should appear.

2. If Tkinter is missing:
   - **Linux:** `sudo apt install python3-tk`
   - **macOS:** Reinstall Python from python.org
   - **Windows:** Tkinter comes with Python

#### Emulator Not Found

**Symptom:** `ERROR: QEMU not found` or similar

**Solutions:**
1. Install the emulator (see [Installation](Installation))
2. Update `config.json` with correct path:
   ```json
   {
     "emulators": {
       "qemu": {
         "path": "/usr/bin/qemu-system-x86_64"
       }
     }
   }
   ```
3. Verify path: `which qemu-system-x86_64` (Linux/Mac)

#### No Serial Output

**Symptom:** Emulators run but no output captured

**Solutions:**
1. Verify kernel outputs to serial:
   ```c
   // In kernel code
   outb(0x3F8, 'A');  // Write to COM1
   ```

2. Check kernel is configured for serial output

3. Increase timeout in case kernel takes longer to boot

#### Analysis Hangs

**Symptom:** Neuro-Probe never completes

**Solutions:**
1. Increase timeout: `--timeout 30`
2. Check if kernel has infinite loop
3. Verify kernel doesn't wait for user input
4. Try with simpler kernel first

#### Permission Denied

**Symptom:** `Permission denied` when accessing image file

**Solutions:**
- **Linux/Mac:** `chmod +r kernel.img`
- **Windows:** Run as Administrator (if necessary)
- Check file is not locked by another program

#### VirtualBox VM Creation Fails

**Symptom:** Error creating/configuring VM

**Solutions:**
1. Close VirtualBox GUI if open
2. Delete existing test VM:
   ```bash
   VBoxManage unregistervm "Neuro-Probe-Test" --delete
   ```
3. Run Neuro-Probe again

### Performance Issues

#### Slow Analysis

**Cause:** Large timeout or slow emulators

**Solutions:**
- Reduce timeout to minimum needed
- Use fewer emulators
- Upgrade hardware (faster CPU/SSD)

#### High Memory Usage

**Cause:** Multiple emulators running simultaneously

**Solutions:**
- Run emulators sequentially (modify code)
- Reduce number of emulators
- Close other applications

### Report Issues

#### Can't Export JSON

**Symptom:** Error saving report

**Solutions:**
- Check write permissions in output directory
- Specify absolute path
- Ensure disk has free space

#### HTML Report Doesn't Open

**Symptom:** Browser shows error

**Solutions:**
- Use modern browser (Chrome, Firefox, Edge)
- Check HTML file isn't corrupted
- Regenerate report

### Getting Help

If issue persists:

1. Check [FAQ](FAQ)
2. Search existing [GitHub Issues](https://github.com/cyberenigma-lgtm/neuro-probe/issues)
3. Create new issue with:
   - OS and version
   - Python version
   - Complete error message
   - Steps to reproduce

---

<a name="español"></a>
## 🇪🇸 Español

### Problemas Comunes

#### La GUI no se Lanza

**Síntoma:** Error al ejecutar `python gui.py`

**Soluciones:**
1. Verifica que Tkinter esté instalado:
   ```bash
   python -m tkinter
   ```
   Debe aparecer una ventana.

2. Si Tkinter falta:
   - **Linux:** `sudo apt install python3-tk`
   - **macOS:** Reinstala Python desde python.org
   - **Windows:** Tkinter viene con Python

#### Emulador no Encontrado

**Síntoma:** `ERROR: QEMU not found` o similar

**Soluciones:**
1. Instala el emulador (ve [Instalación](Instalacion))
2. Actualiza `config.json` con la ruta correcta:
   ```json
   {
     "emulators": {
       "qemu": {
         "path": "/usr/bin/qemu-system-x86_64"
       }
     }
   }
   ```
3. Verifica ruta: `which qemu-system-x86_64` (Linux/Mac)

#### Sin Salida Serial

**Síntoma:** Los emuladores corren pero no se captura salida

**Soluciones:**
1. Verifica que el kernel envíe salida a serial:
   ```c
   // En código del kernel
   outb(0x3F8, 'A');  // Escribir a COM1
   ```

2. Verifica que el kernel esté configurado para salida serial

3. Incrementa timeout en caso de que el kernel tarde más en arrancar

#### El Análisis se Cuelga

**Síntoma:** Neuro-Probe nunca completa

**Soluciones:**
1. Incrementa timeout: `--timeout 30`
2. Verifica si el kernel tiene bucle infinito
3. Verifica que el kernel no espera entrada del usuario
4. Prueba primero con un kernel más simple

#### Permiso Denegado

**Síntoma:** `Permission denied` al acceder archivo de imagen

**Soluciones:**
- **Linux/Mac:** `chmod +r kernel.img`
- **Windows:** Ejecutar como Administrador (si es necesario)
- Verifica que el archivo no esté bloqueado por otro programa

#### Falla Creación de VM en VirtualBox

**Síntoma:** Error creando/configurando VM

**Soluciones:**
1. Cierra la GUI de VirtualBox si está abierta
2. Elimina VM de prueba existente:
   ```bash
   VBoxManage unregistervm "Neuro-Probe-Test" --delete
   ```
3. Ejecuta Neuro-Probe de nuevo

### Problemas de Rendimiento

#### Análisis Lento

**Causa:** Timeout grande o emuladores lentos

**Soluciones:**
- Reduce timeout al mínimo necesario
- Usa menos emuladores
- Mejora hardware (CPU/SSD más rápido)

#### Alto Uso de Memoria

**Causa:** Múltiples emuladores corriendo simultáneamente

**Soluciones:**
- Ejecuta emuladores secuencialmente (modifica código)
- Reduce número de emuladores
- Cierra otras aplicaciones

### Problemas de Reportes

#### No se Puede Exportar JSON

**Síntoma:** Error al guardar reporte

**Soluciones:**
- Verifica permisos de escritura en directorio de salida
- Especifica ruta absoluta
- Asegúrate de que el disco tenga espacio libre

#### El Reporte HTML no Abre

**Síntoma:** Navegador muestra error

**Soluciones:**
- Usa navegador moderno (Chrome, Firefox, Edge)
- Verifica que archivo HTML no esté corrupto
- Regenera reporte

### Obtener Ayuda

Si el problema persiste:

1. Revisa [FAQ](Preguntas-Frecuentes)
2. Busca en [GitHub Issues](https://github.com/cyberenigma-lgtm/neuro-probe/issues) existentes
3. Crea nuevo issue con:
   - SO y versión
   - Versión de Python
   - Mensaje de error completo
   - Pasos para reproducir

---

**[← Back to Home](Home)**

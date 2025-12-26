# Quick Start Guide

[English](#english) | [Español](#español)

---

<a name="english"></a>
## 🇬🇧 English

### Your First Analysis in 3 Steps

#### Step 1: Launch Neuro-Probe

```bash
python neuro-probe.py
```

Choose your interface:
- `[1]` for GUI (recommended for beginners)
- `[2]` for CLI (for automation)

#### Step 2: Configure Analysis

**GUI Mode:**
1. Click "Browse" and select your `kernel.img`
2. Check emulators you want to test (QEMU, VirtualBox)
3. Set timeout (default: 5 seconds)
4. Click "RUN"

**CLI Mode:**
```bash
python probe.py --image /path/to/kernel.img
```

#### Step 3: Review Results

**GUI:**
- Check "Console" tab for execution log
- Check "Comparison" tab for emulator outputs
- Check "Divergences" tab for differences

**CLI:**
- See terminal output with color-coded results
- Export JSON: `--output report.json`

### Example: Testing Neuro-OS Kernel

```bash
# Using CLI
python probe.py \
  --image ~/kernels/neuro-os.img \
  --emulators qemu,virtualbox \
  --timeout 10 \
  --output neuro-os-test.json

# Results
>> Starting Neuro-Probe analysis...
OK QEMU completed
OK VirtualBox completed
>> No divergences - identical behavior
```

### Understanding the Output

**Green markers:** Execution points reached  
**Red markers:** Divergence detected  
**Serial output:** What the kernel printed  
**Divergences:** Where emulators behaved differently  

### Common First-Time Issues

**Issue:** "Image not found"  
**Fix:** Use absolute path or verify file exists

**Issue:** "No emulators configured"  
**Fix:** Select at least one emulator checkbox

**Issue:** "QEMU not found"  
**Fix:** Update path in `config.json`

---

<a name="español"></a>
## 🇪🇸 Español

### Tu Primer Análisis en 3 Pasos

#### Paso 1: Lanzar Neuro-Probe

```bash
python neuro-probe.py
```

Elige tu interfaz:
- `[1]` para GUI (recomendado para principiantes)
- `[2]` para CLI (para automatización)

#### Paso 2: Configurar Análisis

**Modo GUI:**
1. Click "Browse" y selecciona tu `kernel.img`
2. Marca los emuladores que quieres probar (QEMU, VirtualBox)
3. Establece timeout (por defecto: 5 segundos)
4. Click "RUN"

**Modo CLI:**
```bash
python probe.py --image /ruta/a/kernel.img
```

#### Paso 3: Revisar Resultados

**GUI:**
- Revisa pestaña "Console" para log de ejecución
- Revisa pestaña "Comparison" para salidas de emuladores
- Revisa pestaña "Divergences" para diferencias

**CLI:**
- Ve la salida en terminal con resultados coloreados
- Exporta JSON: `--output reporte.json`

### Ejemplo: Probando Kernel Neuro-OS

```bash
# Usando CLI
python probe.py \
  --image ~/kernels/neuro-os.img \
  --emulators qemu,virtualbox \
  --timeout 10 \
  --output neuro-os-test.json

# Resultados
>> Iniciando análisis Neuro-Probe...
OK QEMU completado
OK VirtualBox completado
>> Sin divergencias - comportamiento idéntico
```

### Entendiendo la Salida

**Marcadores verdes:** Puntos de ejecución alcanzados  
**Marcadores rojos:** Divergencia detectada  
**Salida serial:** Lo que el kernel imprimió  
**Divergencias:** Donde los emuladores se comportaron diferente  

### Problemas Comunes Iniciales

**Problema:** "Imagen no encontrada"  
**Solución:** Usa ruta absoluta o verifica que el archivo existe

**Problema:** "No hay emuladores configurados"  
**Solución:** Selecciona al menos un checkbox de emulador

**Problema:** "QEMU no encontrado"  
**Solución:** Actualiza la ruta en `config.json`

---

**Next:** [CLI Guide →](CLI-Guide) | [GUI Guide →](GUI-Guide)

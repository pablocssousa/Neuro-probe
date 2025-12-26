# Neuro-Probe - Quick Start Guide

## Installation

No installation needed! Just Python 3.7+

```bash
cd neuro-tools/neuro-probe
```

## Quick Start

### Option 1: Launcher (Recommended)
```bash
python neuro-probe.py
```

Choose:
- **[1] GUI** - Graphical interface
- **[2] CLI** - Command line

### Option 2: Direct GUI
```bash
python gui.py
```

### Option 3: Direct CLI
```bash
python probe.py --image /path/to/kernel.img
```

## Usage Examples

### CLI Examples

**Basic analysis:**
```bash
python probe.py --image kernel.img
```

**With timeout:**
```bash
python probe.py --image kernel.img --timeout 10
```

**Export JSON:**
```bash
python probe.py --image kernel.img --output report.json
```

**Specific emulators:**
```bash
python probe.py --image kernel.img --emulators qemu,virtualbox
```

### GUI Usage

1. Launch: `python gui.py`
2. Click "Browse" to select kernel image
3. Select emulators (checkboxes)
4. Click "RUN"
5. View results in tabs
6. Export JSON or HTML

## Features

✅ QEMU support  
✅ VirtualBox support  
✅ Serial output capture  
✅ Divergence detection  
✅ Visual comparison  
✅ JSON/HTML export  
✅ Zero dependencies  

## Requirements

- Python 3.7+
- QEMU (optional)
- VirtualBox (optional)

## Troubleshooting

**GUI doesn't launch:**
- Check Tkinter: `python -m tkinter`

**Emulator not found:**
- Update paths in `config.json`

**No output:**
- Check kernel image exists
- Verify emulator paths

## Next Steps

- See `README.md` for full documentation
- Check `GUI_FEATURES.md` for GUI details
- Review `config.json` for configuration

## Support

Created by José Manuel Moreno Cano  
Project: Neuro-OS Genesis  
Tool: Neuro-Probe v1.0.0

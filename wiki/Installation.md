# Installation Guide

[English](#english) | [Español](#español)

---

<a name="english"></a>
## 🇬🇧 English

### Requirements

**Minimum:**
- Python 3.7+
- 50 MB free disk space

**Optional (for emulator testing):**
- QEMU
- VirtualBox
- Bochs

### Installation Steps

#### 1. Clone Repository

```bash
git clone https://github.com/cyberenigma-lgtm/neuro-probe
cd neuro-probe
```

#### 2. Verify Installation

```bash
python --version
# Should show Python 3.7 or higher
```

#### 3. Test Neuro-Probe

```bash
python neuro-probe.py
```

That's it! No dependencies to install.

### Platform-Specific Notes

#### Windows

Use the provided batch launcher:
```bash
neuro-probe.bat
```

#### Linux/macOS

Make the script executable:
```bash
chmod +x neuro-probe.sh
./neuro-probe.sh
```

### Emulator Configuration

#### QEMU

**Linux:**
```bash
sudo apt install qemu-system-x86
```

**Windows:**
Download from [qemu.org](https://www.qemu.org/download/)

**macOS:**
```bash
brew install qemu
```

#### VirtualBox

Download from [virtualbox.org](https://www.virtualbox.org/)

Update `config.json` with installation path:
```json
{
  "emulators": {
    "virtualbox": {
      "path": "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
    }
  }
}
```

### Verification

```bash
# Test CLI
python probe.py --help

# Test GUI
python gui.py
```

---

<a name="español"></a>
## 🇪🇸 Español

### Requisitos

**Mínimos:**
- Python 3.7+
- 50 MB de espacio libre

**Opcionales (para testing de emuladores):**
- QEMU
- VirtualBox
- Bochs

### Pasos de Instalación

#### 1. Clonar Repositorio

```bash
git clone https://github.com/cyberenigma-lgtm/neuro-probe
cd neuro-probe
```

#### 2. Verificar Instalación

```bash
python --version
# Debe mostrar Python 3.7 o superior
```

#### 3. Probar Neuro-Probe

```bash
python neuro-probe.py
```

¡Eso es todo! No hay dependencias que instalar.

### Notas Específicas por Plataforma

#### Windows

Usa el launcher batch incluido:
```bash
neuro-probe.bat
```

#### Linux/macOS

Haz el script ejecutable:
```bash
chmod +x neuro-probe.sh
./neuro-probe.sh
```

### Configuración de Emuladores

#### QEMU

**Linux:**
```bash
sudo apt install qemu-system-x86
```

**Windows:**
Descarga desde [qemu.org](https://www.qemu.org/download/)

**macOS:**
```bash
brew install qemu
```

#### VirtualBox

Descarga desde [virtualbox.org](https://www.virtualbox.org/)

Actualiza `config.json` con la ruta de instalación:
```json
{
  "emulators": {
    "virtualbox": {
      "path": "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe"
    }
  }
}
```

### Verificación

```bash
# Probar CLI
python probe.py --help

# Probar GUI
python gui.py
```

---

**Next:** [Quick Start Guide →](Quick-Start)

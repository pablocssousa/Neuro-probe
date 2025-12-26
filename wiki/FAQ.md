# FAQ - Frequently Asked Questions

[English](#english) | [Español](#español)

---

<a name="english"></a>
## 🇬🇧 English

### General Questions

**Q: What does Neuro-Probe do?**  
A: Neuro-Probe runs your OS kernel in multiple emulators simultaneously, captures their output, and automatically detects behavioral differences.

**Q: Why would I need this?**  
A: Different emulators behave differently. A bug might appear in QEMU but not VirtualBox, or vice versa. Neuro-Probe finds these differences automatically, saving hours of manual testing.

**Q: Is it free?**  
A: Yes! Neuro-Probe is open source under MIT license.

**Q: Does it require external dependencies?**  
A: No. Neuro-Probe uses only Python standard library. The emulators themselves (QEMU, VirtualBox) are optional.

### Technical Questions

**Q: Which emulators are supported?**  
A: Currently QEMU and VirtualBox fully supported. Bochs support is planned.

**Q: Can I test on real hardware?**  
A: Not yet, but it's on the roadmap for v1.2.

**Q: What file formats are supported?**  
A: Raw disk images (`.img`), ISO images (`.iso`).

**Q: How does divergence detection work?**  
A: Neuro-Probe captures serial output from each emulator and compares them marker-by-marker. Any difference in output, timing, or execution flow is flagged.

**Q: Can I customize the serial markers?**  
A: Yes, edit `config.json` and modify the `markers` field.

### Usage Questions

**Q: Which is better, CLI or GUI?**  
A: GUI is better for learning and one-off tests. CLI is better for automation and CI/CD.

**Q: Can I run Neuro-Probe in my CI/CD pipeline?**  
A: Yes! Use CLI mode with `--output` for JSON reports that can be parsed.

**Q: How long does an analysis take?**  
A: Typically 30 seconds to 2 minutes, depending on your timeout setting.

**Q: Can I test multiple kernels?**  
A: Yes, run Neuro-Probe multiple times or create a batch script.

### Troubleshooting

**Q: GUI doesn't launch**  
A: Verify Tkinter is installed: `python -m tkinter`

**Q: Emulator not found**  
A: Update paths in `config.json` to point to your emulator executables.

**Q: No serial output captured**  
A: Ensure your kernel outputs to serial port (usually COM1/ttyS0).

**Q: Analysis hangs**  
A: Increase timeout or check if your kernel has an infinite loop.

### Development

**Q: Can I contribute?**  
A: Absolutely! See [Contributing](Contributing) guide.

**Q: How do I add support for another emulator?**  
A: Create a new class in `emulators/` inheriting from `Emulator` base class.

**Q: Is there an API?**  
A: Yes, see [API Reference](API-Reference).

**Q: Can I use Neuro-Probe as a library?**  
A: Yes:
```python
from probe import NeuroProbe
probe = NeuroProbe()
probe.setup_emulators("kernel.img")
probe.run_tests()
```

---

<a name="español"></a>
## 🇪🇸 Español

### Preguntas Generales

**P: ¿Qué hace Neuro-Probe?**  
R: Neuro-Probe ejecuta tu kernel en múltiples emuladores simultáneamente, captura su salida y detecta automáticamente diferencias de comportamiento.

**P: ¿Por qué necesitaría esto?**  
R: Diferentes emuladores se comportan diferente. Un bug podría aparecer en QEMU pero no en VirtualBox, o viceversa. Neuro-Probe encuentra estas diferencias automáticamente, ahorrando horas de testing manual.

**P: ¿Es gratis?**  
R: ¡Sí! Neuro-Probe es código abierto bajo licencia MIT.

**P: ¿Requiere dependencias externas?**  
R: No. Neuro-Probe usa solo la biblioteca estándar de Python. Los emuladores mismos (QEMU, VirtualBox) son opcionales.

### Preguntas Técnicas

**P: ¿Qué emuladores están soportados?**  
R: Actualmente QEMU y VirtualBox completamente soportados. Soporte para Bochs está planeado.

**P: ¿Puedo probar en hardware real?**  
R: Aún no, pero está en la hoja de ruta para v1.2.

**P: ¿Qué formatos de archivo están soportados?**  
R: Imágenes de disco raw (`.img`), imágenes ISO (`.iso`).

**P: ¿Cómo funciona la detección de divergencias?**  
R: Neuro-Probe captura la salida serial de cada emulador y las compara marcador por marcador. Cualquier diferencia en salida, timing o flujo de ejecución se marca.

**P: ¿Puedo personalizar los markers seriales?**  
R: Sí, edita `config.json` y modifica el campo `markers`.

### Preguntas de Uso

**P: ¿Qué es mejor, CLI o GUI?**  
R: GUI es mejor para aprender y pruebas ocasionales. CLI es mejor para automatización y CI/CD.

**P: ¿Puedo ejecutar Neuro-Probe en mi pipeline CI/CD?**  
R: ¡Sí! Usa modo CLI con `--output` para reportes JSON que pueden parsearse.

**P: ¿Cuánto tarda un análisis?**  
R: Típicamente 30 segundos a 2 minutos, dependiendo de tu configuración de timeout.

**P: ¿Puedo probar múltiples kernels?**  
R: Sí, ejecuta Neuro-Probe varias veces o crea un script batch.

### Solución de Problemas

**P: La GUI no se lanza**  
R: Verifica que Tkinter esté instalado: `python -m tkinter`

**P: Emulador no encontrado**  
R: Actualiza las rutas en `config.json` para apuntar a tus ejecutables de emulador.

**P: No se captura salida serial**  
R: Asegúrate de que tu kernel envía salida al puerto serial (usualmente COM1/ttyS0).

**P: El análisis se cuelga**  
R: Incrementa el timeout o verifica si tu kernel tiene un bucle infinito.

### Desarrollo

**P: ¿Puedo contribuir?**  
R: ¡Absolutamente! Ve la guía de [Contribución](Contribuir).

**P: ¿Cómo agrego soporte para otro emulador?**  
R: Crea una nueva clase en `emulators/` heredando de la clase base `Emulator`.

**P: ¿Hay una API?**  
R: Sí, ve [Referencia API](Referencia-API).

**P: ¿Puedo usar Neuro-Probe como librería?**  
R: Sí:
```python
from probe import NeuroProbe
probe = NeuroProbe()
probe.setup_emulators("kernel.img")
probe.run_tests()
```

---

**[← Back to Home](Home)**

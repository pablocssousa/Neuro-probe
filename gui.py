"""
Neuro-Probe GUI - Interfaz Gráfica Completa
Integración completa con el core de Neuro-Probe
"""

import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import threading
import json
from pathlib import Path
from datetime import datetime

from probe import NeuroProbe


class NeuroProbeGUI:
    """GUI completa para Neuro-Probe"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Neuro-Probe - Emulator Analysis Tool")
        self.root.geometry("1200x800")
        
        # Variables
        self.kernel_path = tk.StringVar()
        self.qemu_enabled = tk.BooleanVar(value=True)
        self.vbox_enabled = tk.BooleanVar(value=True)
        self.bochs_enabled = tk.BooleanVar(value=False)
        self.timeout = tk.IntVar(value=5)
        self.status = tk.StringVar(value="Ready")
        
        # Results storage
        self.last_results = None
        self.last_divergences = None
        
        self.build_ui()
    
    def build_ui(self):
        """Construye la interfaz completa"""
        # Top toolbar
        self.create_toolbar()
        
        # Main content area
        main_frame = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Configuration
        left_panel = tk.Frame(main_frame, width=300, bg="#f0f0f0")
        main_frame.add(left_panel)
        self.create_config_panel(left_panel)
        
        # Right panel - Results
        right_panel = tk.Frame(main_frame)
        main_frame.add(right_panel)
        self.create_results_panel(right_panel)
        
        # Status bar
        self.create_status_bar()
    
    def create_toolbar(self):
        """Barra de herramientas superior"""
        toolbar = tk.Frame(self.root, bg="#34495e", height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Title
        title = tk.Label(toolbar, text="NEURO-PROBE", 
                        font=("Arial", 16, "bold"),
                        fg="white", bg="#34495e")
        title.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Quick buttons
        self.run_btn = tk.Button(toolbar, text="RUN", 
                                command=self.run_analysis,
                                bg="#27ae60", fg="white",
                                font=("Arial", 12, "bold"),
                                width=10, height=1)
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(toolbar, text="Export JSON", 
                 command=self.export_json,
                 bg="#3498db", fg="white",
                 font=("Arial", 10, "bold"),
                 width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(toolbar, text="Export HTML", 
                 command=self.export_html,
                 bg="#9b59b6", fg="white",
                 font=("Arial", 10, "bold"),
                 width=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(toolbar, text="Clear",  
                 command=self.clear_logs,
                 bg="#e74c3c", fg="white",
                 font=("Arial", 10, "bold"),
                 width=8).pack(side=tk.LEFT, padx=5)
    
    def create_config_panel(self, parent):
        """Panel de configuración izquierdo"""
        # Header
        header = tk.Label(parent, text="Configuration", 
                         font=("Arial", 14, "bold"),
                         bg="#34495e", fg="white")
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Content frame
        content = tk.Frame(parent, bg="#f0f0f0", padx=15, pady=15)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Kernel selection
        tk.Label(content, text="Kernel Image:", 
                font=("Arial", 11, "bold"), 
                bg="#f0f0f0").pack(anchor=tk.W, pady=(0, 5))
        
        kernel_frame = tk.Frame(content, bg="#f0f0f0")
        kernel_frame.pack(fill=tk.X, pady=(0, 15))
        
        kernel_entry = tk.Entry(kernel_frame, textvariable=self.kernel_path,
                               font=("Arial", 9), state='readonly')
        kernel_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        tk.Button(kernel_frame, text="Browse...",
                 command=self.select_kernel,
                 bg="#3498db", fg="white",
                 font=("Arial", 9, "bold")).pack(side=tk.RIGHT)
        
        # Emulators
        emu_frame = tk.LabelFrame(content, text="Emulators", 
                                 font=("Arial", 11, "bold"),
                                 bg="#f0f0f0", padx=10, pady=10)
        emu_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Checkbutton(emu_frame, text="QEMU", 
                      variable=self.qemu_enabled,
                      font=("Arial", 10), bg="#f0f0f0").pack(anchor=tk.W)
        
        tk.Checkbutton(emu_frame, text="VirtualBox", 
                      variable=self.vbox_enabled,
                      font=("Arial", 10), bg="#f0f0f0").pack(anchor=tk.W)
        
        tk.Checkbutton(emu_frame, text="Bochs", 
                      variable=self.bochs_enabled,
                      font=("Arial", 10), bg="#f0f0f0").pack(anchor=tk.W)
        
        # Timeout
        timeout_frame = tk.Frame(content, bg="#f0f0f0")
        timeout_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(timeout_frame, text="Timeout (seconds):", 
                font=("Arial", 11, "bold"),
                bg="#f0f0f0").pack(anchor=tk.W, pady=(0, 5))
        
        tk.Spinbox(timeout_frame, from_=1, to=60, 
                  textvariable=self.timeout,
                  font=("Arial", 10), width=10).pack(anchor=tk.W)
        
        # Status indicator
        status_frame = tk.LabelFrame(content, text="Status", 
                                    font=("Arial", 11, "bold"),
                                    bg="#f0f0f0", padx=10, pady=10)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.status_label = tk.Label(status_frame, textvariable=self.status,
                                     font=("Arial", 10),
                                     bg="#f0f0f0", fg="#27ae60")
        self.status_label.pack()
        
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(5, 0))
    
    def create_results_panel(self, parent):
        """Panel de resultados derecho"""
        # Notebook con tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Console / Logs
        console_frame = tk.Frame(self.notebook)
        self.notebook.add(console_frame, text="Console")
        
        self.console = scrolledtext.ScrolledText(console_frame,
                                                font=("Consolas", 9),
                                                bg="#1e1e1e", fg="#00ff00",
                                                wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Tab 2: Comparison
        compare_frame = tk.Frame(self.notebook)
        self.notebook.add(compare_frame, text="Comparison")
        
        # Sub-panels for each emulator
        self.comparison_panels = {}
        for emu in ["QEMU", "VirtualBox", "Bochs"]:
            panel = tk.LabelFrame(compare_frame, text=emu, 
                                 font=("Arial", 10, "bold"))
            panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            text = scrolledtext.ScrolledText(panel, height=8,
                                            font=("Consolas", 9),
                                            wrap=tk.WORD)
            text.pack(fill=tk.BOTH, expand=True)
            self.comparison_panels[emu] = text
        
        # Tab 3: Divergences
        div_frame = tk.Frame(self.notebook)
        self.notebook.add(div_frame, text="Divergences")
        
        self.divergences = scrolledtext.ScrolledText(div_frame,
                                                     font=("Arial", 10),
                                                     wrap=tk.WORD)
        self.divergences.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        """Barra de estado inferior"""
        status_bar = tk.Frame(self.root, bg="#ecf0f1", height=25)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_text = tk.Label(status_bar, text="Ready to analyze", 
                                   bg="#ecf0f1", anchor=tk.W, padx=10)
        self.status_text.pack(side=tk.LEFT)
    
    # === FUNCIONES ===
    
    def select_kernel(self):
        """Seleccionar imagen de kernel"""
        path = filedialog.askopenfilename(
            title="Select Kernel Image",
            filetypes=[("Image files", "*.img *.iso"), ("All files", "*.*")]
        )
        if path:
            self.kernel_path.set(path)
            self.log(f"[INFO] Kernel selected: {path}")
            self.update_status_bar(f"Kernel: {Path(path).name}")
    
    def run_analysis(self):
        """Ejecutar análisis"""
        # Validations
        if not self.kernel_path.get():
            messagebox.showerror("Error", "Please select a kernel image first")
            return
        
        if not Path(self.kernel_path.get()).exists():
            messagebox.showerror("Error", "Kernel image does not exist")
            return
        
        if not any([self.qemu_enabled.get(), self.vbox_enabled.get(), self.bochs_enabled.get()]):
            messagebox.showerror("Error", "Select at least one emulator")
            return
        
        # Start analysis in thread
        self.run_btn.config(state=tk.DISABLED, text="RUNNING...")
        self.progress.start()
        self.set_status("Running", "orange")
        
        thread = threading.Thread(target=self._run_analysis_thread, daemon=True)
        thread.start()
    
    def _run_analysis_thread(self):
        """Análisis en thread separado"""
        try:
            self.log("=" * 70)
            self.log("[START] Neuro-Probe Analysis")
            self.log("=" * 70)
            
            # Build emulator list
            emulators = []
            if self.qemu_enabled.get():
                emulators.append("qemu")
            if self.vbox_enabled.get():
                emulators.append("virtualbox")
            if self.bochs_enabled.get():
                emulators.append("bochs")
            
            self.log(f"[CONFIG] Emulators: {', '.join(emulators)}")
            self.log(f"[CONFIG] Timeout: {self.timeout.get()}s")
            self.log(f"[CONFIG] Image: {self.kernel_path.get()}")
            self.log("")
            
            # Create probe
            self.set_status("Initializing", "blue")
            probe = NeuroProbe()
            probe.config["analysis"]["timeout"] = self.timeout.get()
            
            # Setup
            self.set_status("Configuring", "blue")
            probe.setup_emulators(self.kernel_path.get(), emulators)
            self.log(f"[INFO] {len(probe.emulators)} emulator(s) configured")
            self.log("")
            
            # Run
            self.set_status("Running Tests", "orange")
            self.log("[EXEC] Running emulators...")
            
            probe.run_tests()
            
            # Log results
            for name, result in probe.results.items():
                if "error" in result:
                    self.log(f"[ERROR] {name}: {result['error']}")
                else:
                    self.log(f"[OK] {name} completed in {result['duration']:.2f}s")
            
            self.log("")
            
            # Analyze
            self.set_status("Analyzing", "blue")
            self.log("[ANALYZE] Comparing results...")
            divergences = probe.analyze_results()
            
            if divergences:
                self.log(f"[WARN] {len(divergences)} divergence(s) found")
            else:
                self.log("[OK] No divergences - identical behavior")
            
            # Store results
            self.last_results = probe.results
            self.last_divergences = divergences
            
            # Display
            self.display_comparison(probe.results)
            self.display_divergences(divergences)
            
            self.log("")
            self.log("=" * 70)
            self.log("[DONE] Analysis complete!")
            self.log("=" * 70)
            
            self.set_status("Complete", "green")
            self.update_status_bar("Analysis complete - Review results")
            
            messagebox.showinfo("Success", "Analysis completed!\nCheck the tabs for results.")
            
        except Exception as e:
            self.log(f"[FATAL ERROR] {e}")
            self.set_status("Error", "red")
            messagebox.showerror("Error", f"Analysis failed:\n{e}")
            
        finally:
            self.progress.stop()
            self.run_btn.config(state=tk.NORMAL, text="RUN")
    
    def display_comparison(self, results):
        """Mostrar comparación en panels"""
        for name, result in results.items():
            if name in self.comparison_panels:
                panel = self.comparison_panels[name]
                panel.delete(1.0, tk.END)
                
                if "error" in result:
                    panel.insert(tk.END, f"ERROR: {result['error']}\n")
                else:
                    serial = result.get("serial_output", "")
                    duration = result.get("duration", 0)
                    
                    panel.insert(tk.END, f"Serial Output:\n")
                    panel.insert(tk.END, f"{serial}\n\n")
                    panel.insert(tk.END, f"Duration: {duration:.2f}s\n")
                    panel.insert(tk.END, f"Status: Completed\n")
    
    def display_divergences(self, divergences):
        """Mostrar divergencias"""
        self.divergences.delete(1.0, tk.END)
        
        if not divergences:
            self.divergences.insert(tk.END, "\n")
            self.divergences.insert(tk.END, "  ╔═══════════════════════════════╗\n", "success")
            self.divergences.insert(tk.END, "  ║   NO DIVERGENCES FOUND       ║\n", "success")
            self.divergences.insert(tk.END, "  ╚═══════════════════════════════╝\n", "success")
            self.divergences.insert(tk.END, "\n  All emulators produced identical output.\n")
        else:
            self.divergences.insert(tk.END, f"\n  Found {len(divergences)} divergence(s):\n\n", "warn")
            
            for i, div in enumerate(divergences, 1):
                self.divergences.insert(tk.END, f"  [{i}] ", "bold")
                
                if div["type"] == "marker_difference":
                    self.divergences.insert(tk.END, f"Position {div['position']}\n")
                    for emu, marker in div["details"].items():
                        if marker:
                            self.divergences.insert(tk.END, f"      {emu}: '{marker}'\n")
                        else:
                            self.divergences.insert(tk.END, f"      {emu}: (not reached)\n", "error")
                
                elif div["type"] == "length_difference":
                    self.divergences.insert(tk.END, "Different marker count\n")
                    for emu, length in div["details"].items():
                        self.divergences.insert(tk.END, f"      {emu}: {length} markers\n")
                
                self.divergences.insert(tk.END, "\n")
        
        # Tags
        self.divergences.tag_config("success", foreground="green")
        self.divergences.tag_config("warn", foreground="orange")
        self.divergences.tag_config("error", foreground="red")
        self.divergences.tag_config("bold", font=("Arial", 10, "bold"))
    
    def log(self, message):
        """Agregar log a consola"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console.see(tk.END)
        self.root.update()
    
    def set_status(self, text, color="green"):
        """Actualizar indicador de estado"""
        colors = {
            "green": "#27ae60",
            "blue": "#3498db",
            "orange": "#f39c12",
            "red": "#e74c3c"
        }
        self.status.set(text)
        self.status_label.config(fg=colors.get(color, "black"))
    
    def update_status_bar(self, text):
        """Actualizar status bar"""
        self.status_text.config(text=text)
    
    def export_json(self):
        """Exportar a JSON"""
        if not self.last_results:
            messagebox.showwarning("Warning", "Run analysis first")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if path:
            try:
                report = {
                    "timestamp": datetime.now().isoformat(),
                    "tool": "Neuro-Probe GUI",
                    "version": "1.0.0",
                    "results": self.last_results,
                    "divergences": self.last_divergences
                }
                
                with open(path, 'w') as f:
                    json.dump(report, f, indent=2)
                
                self.log(f"[EXPORT] JSON saved: {path}")
                messagebox.showinfo("Success", f"Report saved to:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed:\n{e}")
    
    def export_html(self):
        """Exportar a HTML"""
        if not self.last_results:
            messagebox.showwarning("Warning", "Run analysis first")
            return
        
        path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if path:
            try:
                html = self.generate_html_report()
                with open(path, 'w') as f:
                    f.write(html)
                
                self.log(f"[EXPORT] HTML saved: {path}")
                messagebox.showinfo("Success", f"HTML report saved to:\n{path}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed:\n{e}")
    
    def generate_html_report(self):
        """Generar reporte HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Neuro-Probe Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #34495e; }}
        .emulator {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; }}
        .success {{ color: green; }}
        .error {{ color: red; }}
        pre {{ background: #f0f0f0; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>Neuro-Probe Analysis Report</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    
    <h2>Results</h2>
"""
        for name, result in self.last_results.items():
            if "error" in result:
                html += f'<div class="emulator"><h3 class="error">{name}</h3><p>Error: {result["error"]}</p></div>'
            else:
                serial = result.get("serial_output", "")
                duration = result.get("duration", 0)
                html += f'''
    <div class="emulator">
        <h3 class="success">{name}</h3>
        <p><strong>Duration:</strong> {duration:.2f}s</p>
        <p><strong>Serial Output:</strong></p>
        <pre>{serial}</pre>
    </div>
'''
        
        html += "<h2>Divergences</h2>"
        if self.last_divergences:
            html += f"<p>Found {len(self.last_divergences)} divergence(s)</p><ul>"
            for div in self.last_divergences:
                html += f"<li>{div}</li>"
            html += "</ul>"
        else:
            html += '<p class="success">No divergences found - identical behavior</p>'
        
        html += "</body></html>"
        return html
    
    def clear_logs(self):
        """Limpiar logs"""
        self.console.delete(1.0, tk.END)
        self.log("[INFO] Logs cleared")


def main():
    """Entry point"""
    root = tk.Tk()
    app = NeuroProbeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

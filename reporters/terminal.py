"""Reporter de terminal SIMPLE para Neuro-Probe - Solo ASCII"""

from typing import Dict, List


class TerminalReporter:
    """Genera reporte visual en la terminal - SOLO ASCII"""
    
    # Colores ANSI
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    
    def generate(self, results: Dict, divergences: List[Dict]):
        """Genera reporte en terminal"""
        self.print_header()
        self.print_results(results)
        if divergences:
            self.print_divergences(divergences)
            self.print_recommendation(divergences)
        else:
            self.print_success()
    
    def print_header(self):
        """Imprime cabecera"""
        print(f"\n{self.CYAN}{self.BOLD}=" * 60 + f"{self.RESET}")
        print(f"{self.CYAN}{self.BOLD}     NEURO-PROBE: ANALISIS DE EMULADORES{self.RESET}")
        print(f"{self.CYAN}{self.BOLD}=" * 60 + f"{self.RESET}\n")
    
    def print_results(self, results: Dict):
        """Imprime resultados de cada emulador"""
        for emu_name, result in results.items():
            if "error" in result:
                print(f"{self.RED}X {emu_name}: ERROR - {result['error']}{self.RESET}\n")
                continue
            
            serial = result.get("serial_output", "")
            duration = result.get("duration", 0)
            
            print(f"{self.BOLD}--- {emu_name} {'-' * (50 - len(emu_name))}{self.RESET}")
            print(f"  Serial: {self.GREEN}{serial}{self.RESET}")
            print(f"  Duracion: {duration:.2f}s")
            print(f"  Estado: {self.GREEN}OK Completado{self.RESET}")
            print(f"{'-' * 60}\n")
    
    def print_divergences(self, divergences: List[Dict]):
        """Imprime divergencias encontradas"""
        print(f"{self.YELLOW}{self.BOLD}=" * 60 + f"{self.RESET}")
        print(f"{self.YELLOW}{self.BOLD}           DIVERGENCIAS ENCONTRADAS{self.RESET}")
        print(f"{self.YELLOW}{self.BOLD}=" * 60 + f"{self.RESET}\n")
        
        for i, div in enumerate(divergences, 1):
            if div["type"] == "marker_difference":
                print(f"{self.RED}[{i}] Diferencia en posicion {div['position']}{self.RESET}")
                for emu, marker in div["details"].items():
                    if marker is None:
                        print(f"    {self.RED}X {emu}: (no alcanzado){self.RESET}")
                    else:
                        print(f"    {self.GREEN}OK {emu}: '{marker}'{self.RESET}")
                print()
            
            elif div["type"] == "length_difference":
                print(f"{self.RED}[{i}] Diferencia en cantidad de markers{self.RESET}")
                for emu, length in div["details"].items():
                    print(f"    {emu}: {length} markers")
                print()
    
    def print_recommendation(self, divergences: List[Dict]):
        """Imprime recomendacion basada en divergencias"""
        print(f"{self.MAGENTA}{self.BOLD}=" * 60 + f"{self.RESET}")
        print(f"{self.MAGENTA}{self.BOLD}              RECOMENDACION{self.RESET}")
        print(f"{self.MAGENTA}{self.BOLD}=" * 60 + f"{self.RESET}\n")
        
        high_severity = any(d.get("severity") == "high" for d in divergences)
        
        if high_severity:
            print(f"{self.YELLOW}WARNING: Diferencias significativas detectadas.{self.RESET}")
            print(f"    Usa el emulador que da mas informacion de debug.\n")
        else:
            print(f"{self.YELLOW}INFO: Diferencias menores detectadas.{self.RESET}")
            print(f"    Ambos emuladores son validos para desarrollo.\n")
    
    def print_success(self):
        """Imprime mensaje de exito si no hay divergencias"""
        print(f"{self.GREEN}{self.BOLD}=" * 60 + f"{self.RESET}")
        print(f"{self.GREEN}{self.BOLD}          OK COMPORTAMIENTO IDENTICO{self.RESET}")
        print(f"{self.GREEN}{self.BOLD}=" * 60 + f"{self.RESET}\n")
        print(f"{self.GREEN}Todos los emuladores produjeron la misma salida.{self.RESET}\n")

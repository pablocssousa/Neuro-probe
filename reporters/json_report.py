"""Reporter JSON para Neuro-Probe"""

import json
from typing import Dict, List
from datetime import datetime


class JSONReporter:
    """Genera reporte en formato JSON"""
    
    def generate(self, results: Dict, divergences: List[Dict], output_path: str):
        """
        Genera reporte JSON
        
        Args:
            results: Resultados de emuladores
            divergences: Divergencias encontradas
            output_path: Ruta donde guardar el JSON
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "tool": "Neuro-Probe",
            "version": "1.0.0",
            "emulators_tested": len(results),
            "results": results,
            "divergences": {
                "count": len(divergences),
                "details": divergences
            },
            "summary": self.generate_summary(results, divergences)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    def generate_summary(self, results: Dict, divergences: List[Dict]) -> Dict:
        """Genera resumen del análisis"""
        successful = sum(1 for r in results.values() if "error" not in r)
        failed = len(results) - successful
        
        return {
            "emulators_successful": successful,
            "emulators_failed": failed,
            "has_divergences": len(divergences) > 0,
            "divergence_count": len(divergences),
            "high_severity_count": sum(1 for d in divergences if d.get("severity") == "high")
        }

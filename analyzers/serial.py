"""Analizador de salida serial para Neuro-Probe"""

from typing import List, Dict


class SerialAnalyzer:
    """Analiza la salida serial y extrae markers"""
    
    def __init__(self, markers: str):
        """
        Inicializa el analizador con los markers esperados
        
        Args:
            markers: String con todos los markers válidos, ej: "[]{}!?ABC123"
        """
        self.markers = set(markers)
    
    def parse(self, serial_output: str) -> Dict:
        """
        Parsea la salida serial y extrae información
        
        Returns:
            Dict con markers encontrados, orden, timing, etc.
        """
        result = {
            "raw_output": serial_output,
            "markers_found": [],
            "markers_order": [],
            "total_markers": 0,
            "unknown_chars": []
        }
        
        for char in serial_output:
            if char in self.markers:
                result["markers_found"].append(char)
                result["markers_order"].append({
                    "marker": char,
                    "position": len(result["markers_order"])
                })
                result["total_markers"] += 1
            elif char not in ['\r', '\n', '\x00']:
                # Caracter desconocido (podría ser error)
                result["unknown_chars"].append(char)
        
        return result
    
    def get_markers_string(self, parsed: Dict) -> str:
        """Convierte markers encontrados a string simple"""
        return ''.join(parsed["markers_found"])

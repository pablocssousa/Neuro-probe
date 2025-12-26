"""Comparador de resultados entre emuladores"""

from typing import Dict, List


class Comparator:
    """Compara resultados de múltiples emuladores"""
    
    def compare(self, parsed_results: Dict[str, Dict]) -> List[Dict]:
        """
        Compara resultados parseados de diferentes emuladores
        
        Args:
            parsed_results: Dict con nombre_emulador → resultado_parseado
        
        Returns:
            Lista de divergencias encontradas
        """
        divergences = []
        
        if len(parsed_results) < 2:
            return divergences
        
        # Obtener todos los emuladores
        emulators = list(parsed_results.keys())
        
        # Comparar markers uno a uno
        max_markers = max(len(r["markers_found"]) for r in parsed_results.values())
        
        for pos in range(max_markers):
            markers_at_pos = {}
            
            for emu_name, result in parsed_results.items():
                if pos < len(result["markers_found"]):
                    marker = result["markers_found"][pos]
                    markers_at_pos[emu_name] = marker
                else:
                    markers_at_pos[emu_name] = None
            
            # Verificar si todos tienen el mismo marker
            unique_markers = set(m for m in markers_at_pos.values() if m is not None)
            
            if len(unique_markers) > 1 or None in markers_at_pos.values():
                # DIVERGENCIA ENCONTRADA
                divergences.append({
                    "position": pos,
                    "type": "marker_difference",
                    "details": markers_at_pos,
                    "severity": "high" if None in markers_at_pos.values() else "medium"
                })
        
        # Comparar longitudes totales
        lengths = {name: len(r["markers_found"]) for name, r in parsed_results.items()}
        if len(set(lengths.values())) > 1:
            divergences.append({
                "type": "length_difference",
                "details": lengths,
                "severity": "high"
            })
        
        return divergences

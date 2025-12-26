"""Base emulator class for Neuro-Probe"""

from abc import ABC, abstractmethod
from typing import Dict
import subprocess
import time


class Emulator(ABC):
    """Abstract base class for emulator wrappers"""
    
    def __init__(self, image_path: str, config: dict):
        self.image_path = image_path
        self.config = config
        self.name = self.__class__.__name__.replace("Emulator", "")
        self.process = None
        self.serial_output = ""
        
    @abstractmethod
    def prepare(self):
        """Prepare emulator for running (convert image if needed, etc.)"""
        pass
    
    @abstractmethod
    def start(self):
        """Start the emulator"""
        pass
    
    @abstractmethod
    def stop(self):
        """Stop the emulator"""
        pass
    
    @abstractmethod
    def get_serial_output(self) -> str:
        """Get serial port output"""
        pass
    
    def run(self, timeout: int = 10) -> Dict:
        """Run emulator and capture results"""
        result = {
            "name": self.name,
            "start_time": time.time(),
            "status": "unknown",
            "serial_output": "",
            "error": None
        }
        
        try:
            # Prepare
            self.prepare()
            
            # Start
            self.start()
            
            # Wait for timeout
            time.sleep(timeout)
            
            # Get output
            result["serial_output"] = self.get_serial_output()
            result["status"] = "completed"
            
        except Exception as e:
            result["error"] = str(e)
            result["status"] = "failed"
        
        finally:
            # Stop
            try:
                self.stop()
            except:
                pass
            
            result["end_time"] = time.time()
            result["duration"] = result["end_time"] - result["start_time"]
        
        return result

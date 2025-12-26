"""QEMU emulator wrapper for Neuro-Probe"""

import subprocess
import os
import time
from pathlib import Path
from .base import Emulator


class QEMUEmulator(Emulator):
    """QEMU emulator wrapper"""
    
    def __init__(self, image_path: str, config: dict):
        super().__init__(image_path, config)
        self.serial_log = "qemu_serial.log"
        self.qemu_path = config.get("path", "qemu-system-x86_64")
        
    def prepare(self):
        """Prepare QEMU (image is already in raw format)"""
        # Clean up old serial log
        if os.path.exists(self.serial_log):
            os.remove(self.serial_log)
    
    def start(self):
        """Start QEMU"""
        cmd = [
            self.qemu_path,
            "-drive", f"file={self.image_path},format=raw",
            "-serial", f"file:{self.serial_log}",
            "-display", "none",
            "-no-reboot"
        ]
        
        # Start in background
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    
    def stop(self):
        """Stop QEMU"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
    
    def get_serial_output(self) -> str:
        """Get serial output from log file"""
        try:
            if os.path.exists(self.serial_log):
                with open(self.serial_log, 'rb') as f:
                    return f.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return f"ERROR: {e}"
        
        return ""

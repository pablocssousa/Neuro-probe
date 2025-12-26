"""VirtualBox emulator wrapper for Neuro-Probe"""

import subprocess
import os
import time
from pathlib import Path
from .base import Emulator


class VirtualBoxEmulator(Emulator):
    """VirtualBox emulator wrapper"""
    
    def __init__(self, image_path: str, config: dict):
        super().__init__(image_path, config)
        self.vbox_path = config.get("path", "VBoxManage")
        self.vm_name = "Neuro-Probe-Test"
        self.vdi_path = "neuro-probe-test.vdi"
        self.serial_log = config.get("serial_log", "vbox_serial.log")
        
    def prepare(self):
        """Prepare VirtualBox (convert to VDI, create/update VM)"""
        # Clean old serial log
        if os.path.exists(self.serial_log):
            os.remove(self.serial_log)
        
        # Convert RAW to VDI
        cmd_convert = [
            self.vbox_path,
            "convertfromraw",
            "--format", "VDI",
            self.image_path,
            self.vdi_path
        ]
        subprocess.run(cmd_convert, capture_output=True)
        
        # Check if VM exists, create if not
        vm_list = subprocess.run(
            [self.vbox_path, "list", "vms"],
            capture_output=True,
            text=True
        )
        
        if self.vm_name not in vm_list.stdout:
            # Create VM
            subprocess.run([
                self.vbox_path, "createvm",
                "--name", self.vm_name,
                "--ostype", "Other_64",
                "--register"
            ], capture_output=True)
            
            # Configure VM
            subprocess.run([
                self.vbox_path, "modifyvm", self.vm_name,
                "--memory", "64",
                "--cpus", "1",
                "--boot1", "disk",
                "--uart1", "0x3F8", "4",
                "--uartmode1", f"file {os.path.abspath(self.serial_log)}"
            ], capture_output=True)
            
            # Create storage controller
            subprocess.run([
                self.vbox_path, "storagectl", self.vm_name,
                "--name", "IDE",
                "--add", "ide",
                "--controller", "PIIX4"
            ], capture_output=True)
        
        # Attach disk
        subprocess.run([
            self.vbox_path, "storageattach", self.vm_name,
            "--storagectl", "IDE",
            "--port", "0",
            "--device", "0",
            "--type", "hdd",
            "--medium", os.path.abspath(self.vdi_path)
        ], capture_output=True)
    
    def start(self):
        """Start VirtualBox VM"""
        subprocess.run([
            self.vbox_path, "startvm", self.vm_name,
            "--type", "headless"
        ], capture_output=True)
    
    def stop(self):
        """Stop VirtualBox VM"""
        subprocess.run([
            self.vbox_path, "controlvm", self.vm_name,
            "poweroff"
        ], capture_output=True)
    
    def get_serial_output(self) -> str:
        """Get serial output from log file"""
        try:
            if os.path.exists(self.serial_log):
                with open(self.serial_log, 'rb') as f:
                    return f.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return f"ERROR: {e}"
        
        return ""

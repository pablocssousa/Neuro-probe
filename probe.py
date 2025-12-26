"""
Neuro-Probe: Emulator Behavior Analyzer
Main entry point for running kernel tests across multiple emulators
"""

import argparse
import sys
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from emulators import QEMUEmulator, VirtualBoxEmulator
from analyzers import SerialAnalyzer, Comparator
from reporters import TerminalReporter, JSONReporter


class NeuroProbe:
    def __init__(self, config_path: str = "config.json"):
        """Initialize Neuro-Probe with configuration"""
        self.config = self.load_config(config_path)
        self.emulators = []
        self.results = {}
        
    def load_config(self, path: str) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"WARNING: Config file not found: {path}")
            print("Using default configuration...")
            return self.get_default_config()
    
    def get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            "emulators": {
                "qemu": {
                    "path": "qemu-system-x86_64",
                    "enabled": True
                },
                "virtualbox": {
                    "path": "C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage.exe",
                    "enabled": True
                }
            },
            "analysis": {
                "timeout": 10,
                "markers": "[]{}!?ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                "compare_screenshots": False
            }
        }
    
    def setup_emulators(self, image_path: str, emulator_names: List[str] = None):
        """Setup emulators for testing"""
        if emulator_names is None:
            # Use all enabled emulators from config
            emulator_names = [name for name, cfg in self.config["emulators"].items() 
                            if cfg.get("enabled", True)]
        
        for name in emulator_names:
            if name.lower() == "qemu":
                self.emulators.append(QEMUEmulator(image_path, self.config["emulators"]["qemu"]))
            elif name.lower() == "virtualbox":
                self.emulators.append(VirtualBoxEmulator(image_path, self.config["emulators"]["virtualbox"]))
            else:
                print(f"WARNING: Unknown emulator: {name}")
    
    def run_tests(self):
        """Run kernel in all emulators"""
        print(">> Starting Neuro-Probe analysis...")
        print(f">> Testing {len(self.emulators)} emulator(s)\n")
        
        for emulator in self.emulators:
            print(f">>  Running {emulator.name}...")
            try:
                result = emulator.run(timeout=self.config["analysis"]["timeout"])
                self.results[emulator.name] = result
                print(f"OK {emulator.name} completed\n")
            except Exception as e:
                print(f"X {emulator.name} failed: {e}\n")
                self.results[emulator.name] = {"error": str(e)}
    
    def analyze_results(self):
        """Analyze and compare results"""
        print(">> Analyzing results...")
        
        # Parse serial outputs
        analyzer = SerialAnalyzer(self.config["analysis"]["markers"])
        parsed_results = {}
        
        for emu_name, result in self.results.items():
            if "error" not in result:
                parsed = analyzer.parse(result.get("serial_output", ""))
                parsed_results[emu_name] = parsed
        
        # Compare results
        if len(parsed_results) > 1:
            comparator = Comparator()
            divergences = comparator.compare(parsed_results)
            return divergences
        else:
            return []
    
    def generate_reports(self, divergences: List[Dict], output_path: str = None):
        """Generate reports"""
        # Terminal report (always)
        reporter = TerminalReporter()
        reporter.generate(self.results, divergences)
        
        # JSON report (if requested)
        if output_path:
            json_reporter = JSONReporter()
            json_reporter.generate(self.results, divergences, output_path)
            print(f"\n>> Report saved to: {output_path}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Neuro-Probe: Emulator Behavior Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  probe.py --image kernel.img
  probe.py --image kernel.img --emulators qemu,virtualbox
  probe.py --image kernel.img --output report.json
        """
    )
    
    parser.add_argument("--image", required=True, help="Kernel image file")
    parser.add_argument("--emulators", help="Comma-separated list of emulators (default: all enabled)")
    parser.add_argument("--config", default="config.json", help="Config file path")
    parser.add_argument("--output", help="Output JSON report path")
    parser.add_argument("--timeout", type=int, help="Override timeout in seconds")
    
    args = parser.parse_args()
    
    # Verify image exists
    if not Path(args.image).exists():
        print(f"X Image file not found: {args.image}")
        sys.exit(1)
    
    # Initialize probe
    probe = NeuroProbe(args.config)
    
    # Override timeout if specified
    if args.timeout:
        probe.config["analysis"]["timeout"] = args.timeout
    
    # Setup emulators
    emulator_list = args.emulators.split(',') if args.emulators else None
    probe.setup_emulators(args.image, emulator_list)
    
    if not probe.emulators:
        print("X No emulators configured!")
        sys.exit(1)
    
    # Run tests
    probe.run_tests()
    
    # Analyze
    divergences = probe.analyze_results()
    
    # Report
    output_file = args.output if args.output else None
    probe.generate_reports(divergences, output_file)
    
    print("\n* Analysis complete!")


if __name__ == "__main__":
    main()

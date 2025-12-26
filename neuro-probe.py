#!/usr/bin/env python3
"""
Neuro-Probe Launcher
Unified entry point - choose CLI or GUI
"""

import sys
import argparse


def print_banner():
    """Show welcome banner"""
    print()
    print("=" * 60)
    print("          NEURO-PROBE v1.0.0")
    print("     Emulator Behavior Analysis Tool")
    print("=" * 60)
    print()


def main():
    """Main launcher"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="Neuro-Probe: Emulator Analysis Tool",
        epilog="""
Examples:
  neuro-probe                    # Interactive mode (choose CLI/GUI)
  neuro-probe gui                # Launch GUI
  neuro-probe cli --image kernel.img  # Run CLI analysis
        """
    )
    
    parser.add_argument('mode', nargs='?', choices=['cli', 'gui', 'interactive'],
                       default='interactive',
                       help='Launch mode: cli, gui, or interactive (default)')
    
    parser.add_argument('--image', help='Kernel image (CLI mode)')
    parser.add_argument('--emulators', help='Emulators to use (CLI mode)')
    parser.add_argument('--timeout', type=int, help='Timeout in seconds (CLI mode)')
    parser.add_argument('--output', help='Output file for report (CLI mode)')
    
    args = parser.parse_args()
    
    # Interactive mode - ask user
    if args.mode == 'interactive':
        print("Select mode:")
        print("  [1] GUI - Graphical Interface")
        print("  [2] CLI - Command Line")
        print("  [q] Quit")
        print()
        
        choice = input("Choice: ").strip().lower()
        
        if choice == '1' or choice == 'gui':
            args.mode = 'gui'
        elif choice == '2' or choice == 'cli':
            args.mode = 'cli'
        elif choice == 'q' or choice == 'quit':
            print("\nExiting...")
            return
        else:
            print("\nInvalid choice. Exiting...")
            return
    
    # Launch selected mode
    if args.mode == 'gui':
        print("Launching GUI...")
        print()
        try:
            import gui
            gui.main()
        except ImportError as e:
            print(f"ERROR: Could not launch GUI: {e}")
            print("Make sure Tkinter is installed.")
            sys.exit(1)
    
    elif args.mode == 'cli':
        print("Running CLI analysis...")
        print()
        
        # Build CLI args
        cli_args = ['probe.py']
        
        if args.image:
            cli_args.extend(['--image', args.image])
        
        if args.emulators:
            cli_args.extend(['--emulators', args.emulators])
        
        if args.timeout:
            cli_args.extend(['--timeout', str(args.timeout)])
        
        if args.output:
            cli_args.extend(['--output', args.output])
        
        # Override sys.argv and run
        sys.argv = cli_args
        
        try:
            import probe
            probe.main()
        except Exception as e:
            print(f"ERROR: CLI failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()

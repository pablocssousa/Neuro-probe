#!/bin/bash
# Neuro-Probe Launcher for Linux/Mac

echo ""
echo "============================================================"
echo "          NEURO-PROBE v1.0.0"
echo "     Emulator Behavior Analysis Tool"
echo "============================================================"
echo ""

python3 neuro-probe.py "$@"

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to launch Neuro-Probe"
    echo "Make sure Python 3.7+ is installed"
    read -p "Press Enter to continue..."
fi

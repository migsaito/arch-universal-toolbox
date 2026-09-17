#!/usr/bin/env python3
"""
Arch Universal Toolbox - Entry point
"""

import sys
import os

# Add src to path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Rocket Simulation Launcher
Simple startup script with dependency checking
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed"""
    required = ['flask', 'numpy']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def install_dependencies(packages):
    """Install missing packages"""
    print(f"Installing missing packages: {', '.join(packages)}")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 Rocket Simulation Setup")
    print("=" * 40)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        if input("Install automatically? (y/n): ").lower() == 'y':
            if install_dependencies(missing):
                print("✅ Dependencies installed successfully")
            else:
                print("❌ Failed to install dependencies")
                return
        else:
            print("Please install manually: pip install " + " ".join(missing))
            return
    
    # Start the application
    print("\n🚀 Starting Rocket Simulation...")
    try:
        from app import app
        print("📡 Server starting at: http://localhost:5000")
        app.run(debug=False, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Smart dependency checker that only installs what's needed
"""

import sys
import subprocess
from packaging import version

def check_package(package_name, min_version=None):
    """Check if package is installed with minimum version"""
    try:
        if package_name == "python-docx":
            import docx
            return True, "installed"
        else:
            module = __import__(package_name)
            if hasattr(module, '__version__'):
                pkg_version = module.__version__
                if min_version and version.parse(pkg_version) < version.parse(min_version):
                    return False, f"{pkg_version} < {min_version}"
                return True, pkg_version
            return True, "installed"
    except ImportError:
        return False, "missing"

def main():
    print("Checking dependencies...")
    
    requirements = [
        ("pyaudiowpatch", None),
        ("torch", "2.0.0"),
        ("numpy", "1.21.0"),
        ("scipy", None),
        ("requests", None),
        ("psutil", None),
        ("python-docx", None)
    ]
    
    missing = []
    
    for package, min_ver in requirements:
        installed, status = check_package(package, min_ver)
        if installed:
            print(f"✓ {package}: {status}")
        else:
            print(f"✗ {package}: {status}")
            if min_ver:
                missing.append(f"{package}>={min_ver}")
            else:
                missing.append(package)
    
    if missing:
        print(f"\nNeed to install: {' '.join(missing)}")
        return missing
    else:
        print("\n✓ All dependencies satisfied!")
        return []

if __name__ == "__main__":
    missing_packages = main()
    if missing_packages:
        print(f"\nInstalling missing packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages + ["--user", "--quiet"])
            print("✓ Installation complete!")
        except subprocess.CalledProcessError:
            print("⚠ Some packages failed to install")
    else:
        print("No installation needed!")
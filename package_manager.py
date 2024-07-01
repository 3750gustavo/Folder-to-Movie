# package_manager.py
import subprocess
import sys
import importlib

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def ensure_package(module, package=None):
    if package is None:
        package = module
    try:
        importlib.import_module(module)
    except ImportError:
        print(f"{module} not found. Installing...")
        install(package)
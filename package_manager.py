# package_manager.py
import subprocess
import sys
import importlib

def install(package):
    process = subprocess.Popen([sys.executable, "-m", "pip", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"An error occurred while installing {package}.\n")
        print(f"Output: {output.decode('utf-8')}")
        print(f"Error: {error.decode('utf-8')}\n")
    else:
        print(f"{package} installed successfully using: \nPython Path: {sys.executable}.\n")

def ensure_package(module, package=None):
    if package is None:
        package = module
    try:
        importlib.import_module(module)
    except ImportError:
        print(f"{module} not found. Installing...\n")
        install(package)
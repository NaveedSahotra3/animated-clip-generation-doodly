#!/usr/bin/env python3
"""
Test installation and verify all components are working
Usage: python scripts/test_installation.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

def print_header(text):
    print(f"\n{BLUE}{'='*50}{NC}")
    print(f"{BLUE}{text}{NC}")
    print(f"{BLUE}{'='*50}{NC}\n")

def print_success(text):
    print(f"{GREEN}✓{NC} {text}")

def print_error(text):
    print(f"{RED}✗{NC} {text}")

def print_warning(text):
    print(f"{YELLOW}⚠{NC} {text}")

def check_command(cmd, name):
    """Check if a command exists"""
    try:
        result = subprocess.run(['which', cmd], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{name} found: {result.stdout.strip()}")
            return True
        else:
            print_error(f"{name} not found")
            return False
    except Exception as e:
        print_error(f"Error checking {name}: {e}")
        return False

def check_directory(path, name, required=True):
    """Check if a directory exists"""
    if Path(path).exists():
        print_success(f"{name} exists: {path}")
        return True
    else:
        if required:
            print_error(f"{name} not found: {path}")
        else:
            print_warning(f"{name} not found (optional): {path}")
        return False

def check_file(path, name, required=True):
    """Check if a file exists"""
    if Path(path).exists():
        size = Path(path).stat().st_size / (1024 * 1024)  # MB
        print_success(f"{name} exists: {path} ({size:.1f} MB)")
        return True
    else:
        if required:
            print_error(f"{name} not found: {path}")
        else:
            print_warning(f"{name} not found (optional): {path}")
        return False

def check_python_package(package, name):
    """Check if a Python package is installed"""
    try:
        __import__(package)
        print_success(f"{name} Python package installed")
        return True
    except ImportError:
        print_error(f"{name} Python package not installed")
        return False

def check_comfyui_running():
    """Check if ComfyUI is running"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8188/system_stats", timeout=2)
        if response.status_code == 200:
            print_success("ComfyUI server is running")
            return True
        else:
            print_warning("ComfyUI server not responding")
            return False
    except requests.exceptions.ConnectionError:
        print_warning("ComfyUI server is not running (start with: ./launch_comfyui.sh)")
        return False
    except ImportError:
        print_warning("requests package not installed (pip install requests)")
        return False
    except Exception as e:
        print_warning(f"Could not check ComfyUI status: {e}")
        return False

def main():
    print_header("AI Whiteboard Video Generator - Installation Test")
    
    results = {
        'system': [],
        'comfyui': [],
        'models': [],
        'scripts': [],
        'python': []
    }
    
    # System checks
    print_header("System Requirements")
    results['system'].append(check_command('brew', 'Homebrew'))
    results['system'].append(check_command('python3.10', 'Python 3.10'))
    results['system'].append(check_command('git', 'Git'))
    
    # ComfyUI installation
    print_header("ComfyUI Installation")
    comfyui_dir = Path.home() / "Documents" / "ComfyUI"
    results['comfyui'].append(check_directory(comfyui_dir, 'ComfyUI directory'))
    
    if comfyui_dir.exists():
        venv_dir = comfyui_dir / "venv"
        results['comfyui'].append(check_directory(venv_dir, 'Virtual environment'))
        
        launch_script = comfyui_dir / "launch_comfyui.sh"
        results['comfyui'].append(check_file(launch_script, 'Launch script'))
        
        download_script = comfyui_dir / "download_models.sh"
        results['comfyui'].append(check_file(download_script, 'Download models script'))
        
        # Check custom nodes
        manager_dir = comfyui_dir / "custom_nodes" / "ComfyUI-Manager"
        results['comfyui'].append(check_directory(manager_dir, 'ComfyUI Manager', required=False))
        
        animatediff_dir = comfyui_dir / "custom_nodes" / "ComfyUI-AnimateDiff-Evolved"
        results['comfyui'].append(check_directory(animatediff_dir, 'AnimateDiff', required=False))
    
    # Model checks
    print_header("Model Files")
    if comfyui_dir.exists():
        checkpoints_dir = comfyui_dir / "models" / "checkpoints"
        results['models'].append(check_directory(checkpoints_dir, 'Checkpoints directory'))
        
        # Check for specific models
        dreamshaper = list(checkpoints_dir.glob("*DreamShaper*.safetensors")) if checkpoints_dir.exists() else []
        if dreamshaper:
            results['models'].append(check_file(dreamshaper[0], 'DreamShaper XL model'))
        else:
            print_warning("DreamShaper XL model not found (download required)")
            results['models'].append(False)
        
        animatediff_dir = comfyui_dir / "custom_nodes" / "ComfyUI-AnimateDiff-Evolved" / "models"
        motion_module = list(animatediff_dir.glob("mm_*.ckpt")) if animatediff_dir.exists() else []
        if motion_module:
            results['models'].append(check_file(motion_module[0], 'AnimateDiff motion module'))
        else:
            print_warning("AnimateDiff motion module not found (download required)")
            results['models'].append(False)
    
    # Python packages
    print_header("Python Packages")
    results['python'].append(check_python_package('torch', 'PyTorch'))
    results['python'].append(check_python_package('PIL', 'Pillow'))
    try:
        import TTS
        results['python'].append(True)
        print_success("Coqui TTS package installed")
    except ImportError:
        results['python'].append(False)
        print_warning("Coqui TTS not installed (optional)")
    
    # Project scripts
    print_header("Project Scripts")
    project_root = Path(__file__).parent.parent
    scripts_dir = project_root / "scripts"
    results['scripts'].append(check_directory(scripts_dir, 'Scripts directory'))
    
    if scripts_dir.exists():
        script_files = ['install.sh', 'generate_clip.py', 'batch_generate.py', 
                       'generate_voiceover.py', 'assemble_video.py']
        for script in script_files:
            script_path = scripts_dir / script
            if script_path.exists():
                results['scripts'].append(True)
                print_success(f"Script exists: {script}")
            else:
                results['scripts'].append(False)
                print_error(f"Script missing: {script}")
    
    # Workflow files
    print_header("Workflow Files")
    workflows_dir = project_root / "workflows"
    if workflows_dir.exists():
        workflow_files = ['whiteboard_animation.json', 'basic_image.json']
        for workflow in workflow_files:
            workflow_path = workflows_dir / workflow
            if workflow_path.exists():
                print_success(f"Workflow exists: {workflow}")
            else:
                print_warning(f"Workflow missing: {workflow}")
    
    # ComfyUI server status
    print_header("ComfyUI Server Status")
    check_comfyui_running()
    
    # Summary
    print_header("Test Summary")
    
    total_checks = 0
    passed_checks = 0
    
    for category, checks in results.items():
        category_passed = sum(1 for c in checks if c)
        category_total = len(checks)
        total_checks += category_total
        passed_checks += category_passed
        
        status = f"{category_passed}/{category_total}"
        if category_passed == category_total:
            print_success(f"{category.capitalize()}: {status}")
        else:
            print_warning(f"{category.capitalize()}: {status}")
    
    print(f"\nOverall: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print(f"\n{GREEN}✓ All checks passed! Installation is complete.{NC}")
    else:
        print(f"\n{YELLOW}⚠ Some checks failed. Please review the errors above.{NC}")
        print("\nNext steps:")
        print("1. Run: ./scripts/install.sh (if not done)")
        print("2. Download models: cd ~/Documents/ComfyUI && ./download_models.sh")
        print("3. Start ComfyUI: cd ~/Documents/ComfyUI && ./launch_comfyui.sh")
    
    return passed_checks == total_checks

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)


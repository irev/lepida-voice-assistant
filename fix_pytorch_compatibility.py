#!/usr/bin/env python3
"""
PyTorch Compatibility Fix Script
Diagnoses and fixes PyTorch/TorchVision/Transformers compatibility issues
"""

import sys
import subprocess
import importlib.util

def check_package_version(package_name):
    """Check if a package is installed and return its version."""
    try:
        package = importlib.import_module(package_name)
        version = getattr(package, '__version__', 'Unknown')
        return True, version
    except ImportError:
        return False, None

def run_command(cmd):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def diagnose_pytorch_issue():
    """Diagnose PyTorch compatibility issues."""
    
    print("🔍 PyTorch Compatibility Diagnosis")
    print("=" * 50)
    
    # Check current versions
    packages = ['torch', 'torchvision', 'torchaudio', 'transformers']
    versions = {}
    
    for package in packages:
        installed, version = check_package_version(package)
        versions[package] = version if installed else None
        status = f"✅ {version}" if installed else "❌ Not installed"
        print(f"{package:12}: {status}")
    
    print("\n🔍 Compatibility Analysis:")
    
    # Check torch version
    if versions['torch']:
        torch_version = versions['torch']
        print(f"   PyTorch: {torch_version}")
        
        # Check for known problematic versions
        if torch_version.startswith('2.1') or torch_version.startswith('2.2'):
            print("   ⚠️  PyTorch 2.1+ may have compatibility issues with older transformers")
            return "downgrade_pytorch"
        elif torch_version.startswith('1.13') or torch_version.startswith('1.12'):
            print("   ✅ PyTorch version should be compatible")
        else:
            print("   ⚠️  PyTorch version may need adjustment")
    
    # Check torchvision
    if not versions['torchvision']:
        print("   ❌ TorchVision missing - this is likely the cause!")
        return "install_torchvision"
    
    # Check transformers
    if versions['transformers']:
        if versions['transformers'].startswith('4.36') or versions['transformers'].startswith('4.37'):
            print("   ⚠️  Transformers version may be too new for PyTorch version")
            return "downgrade_transformers"
    
    return "unknown"

def fix_pytorch_compatibility():
    """Fix PyTorch compatibility issues."""
    
    print("\n🔧 Applying PyTorch Compatibility Fix")
    print("=" * 50)
    
    # Strategy: Install compatible versions
    print("Installing compatible PyTorch ecosystem...")
    
    # Uninstall existing packages to avoid conflicts
    uninstall_packages = ['torch', 'torchvision', 'torchaudio', 'transformers']
    
    print("\n1. Removing existing packages...")
    for package in uninstall_packages:
        print(f"   Uninstalling {package}...")
        success, stdout, stderr = run_command(f"pip uninstall {package} -y")
        if success:
            print(f"   ✅ {package} uninstalled")
        else:
            print(f"   ⚠️  {package} not found or already removed")
    
    print("\n2. Installing compatible versions...")
    
    # Install specific compatible versions
    install_commands = [
        "pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cpu",
        "pip install transformers==4.25.1",
        "pip install openai-whisper"
    ]
    
    for cmd in install_commands:
        print(f"   Running: {cmd}")
        success, stdout, stderr = run_command(cmd)
        
        if success:
            print("   ✅ Installation successful")
        else:
            print(f"   ❌ Installation failed: {stderr}")
            return False
    
    return True

def verify_fix():
    """Verify that the fix worked."""
    
    print("\n✅ Verifying Fix")
    print("=" * 30)
    
    # Test imports
    test_imports = [
        "import torch",
        "import torchvision", 
        "import transformers",
        "import whisper",
        "from transformers.models.vits.modeling_vits import VitsModel"
    ]
    
    for test_import in test_imports:
        try:
            exec(test_import)
            print(f"✅ {test_import}")
        except Exception as e:
            print(f"❌ {test_import} - Error: {e}")
            return False
    
    # Test torchvision ops
    try:
        import torch
        import torchvision
        
        # Test NMS operation specifically
        boxes = torch.tensor([[0, 0, 1, 1], [0, 0, 1, 1]], dtype=torch.float32)
        scores = torch.tensor([0.9, 0.8], dtype=torch.float32)
        keep = torchvision.ops.nms(boxes, scores, 0.5)
        print("✅ torchvision.ops.nms works correctly")
        
    except Exception as e:
        print(f"❌ torchvision.ops.nms test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! The fix was successful.")
    return True

def alternative_fix():
    """Alternative fix using CPU-only PyTorch."""
    
    print("\n🔄 Trying Alternative Fix (CPU-only PyTorch)")
    print("=" * 55)
    
    # Install CPU-only versions
    commands = [
        "pip uninstall torch torchvision torchaudio transformers -y",
        "pip install torch==1.13.1+cpu torchvision==0.14.1+cpu torchaudio==0.13.1+cpu --index-url https://download.pytorch.org/whl/cpu",
        "pip install transformers==4.25.1",
        "pip install openai-whisper"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        success, stdout, stderr = run_command(cmd)
        
        if not success:
            print(f"❌ Command failed: {stderr}")
            return False
        else:
            print("✅ Command successful")
    
    return True

def main():
    """Main function to fix PyTorch compatibility."""
    
    print("🔧 PyTorch Compatibility Fixer")
    print("=" * 60)
    print("This script will fix the TorchVision NMS operator error")
    print()
    
    # Diagnose the issue
    issue_type = diagnose_pytorch_issue()
    
    # Apply fix based on diagnosis
    if issue_type in ["install_torchvision", "downgrade_pytorch", "downgrade_transformers"]:
        print(f"\n💡 Recommended fix: {issue_type}")
        
        # Try main fix
        print("\n🔧 Attempting main fix...")
        if fix_pytorch_compatibility():
            if verify_fix():
                print("\n🎉 SUCCESS! PyTorch compatibility fixed.")
                print("\nNext steps:")
                print("1. Try running: python app.py")
                print("2. If still issues, run: python cli.py health")
                return
        
        # Try alternative fix
        print("\n🔄 Main fix didn't work, trying alternative...")
        if alternative_fix():
            if verify_fix():
                print("\n🎉 SUCCESS! Alternative fix worked.")
                return
    
    # Manual instructions if automatic fix fails
    print("\n🛠️  MANUAL FIX INSTRUCTIONS")
    print("=" * 40)
    print("If automatic fixes failed, try these steps manually:")
    print()
    print("1. Uninstall conflicting packages:")
    print("   pip uninstall torch torchvision torchaudio transformers -y")
    print()
    print("2. Install compatible versions:")
    print("   pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1")
    print("   pip install transformers==4.25.1")
    print("   pip install openai-whisper")
    print()
    print("3. Test the fix:")
    print("   python -c \"import torch, torchvision, transformers; print('All OK')\"")
    print()
    print("4. If still issues, try CPU-only version:")
    print("   pip install torch==1.13.1+cpu torchvision==0.14.1+cpu torchaudio==0.13.1+cpu --index-url https://download.pytorch.org/whl/cpu")

if __name__ == "__main__":
    main()

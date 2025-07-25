#!/bin/bash
echo "🔧 Quick PyTorch Compatibility Fix"
echo "===================================="
echo ""
echo "This will fix the 'operator torchvision::nms does not exist' error"
echo ""

echo "1. Uninstalling conflicting packages..."
pip uninstall torch torchvision torchaudio transformers -y

echo ""
echo "2. Installing compatible PyTorch versions..."
pip install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cpu

echo ""
echo "3. Installing compatible transformers..."
pip install transformers==4.25.1

echo ""
echo "4. Reinstalling whisper..."
pip install openai-whisper

echo ""
echo "5. Testing the fix..."
python -c "import torch, torchvision, transformers; print('✅ All packages imported successfully')"

echo ""
echo "🎉 Fix completed! Try running: python app.py"
echo ""

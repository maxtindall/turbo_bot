#!/bin/bash
echo "Installing Turbo Bot v0.0.1..."

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Installation complete."
echo "Activate with: source venv/bin/activate"
echo "Run bot with: python bot.py"

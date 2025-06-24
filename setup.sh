#!/bin/bash

echo "========================================"
echo "Albanian Teams Transcriber - Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

echo "[1/4] Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Try: sudo apt-get install python3-pip"
    exit 1
fi

echo
echo "[2/4] Downloading Albanian ASR Model..."
if [ -d "Albanian-ASR" ]; then
    echo "Albanian-ASR already exists, skipping download..."
else
    git clone https://github.com/florijanqosja/Albanian-ASR
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to clone Albanian-ASR repository"
        echo "Make sure git is installed"
        exit 1
    fi
fi

echo
echo "[3/4] Installing Albanian ASR dependencies..."
cd Albanian-ASR
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Albanian ASR dependencies"
    cd ..
    exit 1
fi
cd ..

echo
echo "[4/4] Installing Linux audio dependencies..."
if command -v apt-get &> /dev/null; then
    echo "Installing portaudio for Ubuntu/Debian..."
    sudo apt-get update
    sudo apt-get install -y portaudio19-dev python3-pyaudio
elif command -v dnf &> /dev/null; then
    echo "Installing portaudio for Fedora..."
    sudo dnf install -y portaudio-devel python3-pyaudio
elif command -v pacman &> /dev/null; then
    echo "Installing portaudio for Arch..."
    sudo pacman -S portaudio python-pyaudio
elif command -v brew &> /dev/null; then
    echo "Installing portaudio for macOS..."
    brew install portaudio
else
    echo "Please install portaudio manually for your system"
fi

echo
echo "Setup completed successfully!"
echo
read -p "Do you want to run the transcriber now? (y/n): " choice
if [[ $choice == [Yy]* ]]; then
    echo
    echo "Starting Albanian Teams Transcriber..."
    python3 main.py
else
    echo
    echo "To run later, use: python3 main.py"
fi
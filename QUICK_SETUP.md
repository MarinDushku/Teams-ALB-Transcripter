# Quick Setup Guide

## Windows Users
1. Double-click `setup.bat`
2. Follow the prompts
3. Install Virtual Audio Cable when prompted
4. Run the transcriber!

## Linux/Mac Users
```bash
./setup.sh
```

## Manual Steps (if needed)
```bash
# Install dependencies
pip install -r requirements.txt

# Get Albanian ASR
git clone https://github.com/florijanqosja/Albanian-ASR
cd Albanian-ASR && pip install -r requirements.txt && cd ..

# Run transcriber  
python main.py
```

## Audio Setup
**Windows**: Install [Virtual Audio Cable](https://vac.muzychenko.net/en/) (free)
**Linux**: Audio dependencies installed automatically
**Mac**: Use built-in audio routing

## Troubleshooting
- Ensure Python 3.8+ is installed
- Make sure git is available
- Check Teams is running during transcription
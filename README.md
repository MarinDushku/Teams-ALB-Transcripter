# Albanian Teams Transcriber

Real-time transcription app for Microsoft Teams meetings with Albanian language support.

## Features

✅ **Automatic Teams Detection** - Starts when Teams meeting begins  
✅ **Real-Time Albanian Transcription** - Text appears as people speak  
✅ **Speaker Identification** - Different colors/labels for each speaker  
✅ **Live Display** - Scrolling transcript window  
✅ **Auto-Save** - Continuous saving to file  
✅ **Export Options** - Save as Word, text, or JSON files  

## Installation

### 1. Clone/Download the Project
```bash
git clone <repository-url>
cd Teams-Transcripter
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Albanian ASR Model
```bash
# Clone the Albanian ASR project
git clone https://github.com/florijanqosja/Albanian-ASR
cd Albanian-ASR
pip install -r requirements.txt
cd ..
```

### 4. System Audio Setup (Windows)
- Install Virtual Audio Cable (free) to route Teams audio
- Configure audio routing from Teams to the transcriber
- Alternative: Use Windows WASAPI loopback (built-in)

### 5. Linux Audio Setup
```bash
# Install additional dependencies for Linux
sudo apt-get install portaudio19-dev python3-pyaudio
```

## Usage

### Automatic Mode (Default)
Automatically starts transcription when Teams meeting is detected:
```bash
python main.py
# or
python main.py auto
```

### Manual Mode
User controls transcription via UI:
```bash
python main.py manual
```

### Help
```bash
python main.py help
```

## How It Works

1. **Audio Capture**: Captures system audio output (Teams speakers) using PyAudio
2. **Teams Detection**: Automatically detects when Teams meeting is active
3. **Speech Recognition**: Processes audio with Albanian ASR model
4. **Speaker Identification**: Identifies different speakers using voice characteristics
5. **Live Display**: Shows real-time transcript with speaker labels and timestamps
6. **Export**: Saves transcript in multiple formats

## Technical Architecture

```
Teams Audio → System Audio Capture → Audio Chunks → Albanian ASR → Speaker ID → Live Display
```

### Core Components

- **TeamsAudioCapture**: System audio capture using PyAudio/WASAPI
- **AlbanianRealTimeTranscriber**: Albanian speech recognition
- **TeamsDetector**: Automatic Teams meeting detection
- **SpeakerIdentifier**: Voice-based speaker diarization
- **LiveTranscriptUI**: Real-time transcript display interface

## Configuration

### Audio Settings
- Sample Rate: 16kHz (optimized for speech recognition)
- Channels: Stereo
- Buffer Size: 1024 frames
- Processing Window: 2-3 seconds for real-time transcription

### Speaker Identification
- Sensitivity can be adjusted in `speaker_identifier.py`
- Uses energy, zero-crossing rate, and spectral features
- Automatic speaker profile learning

## Export Formats

- **Text (.txt)**: Plain text transcript with timestamps
- **JSON (.json)**: Structured data with metadata
- **Word (.docx)**: Formatted document (requires python-docx)

## Troubleshooting

### Common Issues

**Audio Not Detected**
- Check Windows audio settings
- Ensure Virtual Audio Cable is installed and configured
- Verify Teams audio output device

**Teams Not Detected**
- Make sure Teams process is running
- Check if Teams meeting window is active
- Monitor CPU usage by Teams processes

**Transcription Quality**
- Ensure clear audio input
- Check microphone/speaker quality
- Adjust speaker sensitivity settings

**Dependencies Issues**
```bash
# Reinstall audio dependencies
pip uninstall pyaudio pyaudiowpatch
pip install pyaudio pyaudiowpatch

# For Windows
pip install pywin32

# For Linux
sudo apt-get install python3-tk
```

### Performance Optimization

- Close unnecessary applications
- Use dedicated audio hardware
- Adjust buffer sizes for your system
- Monitor CPU and memory usage

## Development

### Project Structure
```
Teams-Transcripter/
├── main.py                    # Main application entry point
├── audio_capture.py           # System audio capture
├── albanian_transcriber.py    # Albanian speech recognition
├── teams_detector.py          # Teams meeting detection
├── speaker_identifier.py     # Speaker diarization
├── live_transcript_ui.py      # User interface
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Adding New Features

1. **Custom Language Models**: Integrate additional ASR models in `albanian_transcriber.py`
2. **Enhanced Speaker ID**: Improve speaker identification algorithms
3. **Cloud Integration**: Add cloud storage for transcripts
4. **Meeting Analytics**: Add meeting statistics and insights

## Cost Information

### Free Setup
- Albanian-ASR (open source)
- PyAudio for system audio capture
- Basic speaker detection
- Local processing only
- **Cost: $0**

### Enhanced Setup (Optional)
- Azure Speech Service for better speaker diarization (~$1-2/hour)
- Cloud storage integration
- **Estimated cost: $10-30/month for typical usage**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the GitHub issues
3. Create a new issue with detailed information

## Acknowledgments

- [Albanian-ASR](https://github.com/florijanqosja/Albanian-ASR) for Albanian speech recognition
- PyAudio for audio processing
- Microsoft Teams for meeting platform
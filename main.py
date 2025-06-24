#!/usr/bin/env python3
"""
Albanian Teams Transcriber - Main Entry Point
Beautiful real-time transcription for Microsoft Teams
"""

from working_transcriber import WorkingAlbanianTranscriber

def main():
    """Launch the Albanian Teams Transcriber"""
    print("🎭 Albanian Teams Transcriber")
    print("=" * 50)
    print("Real-time AI transcription with stunning visuals")
    print()
    
    try:
        app = WorkingAlbanianTranscriber()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Try running: python working_transcriber.py")

if __name__ == "__main__":
    main()
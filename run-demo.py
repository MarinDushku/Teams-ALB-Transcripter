#!/usr/bin/env python3
"""
Albanian Teams Transcriber - Demo Runner
Tests the UI without heavy dependencies
"""

import sys
import os

def main():
    print("🎭 Albanian Teams Transcriber")
    print("=" * 50)
    
    # Check if we have the basic packages
    try:
        import tkinter
        print("✓ GUI toolkit available")
    except ImportError:
        print("✗ tkinter not available")
        return
    
    try:
        import pyaudiowpatch
        print("✓ Audio capture available")
        has_audio = True
    except ImportError:
        print("✗ pyaudiowpatch not available - audio capture disabled")
        has_audio = False
    
    try:
        import torch
        print("✓ PyTorch available")
        has_ai = True
    except ImportError:
        print("✗ PyTorch not available - AI features disabled")
        has_ai = False
    
    print()
    
    # Try to run the UI demo first
    try:
        from ui_demo import UIDemo
        print("🚀 Starting UI Demo (no dependencies needed)")
        print("This shows the interface without requiring AI models")
        print()
        
        demo = UIDemo()
        demo.run()
        
    except Exception as e:
        print(f"UI Demo failed: {e}")
        
        # Fallback to basic tkinter test
        try:
            import tkinter as tk
            print("🔧 Starting basic interface test...")
            
            root = tk.Tk()
            root.title("Albanian Teams Transcriber - Basic Test")
            root.geometry("800x600")
            
            label = tk.Label(root, text="🎭 Albanian Teams Transcriber\n\nBasic interface test successful!\n\nYour system can run the transcriber UI.", 
                           justify='center', font=('Arial', 14))
            label.pack(expand=True)
            
            button = tk.Button(root, text="Close", command=root.quit, font=('Arial', 12))
            button.pack(pady=20)
            
            root.mainloop()
            
        except Exception as e2:
            print(f"Basic test also failed: {e2}")
            print("Your system may have GUI issues")

if __name__ == "__main__":
    main()
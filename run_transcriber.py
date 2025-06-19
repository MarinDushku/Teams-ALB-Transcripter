#!/usr/bin/env python3
"""
GUI launcher for Albanian Teams Transcriber
This script provides a user-friendly way to start the application
"""

import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
import os
import threading
import time

class TranscriberLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Albanian Teams Transcriber - Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        self.setup_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the launcher UI"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2196F3', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Albanian Teams Transcriber",
            font=("Arial", 18, "bold"),
            fg='white',
            bg='#2196F3'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Real-time Albanian transcription for Teams meetings",
            font=("Arial", 10),
            fg='white',
            bg='#2196F3'
        )
        subtitle_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Status section
        status_frame = tk.LabelFrame(content_frame, text="System Status", font=("Arial", 10, "bold"))
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.python_status = tk.Label(status_frame, text="⏳ Checking Python...", font=("Arial", 9))
        self.python_status.pack(anchor=tk.W, padx=10, pady=2)
        
        self.deps_status = tk.Label(status_frame, text="⏳ Checking dependencies...", font=("Arial", 9))
        self.deps_status.pack(anchor=tk.W, padx=10, pady=2)
        
        self.teams_status = tk.Label(status_frame, text="⏳ Checking Teams...", font=("Arial", 9))
        self.teams_status.pack(anchor=tk.W, padx=10, pady=2)
        
        # Mode selection
        mode_frame = tk.LabelFrame(content_frame, text="Launch Mode", font=("Arial", 10, "bold"))
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.mode_var = tk.StringVar(value="auto")
        
        auto_radio = tk.Radiobutton(
            mode_frame,
            text="Automatic Mode - Start transcription when Teams meeting detected",
            variable=self.mode_var,
            value="auto",
            font=("Arial", 9)
        )
        auto_radio.pack(anchor=tk.W, padx=10, pady=2)
        
        manual_radio = tk.Radiobutton(
            mode_frame,
            text="Manual Mode - User controls start/stop via interface",
            variable=self.mode_var,
            value="manual",
            font=("Arial", 9)
        )
        manual_radio.pack(anchor=tk.W, padx=10, pady=2)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.launch_btn = tk.Button(
            button_frame,
            text="Launch Transcriber",
            command=self.launch_transcriber,
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            width=20,
            height=2
        )
        self.launch_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        help_btn = tk.Button(
            button_frame,
            text="Help & Setup",
            command=self.show_help,
            font=("Arial", 10),
            bg='#2196F3',
            fg='white',
            width=15
        )
        help_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit,
            font=("Arial", 10),
            bg='#f44336',
            fg='white',
            width=10
        )
        exit_btn.pack(side=tk.RIGHT)
        
        # Start system check
        threading.Thread(target=self.check_system, daemon=True).start()
    
    def check_system(self):
        """Check system requirements"""
        # Check Python
        try:
            result = subprocess.run([sys.executable, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.python_status.config(text=f"✅ Python: {version}", fg='green')
            else:
                self.python_status.config(text="❌ Python: Not found", fg='red')
        except:
            self.python_status.config(text="❌ Python: Error checking", fg='red')
        
        # Check dependencies
        try:
            import pyaudio
            import speech_recognition
            import psutil
            self.deps_status.config(text="✅ Dependencies: All installed", fg='green')
        except ImportError as e:
            self.deps_status.config(text=f"⚠️ Dependencies: Missing {str(e).split()[-1]}", fg='orange')
        
        # Check Teams
        try:
            import psutil
            teams_running = False
            for proc in psutil.process_iter(['name']):
                if 'teams' in proc.info['name'].lower():
                    teams_running = True
                    break
            
            if teams_running:
                self.teams_status.config(text="✅ Teams: Running", fg='green')
            else:
                self.teams_status.config(text="⚠️ Teams: Not detected", fg='orange')
        except:
            self.teams_status.config(text="❓ Teams: Unable to check", fg='gray')
    
    def launch_transcriber(self):
        """Launch the main transcriber application"""
        try:
            mode = self.mode_var.get()
            
            # Hide launcher window
            self.root.withdraw()
            
            # Launch main application
            if os.path.exists('main.py'):
                subprocess.Popen([sys.executable, 'main.py', mode])
            else:
                messagebox.showerror("Error", "main.py not found in current directory")
                self.root.deiconify()
                return
            
            # Close launcher after a delay
            self.root.after(2000, self.root.quit)
            
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch transcriber:\n{e}")
            self.root.deiconify()
    
    def show_help(self):
        """Show help and setup information"""
        help_text = """
Albanian Teams Transcriber - Setup Guide

REQUIREMENTS:
• Python 3.7 or higher
• Microsoft Teams
• Audio input/output devices

INSTALLATION:
1. Install Python from python.org
2. Run: pip install -r requirements.txt
3. For Albanian ASR: 
   git clone https://github.com/florijanqosja/Albanian-ASR

AUDIO SETUP:
• Windows: Install Virtual Audio Cable for system audio capture
• Linux: Install portaudio19-dev
• Make sure Teams audio is working

USAGE:
• Automatic Mode: Starts transcription when Teams meeting detected
• Manual Mode: User controls via Start/Stop buttons
• Transcripts are saved automatically
• Export options: TXT, JSON, DOCX

TROUBLESHOOTING:
• If audio not detected: Check audio devices and Virtual Audio Cable
• If Teams not detected: Make sure Teams is running and in a meeting
• For permission errors: Run as administrator (Windows)

For more help, check README.md
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help & Setup Guide")
        help_window.geometry("600x500")
        help_window.configure(bg='white')
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, font=("Arial", 10))
        scrollbar = ttk.Scrollbar(help_window, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
    
    def run(self):
        """Start the launcher"""
        self.root.mainloop()

if __name__ == "__main__":
    launcher = TranscriberLauncher()
    launcher.run()
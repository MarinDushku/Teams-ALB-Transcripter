#!/usr/bin/env python3
"""
Albanian Teams Transcriber - Beautiful UI
Ultra-modern interface with stunning visuals and animations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import json
from datetime import datetime
import math
import time
import random

class LiveTranscriptUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎭 Albanian Teams Transcriber - Ultra Edition")
        self.window.geometry("1600x1000")
        self.window.minsize(1200, 700)
        self.window.configure(bg='#0d1117')
        
        # Center window
        self.center_window()
        
        # Beautiful themes
        self.themes = {
            'dark': {
                'bg_primary': '#0d1117',
                'bg_secondary': '#161b22', 
                'bg_tertiary': '#21262d',
                'text_primary': '#f0f6fc',
                'text_secondary': '#c9d1d9',
                'accent_primary': '#58a6ff',
                'accent_secondary': '#ff7b72',
                'success': '#3fb950',
                'warning': '#d29922',
                'error': '#f85149'
            },
            'light': {
                'bg_primary': '#ffffff',
                'bg_secondary': '#f8f9fa',
                'bg_tertiary': '#e9ecef',
                'text_primary': '#212529',
                'text_secondary': '#495057',
                'accent_primary': '#0d6efd',
                'accent_secondary': '#dc3545',
                'success': '#198754',
                'warning': '#fd7e14',
                'error': '#dc3545'
            }
        }
        
        self.current_theme = 'dark'
        self.theme = self.themes[self.current_theme]
        
        # Beautiful speaker colors
        self.speaker_colors = [
            {'primary': '#ff79c6', 'avatar': '👤'},
            {'primary': '#50fa7b', 'avatar': '🎭'},
            {'primary': '#ffb86c', 'avatar': '🌟'},
            {'primary': '#ff5555', 'avatar': '💫'},
            {'primary': '#8be9fd', 'avatar': '✨'},
            {'primary': '#f1fa8c', 'avatar': '🎨'},
        ]
        
        # Data
        self.transcript_data = []
        self.is_recording = False
        self.participants = {}
        self._total_words = 0
        
        # Setup UI
        self.setup_ui()
        
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Setup the beautiful user interface"""
        # Main container
        main_frame = tk.Frame(self.window, bg=self.theme['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.theme['bg_secondary'], height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎭 Albanian Teams Transcriber",
            font=("Segoe UI", 24, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        title_label.pack(pady=20)
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg=self.theme['bg_tertiary'], height=80)
        control_frame.pack(fill='x', pady=(0, 20))
        control_frame.pack_propagate(False)
        
        btn_frame = tk.Frame(control_frame, bg=self.theme['bg_tertiary'])
        btn_frame.pack(expand=True)
        
        # Start/Stop button
        self.start_stop_btn = tk.Button(
            btn_frame,
            text="🎙️ Start Transcription",
            command=self.toggle_transcription,
            font=("Segoe UI", 14, "bold"),
            bg=self.theme['success'],
            fg='white',
            relief='flat',
            padx=30,
            pady=12
        )
        self.start_stop_btn.pack(side='left', padx=10, pady=20)
        
        # Export button
        export_btn = tk.Button(
            btn_frame,
            text="💾 Export",
            command=self.export_transcript,
            font=("Segoe UI", 14),
            bg=self.theme['accent_primary'],
            fg='white',
            relief='flat',
            padx=30,
            pady=12
        )
        export_btn.pack(side='left', padx=10, pady=20)
        
        # Clear button
        clear_btn = tk.Button(
            btn_frame,
            text="🗑️ Clear",
            command=self.clear_transcript,
            font=("Segoe UI", 14),
            bg=self.theme['warning'],
            fg='white',
            relief='flat',
            padx=30,
            pady=12
        )
        clear_btn.pack(side='left', padx=10, pady=20)
        
        # Status
        self.status_label = tk.Label(
            btn_frame,
            text="● Ready",
            font=("Segoe UI", 12, "bold"),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_tertiary']
        )
        self.status_label.pack(side='right', padx=20, pady=20)
        
        # Main content
        content_frame = tk.Frame(main_frame, bg=self.theme['bg_primary'])
        content_frame.pack(fill='both', expand=True)
        
        # Transcript area
        transcript_frame = tk.Frame(content_frame, bg=self.theme['bg_secondary'])
        transcript_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        transcript_label = tk.Label(
            transcript_frame,
            text="📝 Live Transcript",
            font=("Segoe UI", 16, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        transcript_label.pack(pady=10)
        
        self.transcript_area = scrolledtext.ScrolledText(
            transcript_frame,
            font=("Consolas", 11),
            bg=self.theme['bg_tertiary'],
            fg=self.theme['text_primary'],
            relief='flat',
            borderwidth=0,
            wrap='word'
        )
        self.transcript_area.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Configure text tags for speaker colors
        for i, color in enumerate(self.speaker_colors):
            self.transcript_area.tag_config(f'speaker_{i}', foreground=color['primary'], font=("Consolas", 11, "bold"))
        
        # Side panel
        side_frame = tk.Frame(content_frame, bg=self.theme['bg_secondary'], width=300)
        side_frame.pack(side='right', fill='y')
        side_frame.pack_propagate(False)
        
        # Statistics
        stats_label = tk.Label(
            side_frame,
            text="📊 Session Stats",
            font=("Segoe UI", 16, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        stats_label.pack(pady=10)
        
        stats_frame = tk.Frame(side_frame, bg=self.theme['bg_tertiary'])
        stats_frame.pack(fill='x', padx=10, pady=(0, 20))
        
        # Word count
        word_frame = tk.Frame(stats_frame, bg=self.theme['bg_tertiary'])
        word_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(word_frame, text="Words:", font=("Segoe UI", 10), 
                fg=self.theme['text_secondary'], bg=self.theme['bg_tertiary']).pack(side='left')
        
        self.word_count_var = tk.StringVar(value="0")
        tk.Label(word_frame, textvariable=self.word_count_var, font=("Segoe UI", 10, "bold"),
                fg=self.theme['accent_primary'], bg=self.theme['bg_tertiary']).pack(side='right')
        
        # Confidence
        conf_frame = tk.Frame(stats_frame, bg=self.theme['bg_tertiary'])
        conf_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(conf_frame, text="Confidence:", font=("Segoe UI", 10),
                fg=self.theme['text_secondary'], bg=self.theme['bg_tertiary']).pack(side='left')
        
        self.confidence_var = tk.StringVar(value="0%")
        tk.Label(conf_frame, textvariable=self.confidence_var, font=("Segoe UI", 10, "bold"),
                fg=self.theme['success'], bg=self.theme['bg_tertiary']).pack(side='right')
    
    def toggle_transcription(self):
        """Toggle transcription state"""
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.start_stop_btn.config(text="⏹️ Stop Transcription", bg=self.theme['error'])
            self.status_label.config(text="● Recording", fg=self.theme['success'])
        else:
            self.start_stop_btn.config(text="🎙️ Start Transcription", bg=self.theme['success'])
            self.status_label.config(text="● Stopped", fg=self.theme['warning'])
    
    def add_transcript_entry(self, speaker, text, timestamp):
        """Add entry to transcript with beautiful formatting"""
        # Add to data
        entry = {
            'speaker': speaker,
            'text': text,
            'timestamp': timestamp.strftime("%H:%M:%S") if isinstance(timestamp, datetime) else str(timestamp)
        }
        self.transcript_data.append(entry)
        
        # Update UI
        self.transcript_area.config(state=tk.NORMAL)
        
        # Speaker header
        speaker_idx = hash(speaker) % len(self.speaker_colors)
        avatar = self.speaker_colors[speaker_idx]['avatar']
        
        header = f"\n{avatar} {speaker}\n"
        self.transcript_area.insert(tk.END, header, f'speaker_{speaker_idx}')
        
        # Timestamp and text
        time_text = f"[{entry['timestamp']}] "
        self.transcript_area.insert(tk.END, time_text, 'timestamp')
        self.transcript_area.insert(tk.END, f"{text}\n", 'content')
        
        self.transcript_area.see(tk.END)
        self.transcript_area.config(state=tk.DISABLED)
    
    def clear_transcript(self):
        """Clear transcript with confirmation"""
        if messagebox.askyesno("Clear Transcript", "Clear all transcript data?"):
            self.transcript_area.config(state=tk.NORMAL)
            self.transcript_area.delete(1.0, tk.END)
            self.transcript_area.config(state=tk.DISABLED)
            self.transcript_data.clear()
            self._total_words = 0
            self.word_count_var.set("0")
    
    def export_transcript(self):
        """Export transcript to file"""
        if not self.transcript_data:
            messagebox.showinfo("Export", "No transcript data to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Transcript",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.transcript_data, f, indent=2, ensure_ascii=False)
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("🎭 Albanian Teams Transcriber - Transcript\n")
                        f.write("=" * 50 + "\n\n")
                        for entry in self.transcript_data:
                            f.write(f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}\n")
                
                messagebox.showinfo("Export Complete", f"Transcript saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {e}")
    
    def update_session_stats(self, word_count=0, confidence=0):
        """Update session statistics"""
        try:
            self._total_words += word_count
            self.word_count_var.set(str(self._total_words))
            
            if confidence > 0:
                self.confidence_var.set(f"{confidence:.0f}%")
        except Exception as e:
            print(f"Stats update error: {e}")
    
    def run(self):
        """Start the beautiful UI"""
        self.window.mainloop()
    
    def destroy(self):
        """Close the window"""
        self.window.destroy()

if __name__ == "__main__":
    ui = LiveTranscriptUI()
    ui.run()
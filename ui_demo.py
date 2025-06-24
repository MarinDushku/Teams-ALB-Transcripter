#!/usr/bin/env python3
"""
Albanian Teams Transcriber - UI Demo
Standalone demo to preview the UI without dependencies
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
from datetime import datetime

class UIDemo:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎭 Albanian Teams Transcriber - UI Demo")
        self.window.geometry("1600x1000")
        self.window.minsize(1200, 700)
        self.window.configure(bg='#0d1117')
        
        # Center window
        self.center_window()
        
        # Theme colors
        self.theme = {
            'bg_primary': '#0d1117',
            'bg_secondary': '#161b22', 
            'bg_tertiary': '#21262d',
            'text_primary': '#f0f6fc',
            'text_secondary': '#c9d1d9',
            'accent_primary': '#58a6ff',
            'accent_secondary': '#ff7b72',
            'success': '#3fb950',
            'warning': '#d29922',
        }
        
        # Demo data
        self.demo_speakers = [
            {'name': 'Marin', 'color': '#ff79c6', 'avatar': '👤'},
            {'name': 'Andi', 'color': '#50fa7b', 'avatar': '🎭'},
            {'name': 'Elsa', 'color': '#ffb86c', 'avatar': '🌟'},
        ]
        
        self.demo_transcript = [
            {'speaker': 'Marin', 'text': 'Mirëdita të gjithëve! Si jeni sot?', 'time': '14:30:15'},
            {'speaker': 'Andi', 'text': 'Mirë jam, faleminderit! A fillojmë mbledhjen?', 'time': '14:30:22'},
            {'speaker': 'Elsa', 'text': 'Po, le të diskutojmë për projektin e ri.', 'time': '14:30:28'},
            {'speaker': 'Marin', 'text': 'Kemi bërë progres të mirë këtë javë.', 'time': '14:30:35'},
        ]
        
        self.is_demo_running = False
        self.setup_ui()
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        # Main container with gradient effect
        main_frame = tk.Frame(self.window, bg=self.theme['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with beautiful title
        header_frame = tk.Frame(main_frame, bg=self.theme['bg_secondary'], height=100)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎭 Albanian Teams Transcriber",
            font=("Segoe UI", 28, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Ultra Modern Real-time Transcription • AI-Powered • Beautiful Design",
            font=("Segoe UI", 12),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary']
        )
        subtitle_label.pack()
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg=self.theme['bg_tertiary'], height=80)
        control_frame.pack(fill='x', pady=(0, 20))
        control_frame.pack_propagate(False)
        
        # Buttons with modern styling
        btn_frame = tk.Frame(control_frame, bg=self.theme['bg_tertiary'])
        btn_frame.pack(expand=True)
        
        self.start_btn = tk.Button(
            btn_frame,
            text="🚀 Start Demo",
            command=self.toggle_demo,
            font=("Segoe UI", 14, "bold"),
            bg=self.theme['success'],
            fg='white',
            relief='flat',
            padx=30,
            pady=10
        )
        self.start_btn.pack(side='left', padx=10, pady=20)
        
        export_btn = tk.Button(
            btn_frame,
            text="💾 Export",
            font=("Segoe UI", 14),
            bg=self.theme['accent_primary'],
            fg='white',
            relief='flat',
            padx=30,
            pady=10,
            command=self.show_export_options
        )
        export_btn.pack(side='left', padx=10, pady=20)
        
        settings_btn = tk.Button(
            btn_frame,
            text="⚙️ Settings",
            font=("Segoe UI", 14),
            bg=self.theme['warning'],
            fg='white',
            relief='flat',
            padx=30,
            pady=10,
            command=self.show_settings
        )
        settings_btn.pack(side='left', padx=10, pady=20)
        
        # Status indicator
        self.status_label = tk.Label(
            btn_frame,
            text="● Ready",
            font=("Segoe UI", 12, "bold"),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_tertiary']
        )
        self.status_label.pack(side='right', padx=20, pady=20)
        
        # Main content area
        content_frame = tk.Frame(main_frame, bg=self.theme['bg_primary'])
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - Transcript
        left_frame = tk.Frame(content_frame, bg=self.theme['bg_secondary'])
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        transcript_header = tk.Label(
            left_frame,
            text="📝 Live Transcript",
            font=("Segoe UI", 16, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        transcript_header.pack(pady=10)
        
        # Transcript area with custom styling
        self.transcript_text = scrolledtext.ScrolledText(
            left_frame,
            font=("Consolas", 11),
            bg=self.theme['bg_tertiary'],
            fg=self.theme['text_primary'],
            insertbackground=self.theme['accent_primary'],
            relief='flat',
            borderwidth=0,
            wrap='word'
        )
        self.transcript_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Right panel - Info
        right_frame = tk.Frame(content_frame, bg=self.theme['bg_secondary'], width=350)
        right_frame.pack(side='right', fill='y', padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Speakers panel
        speakers_header = tk.Label(
            right_frame,
            text="👥 Active Speakers",
            font=("Segoe UI", 16, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        speakers_header.pack(pady=10)
        
        self.speakers_frame = tk.Frame(right_frame, bg=self.theme['bg_secondary'])
        self.speakers_frame.pack(fill='x', padx=10)
        
        for speaker in self.demo_speakers:
            speaker_item = tk.Frame(self.speakers_frame, bg=self.theme['bg_tertiary'])
            speaker_item.pack(fill='x', pady=5)
            
            tk.Label(
                speaker_item,
                text=f"{speaker['avatar']} {speaker['name']}",
                font=("Segoe UI", 12, "bold"),
                fg=speaker['color'],
                bg=self.theme['bg_tertiary']
            ).pack(side='left', padx=10, pady=8)
            
        # Stats panel
        stats_header = tk.Label(
            right_frame,
            text="📊 Session Stats",
            font=("Segoe UI", 16, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        stats_header.pack(pady=(30, 10))
        
        stats_frame = tk.Frame(right_frame, bg=self.theme['bg_tertiary'])
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.stats_labels = {}
        stats = [
            ('Duration', '00:00:00'),
            ('Words', '0'),
            ('Speakers', '0'),
            ('Confidence', '0%')
        ]
        
        for stat, value in stats:
            row = tk.Frame(stats_frame, bg=self.theme['bg_tertiary'])
            row.pack(fill='x', padx=10, pady=5)
            
            tk.Label(
                row,
                text=stat + ':',
                font=("Segoe UI", 10),
                fg=self.theme['text_secondary'],
                bg=self.theme['bg_tertiary']
            ).pack(side='left')
            
            self.stats_labels[stat] = tk.Label(
                row,
                text=value,
                font=("Segoe UI", 10, "bold"),
                fg=self.theme['accent_primary'],
                bg=self.theme['bg_tertiary']
            )
            self.stats_labels[stat].pack(side='right')
    
    def toggle_demo(self):
        if not self.is_demo_running:
            self.start_demo()
        else:
            self.stop_demo()
    
    def start_demo(self):
        self.is_demo_running = True
        self.start_btn.config(text="⏹️ Stop Demo", bg=self.theme['accent_secondary'])
        self.status_label.config(text="● Recording", fg=self.theme['success'])
        
        # Clear transcript
        self.transcript_text.delete(1.0, tk.END)
        
        # Start demo thread
        threading.Thread(target=self.run_demo, daemon=True).start()
    
    def stop_demo(self):
        self.is_demo_running = False
        self.start_btn.config(text="🚀 Start Demo", bg=self.theme['success'])
        self.status_label.config(text="● Stopped", fg=self.theme['text_secondary'])
    
    def run_demo(self):
        word_count = 0
        start_time = time.time()
        
        for i, entry in enumerate(self.demo_transcript):
            if not self.is_demo_running:
                break
                
            # Simulate typing effect
            speaker = entry['speaker']
            text = entry['text']
            speaker_color = next(s['color'] for s in self.demo_speakers if s['name'] == speaker)
            
            # Add timestamp and speaker
            timestamp = datetime.now().strftime("%H:%M:%S")
            header = f"[{timestamp}] {speaker}: "
            
            self.transcript_text.insert(tk.END, header, f"speaker_{speaker}")
            self.transcript_text.tag_config(f"speaker_{speaker}", foreground=speaker_color, font=("Segoe UI", 11, "bold"))
            
            # Type out the text
            for char in text:
                if not self.is_demo_running:
                    break
                self.transcript_text.insert(tk.END, char)
                self.transcript_text.see(tk.END)
                self.window.update()
                time.sleep(0.05)  # Typing speed
            
            self.transcript_text.insert(tk.END, "\n\n")
            self.transcript_text.see(tk.END)
            
            # Update stats
            word_count += len(text.split())
            duration = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
            
            self.stats_labels['Duration'].config(text=duration)
            self.stats_labels['Words'].config(text=str(word_count))
            self.stats_labels['Speakers'].config(text=str(len(self.demo_speakers)))
            self.stats_labels['Confidence'].config(text=f"{random.randint(85, 98)}%")
            
            # Wait before next message
            time.sleep(2)
        
        # Auto stop when demo finishes
        if self.is_demo_running:
            self.stop_demo()
    
    def show_export_options(self):
        messagebox.showinfo("Export Options", 
            "Available export formats:\n\n" +
            "• 📄 Plain Text (.txt)\n" +
            "• 📊 JSON with metadata (.json)\n" +
            "• 📝 Word Document (.docx)\n" +
            "• 📋 Rich Text Format (.rtf)")
    
    def show_settings(self):
        messagebox.showinfo("Settings", 
            "Configuration options:\n\n" +
            "• 🎤 Audio input settings\n" +
            "• 🎨 Theme customization\n" +
            "• 👥 Speaker identification\n" +
            "• 🔧 Advanced AI parameters\n" +
            "• 💾 Auto-save preferences")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    print("🎭 Albanian Teams Transcriber - UI Demo")
    print("This is a standalone demo to preview the interface")
    print("No heavy AI libraries required!")
    print()
    
    demo = UIDemo()
    demo.run()
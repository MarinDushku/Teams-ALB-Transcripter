import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import json
from datetime import datetime
import math
import time

class ModernTranscriptUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Albanian Teams Transcriber - Modern UI")
        self.window.geometry("1400x900")
        self.window.minsize(1000, 600)
        
        # Modern color schemes
        self.themes = {
            'dark': {
                'bg_primary': '#1e1e2e',
                'bg_secondary': '#313244', 
                'bg_tertiary': '#45475a',
                'text_primary': '#cdd6f4',
                'text_secondary': '#bac2de',
                'accent': '#89b4fa',
                'accent_hover': '#74c7ec',
                'success': '#a6e3a1',
                'warning': '#f9e2af',
                'error': '#f38ba8',
                'border': '#6c7086'
            },
            'light': {
                'bg_primary': '#ffffff',
                'bg_secondary': '#f8f9fa',
                'bg_tertiary': '#e9ecef',
                'text_primary': '#212529',
                'text_secondary': '#495057',
                'accent': '#0d6efd',
                'accent_hover': '#0b5ed7',
                'success': '#198754',
                'warning': '#fd7e14',
                'error': '#dc3545',
                'border': '#dee2e6'
            }
        }
        
        self.current_theme = 'dark'
        self.theme = self.themes[self.current_theme]
        
        # Configure window
        self.window.configure(bg=self.theme['bg_primary'])
        
        # Speaker colors with more variety
        self.speaker_colors = {
            "Speaker 1": "#89b4fa",  # Blue
            "Speaker 2": "#a6e3a1",  # Green
            "Speaker 3": "#f38ba8",  # Red
            "Speaker 4": "#fab387",  # Orange
            "Speaker 5": "#cba6f7",  # Purple
            "Speaker 6": "#f9e2af",  # Yellow
            "Speaker 7": "#74c7ec",  # Cyan
            "Speaker 8": "#eba0ac",  # Pink
        }
        
        # Animation variables
        self.animation_running = False
        self.pulse_alpha = 0
        
        # Transcript data
        self.transcript_data = []
        self.is_recording = False
        self.participants = {}
        
        # Setup modern UI
        self.setup_modern_ui()
        
        # Setup animations
        self.start_animations()
        
    def setup_modern_ui(self):
        """Setup modern, beautiful UI"""
        # Create main container with padding
        main_container = tk.Frame(self.window, bg=self.theme['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=self.theme['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left panel (controls and info)
        left_panel = tk.Frame(content_frame, bg=self.theme['bg_secondary'], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Right panel (transcript)
        right_panel = tk.Frame(content_frame, bg=self.theme['bg_secondary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Setup panels
        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)
        
        # Setup callbacks
        self.start_callback = None
        self.stop_callback = None
    
    def create_header(self, parent):
        """Create modern header with title and controls"""
        header_frame = tk.Frame(parent, bg=self.theme['bg_primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Left side - Logo and title
        left_header = tk.Frame(header_frame, bg=self.theme['bg_primary'])
        left_header.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Modern title with gradient effect simulation
        title_frame = tk.Frame(left_header, bg=self.theme['bg_primary'])
        title_frame.pack(expand=True, fill=tk.BOTH)
        
        # Main title
        self.title_label = tk.Label(
            title_frame,
            text="🎙️ Albanian Teams Transcriber",
            font=("Segoe UI", 28, "bold"),
            fg=self.theme['accent'],
            bg=self.theme['bg_primary']
        )
        self.title_label.pack(anchor=tk.W, pady=(10, 0))
        
        # Subtitle
        self.subtitle_label = tk.Label(
            title_frame,
            text="Real-time AI-powered transcription with participant recognition",
            font=("Segoe UI", 12),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_primary']
        )
        self.subtitle_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Right side - Theme toggle and settings
        right_header = tk.Frame(header_frame, bg=self.theme['bg_primary'])
        right_header.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Theme toggle button
        self.theme_btn = self.create_modern_button(
            right_header,
            text="🌙" if self.current_theme == 'light' else "☀️",
            command=self.toggle_theme,
            width=50,
            style='accent'
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=(10, 0), pady=20)
        
        # Settings button
        self.settings_btn = self.create_modern_button(
            right_header,
            text="⚙️",
            command=self.show_settings,
            width=50,
            style='secondary'
        )
        self.settings_btn.pack(side=tk.RIGHT, padx=(10, 0), pady=20)
    
    def create_modern_button(self, parent, text, command=None, width=None, style='primary'):
        """Create a modern styled button"""
        if style == 'primary':
            bg_color = self.theme['accent']
            fg_color = '#ffffff'
            hover_color = self.theme['accent_hover']
        elif style == 'secondary':
            bg_color = self.theme['bg_tertiary']
            fg_color = self.theme['text_primary']
            hover_color = self.theme['border']
        elif style == 'accent':
            bg_color = self.theme['accent']
            fg_color = '#ffffff'
            hover_color = self.theme['accent_hover']
        elif style == 'success':
            bg_color = self.theme['success']
            fg_color = '#ffffff'
            hover_color = self.theme['success']
        elif style == 'error':
            bg_color = self.theme['error']
            fg_color = '#ffffff'
            hover_color = self.theme['error']
        else:
            bg_color = self.theme['bg_tertiary']
            fg_color = self.theme['text_primary']
            hover_color = self.theme['border']
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=bg_color,
            fg=fg_color,
            activebackground=hover_color,
            activeforeground=fg_color,
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        
        if width:
            button.config(width=width)
        
        # Add hover effects
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=bg_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def setup_left_panel(self, parent):
        """Setup the left control panel"""
        # Add padding to the panel
        panel_content = tk.Frame(parent, bg=self.theme['bg_secondary'])
        panel_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Recording controls section
        controls_section = self.create_section(panel_content, "🎮 Recording Controls")
        
        # Main record button with modern styling
        self.record_btn_frame = tk.Frame(controls_section, bg=self.theme['bg_secondary'])
        self.record_btn_frame.pack(fill=tk.X, pady=(10, 20))
        
        self.start_stop_btn = self.create_modern_button(
            self.record_btn_frame,
            text="🎙️ Start Transcription",
            command=self.toggle_transcription,
            style='success'
        )
        self.start_stop_btn.pack(fill=tk.X)
        
        # Secondary buttons
        button_frame = tk.Frame(controls_section, bg=self.theme['bg_secondary'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.clear_btn = self.create_modern_button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_transcript,
            style='secondary'
        )
        self.clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.export_btn = self.create_modern_button(
            button_frame,
            text="💾 Export",
            command=self.export_transcript,
            style='secondary'
        )
        self.export_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Status section
        status_section = self.create_section(panel_content, "📊 Status")
        
        # Recording status with animated indicator
        self.status_frame = tk.Frame(status_section, bg=self.theme['bg_secondary'])
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_indicator = tk.Label(
            self.status_frame,
            text="⚫",
            font=("Segoe UI", 16),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary']
        )
        self.status_indicator.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready to start",
            font=("Segoe UI", 10, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Teams detection status
        self.teams_frame = tk.Frame(status_section, bg=self.theme['bg_secondary'])
        self.teams_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.teams_indicator = tk.Label(
            self.teams_frame,
            text="📱",
            font=("Segoe UI", 14),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary']
        )
        self.teams_indicator.pack(side=tk.LEFT)
        
        self.teams_label = tk.Label(
            self.teams_frame,
            text="Teams: Not detected",
            font=("Segoe UI", 10),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary']
        )
        self.teams_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Participants section
        participants_section = self.create_section(panel_content, "👥 Participants")
        
        # Participants list with modern styling
        self.participants_frame = tk.Frame(participants_section, bg=self.theme['bg_tertiary'])
        self.participants_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Participants scroll area
        participants_scroll = tk.Frame(self.participants_frame, bg=self.theme['bg_tertiary'])
        participants_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.participants_label = tk.Label(
            participants_scroll,
            text="No participants detected yet",
            font=("Segoe UI", 9),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_tertiary'],
            wraplength=280,
            justify=tk.LEFT
        )
        self.participants_label.pack(anchor=tk.W)
        
        # Statistics section
        stats_section = self.create_section(panel_content, "📈 Statistics")
        
        self.stats_label = tk.Label(
            stats_section,
            text="Speakers: 0 | Duration: 0:00 | Words: 0",
            font=("Segoe UI", 9),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary'],
            wraplength=280,
            justify=tk.LEFT
        )
        self.stats_label.pack(pady=(10, 0), anchor=tk.W)
    
    def create_section(self, parent, title):
        """Create a modern section with title"""
        section_frame = tk.Frame(parent, bg=self.theme['bg_secondary'])
        section_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Section title
        title_label = tk.Label(
            section_frame,
            text=title,
            font=("Segoe UI", 12, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        title_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Section content frame
        content_frame = tk.Frame(section_frame, bg=self.theme['bg_tertiary'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        return content_frame
    
    def setup_right_panel(self, parent):
        """Setup the right transcript panel"""
        # Add padding to the panel
        panel_content = tk.Frame(parent, bg=self.theme['bg_secondary'])
        panel_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Transcript header
        transcript_header = tk.Frame(panel_content, bg=self.theme['bg_secondary'])
        transcript_header.pack(fill=tk.X, pady=(0, 15))
        
        transcript_title = tk.Label(
            transcript_header,
            text="💬 Live Transcript",
            font=("Segoe UI", 16, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        )
        transcript_title.pack(side=tk.LEFT)
        
        # Transcript controls
        transcript_controls = tk.Frame(transcript_header, bg=self.theme['bg_secondary'])
        transcript_controls.pack(side=tk.RIGHT)
        
        # Auto-scroll toggle
        self.auto_scroll_var = tk.BooleanVar(value=True)
        self.auto_scroll_cb = tk.Checkbutton(
            transcript_controls,
            text="Auto-scroll",
            variable=self.auto_scroll_var,
            font=("Segoe UI", 9),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary'],
            selectcolor=self.theme['bg_tertiary'],
            activebackground=self.theme['bg_secondary'],
            activeforeground=self.theme['text_primary']
        )
        self.auto_scroll_cb.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Transcript display with modern styling
        transcript_container = tk.Frame(panel_content, bg=self.theme['bg_tertiary'])
        transcript_container.pack(fill=tk.BOTH, expand=True)
        
        # Create custom scrolled text with modern styling
        self.transcript_area = scrolledtext.ScrolledText(
            transcript_container,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg=self.theme['bg_tertiary'],
            fg=self.theme['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=20,
            insertbackground=self.theme['accent'],
            selectbackground=self.theme['accent'],
            selectforeground='#ffffff'
        )
        self.transcript_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Configure text tags for speakers with modern colors
        for speaker, color in self.speaker_colors.items():
            tag_name = speaker.lower().replace(' ', '_')
            self.transcript_area.tag_configure(
                tag_name,
                foreground=color,
                font=("Consolas", 11, "bold")
            )
        
        # Timestamp tag
        self.transcript_area.tag_configure(
            "timestamp",
            foreground=self.theme['text_secondary'],
            font=("Consolas", 9)
        )
        
        # Confidence tag
        self.transcript_area.tag_configure(
            "confidence",
            foreground=self.theme['warning'],
            font=("Consolas", 9)
        )
        
        # Enhancement indicator tag
        self.transcript_area.tag_configure(
            "enhanced",
            foreground=self.theme['success'],
            font=("Consolas", 10)
        )
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme = self.themes[self.current_theme]
        
        # Update theme button icon
        self.theme_btn.config(text="🌙" if self.current_theme == 'light' else "☀️")
        
        # Refresh UI with new theme
        self.refresh_ui_theme()
    
    def refresh_ui_theme(self):
        """Refresh UI with current theme"""
        # This is a simplified version - in a real app you'd recursively update all widgets
        self.window.configure(bg=self.theme['bg_primary'])
        
        # Update major components
        widgets_to_update = [
            (self.title_label, {'fg': self.theme['accent'], 'bg': self.theme['bg_primary']}),
            (self.subtitle_label, {'fg': self.theme['text_secondary'], 'bg': self.theme['bg_primary']}),
            (self.status_label, {'fg': self.theme['text_primary'], 'bg': self.theme['bg_secondary']}),
            (self.teams_label, {'fg': self.theme['text_secondary'], 'bg': self.theme['bg_secondary']}),
            (self.participants_label, {'fg': self.theme['text_secondary'], 'bg': self.theme['bg_tertiary']}),
            (self.stats_label, {'fg': self.theme['text_secondary'], 'bg': self.theme['bg_secondary']}),
            (self.transcript_area, {'bg': self.theme['bg_tertiary'], 'fg': self.theme['text_primary']})
        ]
        
        for widget, config in widgets_to_update:
            try:
                widget.config(**config)
            except:
                pass
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.window)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.theme['bg_primary'])
        settings_window.transient(self.window)
        settings_window.grab_set()
        
        # Center the window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (400 // 2)
        settings_window.geometry(f"500x400+{x}+{y}")
        
        # Settings content
        settings_frame = tk.Frame(settings_window, bg=self.theme['bg_primary'])
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(
            settings_frame,
            text="⚙️ Settings",
            font=("Segoe UI", 18, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_primary']
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Settings options would go here
        tk.Label(
            settings_frame,
            text="Settings options will be available in future updates.",
            font=("Segoe UI", 10),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_primary']
        ).pack(anchor=tk.W)
    
    def start_animations(self):
        """Start UI animations"""
        self.animation_running = True
        self.animate_pulse()
    
    def animate_pulse(self):
        """Animate the recording indicator with a pulse effect"""
        if not self.animation_running:
            return
        
        if self.is_recording:
            # Pulse effect for recording indicator
            self.pulse_alpha += 0.1
            if self.pulse_alpha > 1:
                self.pulse_alpha = 0
            
            # Simple pulse simulation by changing between red shades
            if self.pulse_alpha < 0.5:
                self.status_indicator.config(text="🔴", fg="#ff4444")
            else:
                self.status_indicator.config(text="🔴", fg="#ff8888")
        
        # Schedule next frame
        self.window.after(100, self.animate_pulse)
    
    def set_callbacks(self, start_callback, stop_callback):
        """Set callback functions for start/stop actions"""
        self.start_callback = start_callback
        self.stop_callback = stop_callback
    
    def toggle_transcription(self):
        """Toggle transcription on/off"""
        if not self.is_recording:
            self.start_transcription()
        else:
            self.stop_transcription()
    
    def start_transcription(self):
        """Start transcription with modern UI updates"""
        self.is_recording = True
        
        # Update button
        self.start_stop_btn.config(
            text="⏹️ Stop Transcription",
            bg=self.theme['error']
        )
        
        # Update status
        self.status_label.config(text="Recording...", fg=self.theme['success'])
        self.status_indicator.config(text="🔴", fg="#ff4444")
        
        # Add welcome message to transcript
        self.add_system_message("🎙️ Transcription started - Listening for audio...")
        
        if self.start_callback:
            self.start_callback()
    
    def stop_transcription(self):
        """Stop transcription with modern UI updates"""
        self.is_recording = False
        
        # Update button
        self.start_stop_btn.config(
            text="🎙️ Start Transcription",
            bg=self.theme['success']
        )
        
        # Update status
        self.status_label.config(text="Stopped", fg=self.theme['text_secondary'])
        self.status_indicator.config(text="⚫", fg=self.theme['text_secondary'])
        
        # Add stop message to transcript
        self.add_system_message("⏹️ Transcription stopped")
        
        if self.stop_callback:
            self.stop_callback()
    
    def add_system_message(self, message):
        """Add a system message to the transcript"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.transcript_area.insert(tk.END, formatted_message, "timestamp")
        if self.auto_scroll_var.get():
            self.transcript_area.see(tk.END)
    
    def update_transcript(self, speaker_id, text, timestamp=None, enhanced_result=None):
        """Update transcript with modern styling"""
        if not timestamp:
            timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Handle enhanced result data
        confidence = ""
        enhanced_indicator = ""
        
        if isinstance(enhanced_result, dict):
            confidence_level = enhanced_result.get('confidence', '')
            if confidence_level and confidence_level != '?':
                confidence = f" {confidence_level}"
            
            if enhanced_result.get('enhancements_applied', False):
                enhanced_indicator = " ✨"
        
        # Add to transcript data
        entry = {
            'timestamp': timestamp,
            'speaker': speaker_id or "Unknown",
            'text': text,
            'confidence': confidence,
            'enhanced': enhanced_indicator
        }
        self.transcript_data.append(entry)
        
        # Format for display
        self.transcript_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Speaker name with color
        speaker_tag = (speaker_id or "unknown").lower().replace(' ', '_')
        display_speaker = speaker_id or "Unknown"
        
        # If speaker is in our color scheme, use colored tag
        if any(speaker_key.lower().replace(' ', '_') == speaker_tag for speaker_key in self.speaker_colors.keys()):
            self.transcript_area.insert(tk.END, f"{display_speaker}: ", speaker_tag)
        else:
            # Use a default color for unknown speakers
            self.transcript_area.insert(tk.END, f"{display_speaker}: ", "timestamp")
        
        # Text content
        self.transcript_area.insert(tk.END, text)
        
        # Confidence indicator
        if confidence:
            self.transcript_area.insert(tk.END, confidence, "confidence")
        
        # Enhancement indicator
        if enhanced_indicator:
            self.transcript_area.insert(tk.END, enhanced_indicator, "enhanced")
        
        self.transcript_area.insert(tk.END, "\n")
        
        # Auto-scroll if enabled
        if self.auto_scroll_var.get():
            self.transcript_area.see(tk.END)
        
        # Update statistics
        self.update_statistics()
    
    def update_participants(self, participants):
        """Update participants display"""
        self.participants = participants
        
        if participants:
            participant_list = []
            for name, info in participants.items():
                method = info.get('detection_method', 'unknown')
                confidence = info.get('confidence', 'unknown')
                participant_list.append(f"👤 {name}")
                if method != 'unknown':
                    participant_list.append(f"   📍 {method} ({confidence})")
            
            participant_text = "\n".join(participant_list)
            self.participants_label.config(
                text=participant_text,
                fg=self.theme['text_primary']
            )
        else:
            self.participants_label.config(
                text="No participants detected yet",
                fg=self.theme['text_secondary']
            )
    
    def update_teams_status(self, is_detected, reason=""):
        """Update Teams detection status with modern indicators"""
        if is_detected:
            self.teams_indicator.config(text="📱", fg=self.theme['success'])
            self.teams_label.config(
                text=f"Teams: Connected ({reason})",
                fg=self.theme['success']
            )
        else:
            self.teams_indicator.config(text="📱", fg=self.theme['text_secondary'])
            self.teams_label.config(
                text="Teams: Not detected",
                fg=self.theme['text_secondary']
            )
    
    def update_statistics(self):
        """Update statistics display"""
        speakers = set(entry['speaker'] for entry in self.transcript_data)
        total_words = sum(len(entry['text'].split()) for entry in self.transcript_data)
        
        # Calculate duration (rough estimate)
        if self.transcript_data:
            first_time = datetime.strptime(self.transcript_data[0]['timestamp'], "%H:%M:%S")
            last_time = datetime.strptime(self.transcript_data[-1]['timestamp'], "%H:%M:%S")
            duration_seconds = (last_time - first_time).total_seconds()
            duration_minutes = int(duration_seconds // 60)
            duration_seconds = int(duration_seconds % 60)
            duration_str = f"{duration_minutes}:{duration_seconds:02d}"
        else:
            duration_str = "0:00"
        
        self.stats_label.config(
            text=f"Speakers: {len(speakers)} | Duration: {duration_str} | Words: {total_words}"
        )
    
    def clear_transcript(self):
        """Clear the transcript with confirmation"""
        if messagebox.askyesno("Clear Transcript", 
                              "Are you sure you want to clear the transcript?\n\nThis action cannot be undone.",
                              parent=self.window):
            self.transcript_area.delete(1.0, tk.END)
            self.transcript_data = []
            self.update_statistics()
            self.add_system_message("📝 Transcript cleared")
    
    def export_transcript(self):
        """Export transcript with modern file dialog"""
        if not self.transcript_data:
            messagebox.showwarning("Export", "No transcript data to export!", parent=self.window)
            return
        
        file_path = filedialog.asksaveasfilename(
            parent=self.window,
            title="Export Transcript",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                if file_path.endswith('.json'):
                    self.export_json(file_path)
                elif file_path.endswith('.md'):
                    self.export_markdown(file_path)
                else:
                    self.export_text(file_path)
                
                messagebox.showinfo("Export", f"Transcript exported successfully to:\n{file_path}", 
                                  parent=self.window)
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export transcript:\n{e}", 
                                   parent=self.window)
    
    def export_text(self, file_path):
        """Export as plain text"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Albanian Teams Transcriber - Transcript\n")
            f.write("=" * 50 + "\n\n")
            
            for entry in self.transcript_data:
                f.write(f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}\n")
    
    def export_json(self, file_path):
        """Export as JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                'export_time': datetime.now().isoformat(),
                'participants': self.participants,
                'transcript': self.transcript_data
            }, f, indent=2, ensure_ascii=False)
    
    def export_markdown(self, file_path):
        """Export as Markdown"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("# Albanian Teams Transcriber - Transcript\n\n")
            f.write(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            if self.participants:
                f.write("## Participants\n\n")
                for name, info in self.participants.items():
                    f.write(f"- **{name}** ({info.get('detection_method', 'unknown')})\n")
                f.write("\n")
            
            f.write("## Transcript\n\n")
            for entry in self.transcript_data:
                f.write(f"**[{entry['timestamp']}] {entry['speaker']}:** {entry['text']}\n\n")
    
    def run(self):
        """Start the modern UI"""
        self.window.mainloop()
    
    def destroy(self):
        """Close the window and stop animations"""
        self.animation_running = False
        self.window.destroy()
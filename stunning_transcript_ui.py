import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import json
from datetime import datetime
import math
import time
import random

class StunningTranscriptUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Albanian Teams Transcriber - Stunning Edition")
        self.window.geometry("1600x1000")
        self.window.minsize(1200, 700)
        
        # Remove default window decorations for custom design
        self.window.configure(bg='#0a0a0a')
        
        # Stunning color schemes with gradients
        self.themes = {
            'dark': {
                'bg_primary': '#0a0a0a',
                'bg_secondary': '#1a1a2e', 
                'bg_tertiary': '#16213e',
                'bg_quaternary': '#0f3460',
                'text_primary': '#ffffff',
                'text_secondary': '#b8c5d1',
                'text_tertiary': '#8892b0',
                'accent_primary': '#64ffda',
                'accent_secondary': '#ff6b9d',
                'accent_tertiary': '#ffd93d',
                'gradient_start': '#667eea',
                'gradient_end': '#764ba2',
                'success': '#4ecdc4',
                'warning': '#ffe66d',
                'error': '#ff6b6b',
                'shadow': '#000000',
                'glass': '#ffffff10'
            },
            'light': {
                'bg_primary': '#f8fafc',
                'bg_secondary': '#ffffff',
                'bg_tertiary': '#f1f5f9',
                'bg_quaternary': '#e2e8f0',
                'text_primary': '#1e293b',
                'text_secondary': '#475569',
                'text_tertiary': '#64748b',
                'accent_primary': '#0ea5e9',
                'accent_secondary': '#ec4899',
                'accent_tertiary': '#f59e0b',
                'gradient_start': '#3b82f6',
                'gradient_end': '#8b5cf6',
                'success': '#10b981',
                'warning': '#f59e0b',
                'error': '#ef4444',
                'shadow': '#00000020',
                'glass': '#ffffff80'
            }
        }
        
        self.current_theme = 'dark'
        self.theme = self.themes[self.current_theme]
        
        # Animation variables
        self.animation_frame = 0
        self.pulse_alpha = 0
        self.wave_offset = 0
        self.gradient_shift = 0
        self.floating_elements = []
        
        # Beautiful speaker colors with gradients
        self.speaker_colors = [
            {'primary': '#ff6b9d', 'secondary': '#c44569', 'glow': '#ff6b9d40'},
            {'primary': '#4ecdc4', 'secondary': '#26de81', 'glow': '#4ecdc440'},
            {'primary': '#ffd93d', 'secondary': '#f8b500', 'glow': '#ffd93d40'},
            {'primary': '#a8e6cf', 'secondary': '#7fcdcd', 'glow': '#a8e6cf40'},
            {'primary': '#ff8b94', 'secondary': '#ffa8a8', 'glow': '#ff8b9440'},
            {'primary': '#b4a7d6', 'secondary': '#9c88ff', 'glow': '#b4a7d640'},
            {'primary': '#ffaaa5', 'secondary': '#ff7675', 'glow': '#ffaaa540'},
            {'primary': '#6c5ce7', 'secondary': '#a29bfe', 'glow': '#6c5ce740'}
        ]
        
        # Transcript data
        self.transcript_data = []
        self.is_recording = False
        self.participants = {}
        
        # Setup stunning UI
        self.setup_stunning_ui()
        
        # Start animations
        self.start_stunning_animations()
        
    def setup_stunning_ui(self):
        """Setup the stunning, beautiful UI"""
        # Main container with gradient background
        self.main_container = tk.Canvas(
            self.window,
            bg=self.theme['bg_primary'],
            highlightthickness=0,
            relief='flat'
        )
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create gradient background
        self.create_gradient_background()
        
        # Create floating particles
        self.create_floating_particles()
        
        # Header with glassmorphism effect
        self.create_stunning_header()
        
        # Main content area with modern layout
        self.create_stunning_content()
        
        # Setup callbacks
        self.start_callback = None
        self.stop_callback = None
        
        # Bind resize event for responsive design
        self.window.bind('<Configure>', self.on_window_resize)
    
    def create_gradient_background(self):
        """Create an animated gradient background"""
        width = self.window.winfo_width() or 1600
        height = self.window.winfo_height() or 1000
        
        # Create gradient rectangles
        gradient_steps = 50
        for i in range(gradient_steps):
            # Calculate color interpolation
            ratio = i / gradient_steps
            
            # Animated gradient with shifting colors
            r1, g1, b1 = self.hex_to_rgb(self.theme['gradient_start'])
            r2, g2, b2 = self.hex_to_rgb(self.theme['gradient_end'])
            
            # Add animation offset
            animated_ratio = (ratio + self.gradient_shift) % 1.0
            
            r = int(r1 + (r2 - r1) * animated_ratio)
            g = int(g1 + (g2 - g1) * animated_ratio)
            b = int(b1 + (b2 - b1) * animated_ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            y1 = i * height / gradient_steps
            y2 = (i + 1) * height / gradient_steps
            
            self.main_container.create_rectangle(
                0, y1, width, y2,
                fill=color,
                outline="",
                tags="gradient"
            )
    
    def create_floating_particles(self):
        """Create beautiful floating particles"""
        width = self.window.winfo_width() or 1600
        height = self.window.winfo_height() or 1000
        
        # Create floating dots
        for i in range(20):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(2, 8)
            
            # Create particle with glow effect
            particle = self.main_container.create_oval(
                x-size, y-size, x+size, y+size,
                fill=self.theme['accent_primary'],
                outline=self.theme['accent_primary'],
                width=0,
                tags="particle"
            )
            
            # Store particle info for animation
            self.floating_elements.append({
                'id': particle,
                'x': x,
                'y': y,
                'size': size,
                'dx': random.uniform(-0.5, 0.5),
                'dy': random.uniform(-0.5, 0.5),
                'pulse_phase': random.uniform(0, 2 * math.pi)
            })
    
    def create_stunning_header(self):
        """Create a stunning header with glassmorphism"""
        width = self.window.winfo_width() or 1600
        
        # Header background with glassmorphism
        header_bg = self.main_container.create_rectangle(
            20, 20, width-20, 120,
            fill=self.theme['glass'],
            outline=self.theme['accent_primary'],
            width=2,
            tags="header"
        )
        
        # Add subtle shadow
        shadow = self.main_container.create_rectangle(
            25, 25, width-15, 125,
            fill=self.theme['shadow'],
            outline="",
            tags="header_shadow"
        )
        self.main_container.tag_lower(shadow)
        
        # Title with beautiful typography
        self.title_text = self.main_container.create_text(
            50, 50,
            text="🎭 Albanian Teams Transcriber",
            font=("Helvetica", 28, "bold"),
            fill=self.theme['text_primary'],
            anchor="w",
            tags="title"
        )
        
        # Animated subtitle
        self.subtitle_text = self.main_container.create_text(
            50, 85,
            text="✨ AI-Powered Real-time Transcription with Stunning Visual Design",
            font=("Helvetica", 12, "italic"),
            fill=self.theme['accent_primary'],
            anchor="w",
            tags="subtitle"
        )
        
        # Header controls (theme toggle, settings)
        self.create_header_controls(width)
    
    def create_header_controls(self, width):
        """Create beautiful header controls"""
        # Theme toggle button with modern design
        theme_btn_bg = self.main_container.create_rectangle(
            width-180, 35, width-120, 75,
            fill=self.theme['bg_tertiary'],
            outline=self.theme['accent_primary'],
            width=2,
            tags="theme_btn_bg"
        )
        
        self.theme_btn_text = self.main_container.create_text(
            width-150, 55,
            text="🌙" if self.current_theme == 'light' else "☀️",
            font=("Helvetica", 20),
            fill=self.theme['accent_primary'],
            tags="theme_btn"
        )
        
        # Settings button
        settings_btn_bg = self.main_container.create_rectangle(
            width-110, 35, width-50, 75,
            fill=self.theme['bg_tertiary'],
            outline=self.theme['accent_secondary'],
            width=2,
            tags="settings_btn_bg"
        )
        
        self.settings_btn_text = self.main_container.create_text(
            width-80, 55,
            text="⚙️",
            font=("Helvetica", 18),
            fill=self.theme['accent_secondary'],
            tags="settings_btn"
        )
        
        # Bind click events
        self.main_container.tag_bind("theme_btn", "<Button-1>", lambda e: self.toggle_theme())
        self.main_container.tag_bind("theme_btn_bg", "<Button-1>", lambda e: self.toggle_theme())
        self.main_container.tag_bind("settings_btn", "<Button-1>", lambda e: self.show_settings())
        self.main_container.tag_bind("settings_btn_bg", "<Button-1>", lambda e: self.show_settings())
    
    def create_stunning_content(self):
        """Create the main content area with stunning design"""
        width = self.window.winfo_width() or 1600
        height = self.window.winfo_height() or 1000
        
        # Left panel for controls
        self.create_stunning_left_panel(width, height)
        
        # Right panel for transcript
        self.create_stunning_right_panel(width, height)
    
    def create_stunning_left_panel(self, width, height):
        """Create stunning left control panel"""
        panel_width = 400
        panel_x = 30
        panel_y = 140
        panel_height = height - 180
        
        # Panel background with glassmorphism
        panel_bg = self.main_container.create_rectangle(
            panel_x, panel_y, panel_x + panel_width, panel_y + panel_height,
            fill=self.theme['glass'],
            outline=self.theme['accent_primary'],
            width=2,
            tags="left_panel"
        )
        
        # Recording controls section
        self.create_recording_controls(panel_x, panel_y, panel_width)
        
        # Status section
        self.create_status_section(panel_x, panel_y + 180, panel_width)
        
        # Participants section
        self.create_participants_section(panel_x, panel_y + 320, panel_width)
        
        # Statistics section
        self.create_statistics_section(panel_x, panel_y + panel_height - 120, panel_width)
    
    def create_recording_controls(self, x, y, width):
        """Create beautiful recording controls"""
        # Section title
        self.main_container.create_text(
            x + 20, y + 30,
            text="🎮 Recording Controls",
            font=("Helvetica", 16, "bold"),
            fill=self.theme['text_primary'],
            anchor="w",
            tags="controls_title"
        )
        
        # Main record button with stunning design
        button_width = width - 40
        button_height = 60
        button_x = x + 20
        button_y = y + 60
        
        # Button background with gradient effect
        self.record_btn_bg = self.main_container.create_rectangle(
            button_x, button_y, button_x + button_width, button_y + button_height,
            fill=self.theme['success'],
            outline=self.theme['accent_primary'],
            width=3,
            tags="record_btn_bg"
        )
        
        # Button text
        self.record_btn_text = self.main_container.create_text(
            button_x + button_width//2, button_y + button_height//2,
            text="🎙️ Start Transcription",
            font=("Helvetica", 14, "bold"),
            fill="#ffffff",
            tags="record_btn_text"
        )
        
        # Secondary buttons
        clear_btn_y = button_y + 80
        export_btn_y = button_y + 80
        
        # Clear button
        self.clear_btn_bg = self.main_container.create_rectangle(
            button_x, clear_btn_y, button_x + (button_width//2 - 5), clear_btn_y + 40,
            fill=self.theme['bg_tertiary'],
            outline=self.theme['warning'],
            width=2,
            tags="clear_btn_bg"
        )
        
        self.main_container.create_text(
            button_x + (button_width//4), clear_btn_y + 20,
            text="🗑️ Clear",
            font=("Helvetica", 10, "bold"),
            fill=self.theme['text_primary'],
            tags="clear_btn_text"
        )
        
        # Export button
        self.export_btn_bg = self.main_container.create_rectangle(
            button_x + (button_width//2 + 5), export_btn_y, button_x + button_width, export_btn_y + 40,
            fill=self.theme['bg_tertiary'],
            outline=self.theme['accent_secondary'],
            width=2,
            tags="export_btn_bg"
        )
        
        self.main_container.create_text(
            button_x + (3 * button_width//4), export_btn_y + 20,
            text="💾 Export",
            font=("Helvetica", 10, "bold"),
            fill=self.theme['text_primary'],
            tags="export_btn_text"
        )
        
        # Bind button events
        self.main_container.tag_bind("record_btn_bg", "<Button-1>", lambda e: self.toggle_transcription())
        self.main_container.tag_bind("record_btn_text", "<Button-1>", lambda e: self.toggle_transcription())
        self.main_container.tag_bind("clear_btn_bg", "<Button-1>", lambda e: self.clear_transcript())
        self.main_container.tag_bind("clear_btn_text", "<Button-1>", lambda e: self.clear_transcript())
        self.main_container.tag_bind("export_btn_bg", "<Button-1>", lambda e: self.export_transcript())
        self.main_container.tag_bind("export_btn_text", "<Button-1>", lambda e: self.export_transcript())
    
    def create_status_section(self, x, y, width):
        """Create beautiful status section"""
        # Section title
        self.main_container.create_text(
            x + 20, y + 20,
            text="📊 Live Status",
            font=("Helvetica", 14, "bold"),
            fill=self.theme['text_primary'],
            anchor="w",
            tags="status_title"
        )
        
        # Recording status with animated indicator
        self.status_indicator = self.main_container.create_oval(
            x + 30, y + 50, x + 50, y + 70,
            fill=self.theme['text_tertiary'],
            outline=self.theme['text_tertiary'],
            width=2,
            tags="status_indicator"
        )
        
        self.status_text = self.main_container.create_text(
            x + 70, y + 60,
            text="Ready to start",
            font=("Helvetica", 11, "bold"),
            fill=self.theme['text_primary'],
            anchor="w",
            tags="status_text"
        )
        
        # Teams detection with modern styling
        self.teams_indicator = self.main_container.create_text(
            x + 30, y + 90,
            text="📱",
            font=("Helvetica", 16),
            fill=self.theme['text_tertiary'],
            anchor="w",
            tags="teams_indicator"
        )
        
        self.teams_text = self.main_container.create_text(
            x + 70, y + 100,
            text="Teams: Not detected",
            font=("Helvetica", 10),
            fill=self.theme['text_secondary'],
            anchor="w",
            tags="teams_text"
        )
    
    def create_participants_section(self, x, y, width):
        """Create beautiful participants section"""
        # Section title
        self.main_container.create_text(
            x + 20, y + 20,
            text="👥 Participants",
            font=("Helvetica", 14, "bold"),
            fill=self.theme['text_primary'],
            anchor="w",
            tags="participants_title"
        )
        
        # Participants area background
        self.participants_bg = self.main_container.create_rectangle(
            x + 20, y + 50, x + width - 20, y + 150,
            fill=self.theme['bg_quaternary'],
            outline=self.theme['accent_tertiary'],
            width=1,
            tags="participants_bg"
        )
        
        # Participants text
        self.participants_text = self.main_container.create_text(
            x + 30, y + 60,
            text="No participants detected yet",
            font=("Helvetica", 9),
            fill=self.theme['text_secondary'],
            anchor="nw",
            width=width-60,
            tags="participants_text"
        )
    
    def create_statistics_section(self, x, y, width):
        """Create beautiful statistics section"""
        # Section title
        self.main_container.create_text(
            x + 20, y + 20,
            text="📈 Live Statistics",
            font=("Helvetica", 14, "bold"),
            fill=self.theme['text_primary'],
            anchor="w",
            tags="stats_title"
        )
        
        # Stats text
        self.stats_text = self.main_container.create_text(
            x + 30, y + 50,
            text="Speakers: 0 | Duration: 0:00 | Words: 0",
            font=("Helvetica", 10),
            fill=self.theme['text_secondary'],
            anchor="nw",
            width=width-60,
            tags="stats_text"
        )
    
    def create_stunning_right_panel(self, width, height):
        """Create stunning right transcript panel"""
        panel_x = 460
        panel_y = 140
        panel_width = width - 490
        panel_height = height - 180
        
        # Panel background with glassmorphism
        panel_bg = self.main_container.create_rectangle(
            panel_x, panel_y, panel_x + panel_width, panel_y + panel_height,
            fill=self.theme['glass'],
            outline=self.theme['accent_secondary'],
            width=2,
            tags="right_panel"
        )
        
        # Transcript header
        self.main_container.create_text(
            panel_x + 20, panel_y + 30,
            text="💬 Live Transcript",
            font=("Helvetica", 18, "bold"),
            fill=self.theme['text_primary'],
            anchor="w",
            tags="transcript_title"
        )
        
        # Create embedded tkinter frame for transcript
        self.transcript_frame = tk.Frame(self.main_container, bg=self.theme['bg_primary'])
        self.transcript_window = self.main_container.create_window(
            panel_x + 20, panel_y + 60,
            window=self.transcript_frame,
            width=panel_width - 40,
            height=panel_height - 80,
            anchor="nw",
            tags="transcript_window"
        )
        
        # Create stunning transcript area
        self.create_transcript_area(panel_width - 40, panel_height - 80)
    
    def create_transcript_area(self, width, height):
        """Create the stunning transcript display area"""
        # Custom scrolled text with modern styling
        self.transcript_area = scrolledtext.ScrolledText(
            self.transcript_frame,
            wrap=tk.WORD,
            font=("JetBrains Mono", 11),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=20,
            insertbackground=self.theme['accent_primary'],
            selectbackground=self.theme['accent_primary'],
            selectforeground='#ffffff'
        )
        self.transcript_area.pack(fill=tk.BOTH, expand=True)
        
        # Configure beautiful text tags for speakers
        for i, colors in enumerate(self.speaker_colors):
            tag_name = f"speaker_{i}"
            self.transcript_area.tag_configure(
                tag_name,
                foreground=colors['primary'],
                font=("JetBrains Mono", 11, "bold")
            )
        
        # Special tags
        self.transcript_area.tag_configure(
            "timestamp",
            foreground=self.theme['text_tertiary'],
            font=("JetBrains Mono", 9)
        )
        
        self.transcript_area.tag_configure(
            "confidence",
            foreground=self.theme['accent_tertiary'],
            font=("JetBrains Mono", 9)
        )
        
        self.transcript_area.tag_configure(
            "enhanced",
            foreground=self.theme['success'],
            font=("JetBrains Mono", 10)
        )
    
    def start_stunning_animations(self):
        """Start all beautiful animations"""
        self.animate_gradient()
        self.animate_particles()
        self.animate_pulse()
        self.animate_wave()
    
    def animate_gradient(self):
        """Animate the gradient background"""
        if hasattr(self, 'main_container'):
            self.gradient_shift += 0.002
            if self.gradient_shift > 1.0:
                self.gradient_shift = 0.0
            
            # Update gradient
            self.main_container.delete("gradient")
            self.create_gradient_background()
            
            # Schedule next frame
            self.window.after(100, self.animate_gradient)
    
    def animate_particles(self):
        """Animate floating particles"""
        if hasattr(self, 'main_container') and self.floating_elements:
            width = self.window.winfo_width() or 1600
            height = self.window.winfo_height() or 1000
            
            for particle in self.floating_elements:
                # Update position
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                
                # Bounce off edges
                if particle['x'] <= 0 or particle['x'] >= width:
                    particle['dx'] *= -1
                if particle['y'] <= 0 or particle['y'] >= height:
                    particle['dy'] *= -1
                
                # Keep within bounds
                particle['x'] = max(0, min(width, particle['x']))
                particle['y'] = max(0, min(height, particle['y']))
                
                # Update pulse phase
                particle['pulse_phase'] += 0.1
                pulse_size = particle['size'] + math.sin(particle['pulse_phase']) * 2
                
                # Update particle position and size
                try:
                    self.main_container.coords(
                        particle['id'],
                        particle['x'] - pulse_size,
                        particle['y'] - pulse_size,
                        particle['x'] + pulse_size,
                        particle['y'] + pulse_size
                    )
                except:
                    pass
            
            # Schedule next frame
            self.window.after(50, self.animate_particles)
    
    def animate_pulse(self):
        """Animate pulsing elements"""
        if hasattr(self, 'main_container'):
            self.pulse_alpha += 0.1
            if self.pulse_alpha > 2 * math.pi:
                self.pulse_alpha = 0
            
            # Animate recording indicator if recording
            if self.is_recording and hasattr(self, 'status_indicator'):
                pulse_intensity = (math.sin(self.pulse_alpha) + 1) / 2
                red_intensity = int(255 * pulse_intensity)
                color = f"#{red_intensity:02x}{20:02x}{20:02x}"
                
                try:
                    self.main_container.itemconfig(self.status_indicator, fill=color, outline=color)
                except:
                    pass
            
            # Schedule next frame
            self.window.after(50, self.animate_pulse)
    
    def animate_wave(self):
        """Animate wave effects"""
        if hasattr(self, 'main_container'):
            self.wave_offset += 0.1
            if self.wave_offset > 2 * math.pi:
                self.wave_offset = 0
            
            # Add wave animation to subtitle
            if hasattr(self, 'subtitle_text'):
                wave_y = 85 + math.sin(self.wave_offset) * 2
                try:
                    self.main_container.coords(self.subtitle_text, 50, wave_y)
                except:
                    pass
            
            # Schedule next frame
            self.window.after(100, self.animate_wave)
    
    def on_window_resize(self, event):
        """Handle window resize for responsive design"""
        if event.widget == self.window:
            # Recreate UI elements for new size
            self.main_container.delete("all")
            self.setup_stunning_ui()
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def toggle_theme(self):
        """Toggle between dark and light themes with animation"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme = self.themes[self.current_theme]
        
        # Animate theme transition
        self.animate_theme_transition()
    
    def animate_theme_transition(self):
        """Animate smooth theme transition"""
        # Recreate UI with new theme
        self.main_container.delete("all")
        self.setup_stunning_ui()
        
        # Update theme button
        try:
            self.main_container.itemconfig(
                self.theme_btn_text,
                text="🌙" if self.current_theme == 'light' else "☀️"
            )
        except:
            pass
    
    def show_settings(self):
        """Show beautiful settings dialog"""
        settings_window = tk.Toplevel(self.window)
        settings_window.title("⚙️ Settings")
        settings_window.geometry("600x500")
        settings_window.configure(bg=self.theme['bg_primary'])
        settings_window.transient(self.window)
        settings_window.grab_set()
        
        # Center the window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (500 // 2)
        settings_window.geometry(f"600x500+{x}+{y}")
        
        # Beautiful settings content
        settings_frame = tk.Frame(settings_window, bg=self.theme['bg_primary'])
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        tk.Label(
            settings_frame,
            text="⚙️ Settings & Preferences",
            font=("Helvetica", 20, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_primary']
        ).pack(anchor=tk.W, pady=(0, 30))
        
        # Beautiful settings options
        self.create_settings_options(settings_frame)
    
    def create_settings_options(self, parent):
        """Create beautiful settings options"""
        # Theme selection
        theme_frame = tk.Frame(parent, bg=self.theme['bg_secondary'])
        theme_frame.pack(fill=tk.X, pady=(0, 20), padx=20)
        
        tk.Label(
            theme_frame,
            text="🎨 Appearance",
            font=("Helvetica", 14, "bold"),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_secondary']
        ).pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Add more settings options here
        settings_text = """
🌟 Beautiful Visual Settings:
   • Theme: Dark/Light mode toggle
   • Animations: Smooth transitions and effects
   • Particles: Floating background elements
   • Gradient: Animated color transitions

🎙️ Audio Processing:
   • Noise Reduction: Advanced algorithms
   • Echo Cancellation: Real-time processing
   • Voice Enhancement: AI-powered clarity
   • Gain Control: Automatic level adjustment

🧠 AI Features:
   • Participant Recognition: Smart mapping
   • Voice Analysis: Characteristics detection
   • Language Processing: Albanian optimization
   • Confidence Scoring: Transcription quality

More settings coming in future updates...
        """
        
        tk.Label(
            theme_frame,
            text=settings_text,
            font=("JetBrains Mono", 10),
            fg=self.theme['text_secondary'],
            bg=self.theme['bg_secondary'],
            justify=tk.LEFT,
            anchor=tk.W
        ).pack(padx=20, pady=(0, 20), fill=tk.BOTH, expand=True)
    
    # UI Control Methods
    def set_callbacks(self, start_callback, stop_callback):
        """Set callback functions"""
        self.start_callback = start_callback
        self.stop_callback = stop_callback
    
    def toggle_transcription(self):
        """Toggle transcription with beautiful animations"""
        if not self.is_recording:
            self.start_transcription()
        else:
            self.stop_transcription()
    
    def start_transcription(self):
        """Start transcription with stunning visual feedback"""
        self.is_recording = True
        
        # Update button with animation
        try:
            self.main_container.itemconfig(self.record_btn_bg, fill=self.theme['error'])
            self.main_container.itemconfig(self.record_btn_text, text="⏹️ Stop Transcription")
            self.main_container.itemconfig(self.status_text, text="Recording...", fill=self.theme['success'])
        except:
            pass
        
        # Add stunning start message
        self.add_stunning_system_message("🎙️ Transcription started with stunning visual effects...")
        
        if self.start_callback:
            self.start_callback()
    
    def stop_transcription(self):
        """Stop transcription with beautiful effects"""
        self.is_recording = False
        
        # Update button
        try:
            self.main_container.itemconfig(self.record_btn_bg, fill=self.theme['success'])
            self.main_container.itemconfig(self.record_btn_text, text="🎙️ Start Transcription")
            self.main_container.itemconfig(self.status_text, text="Stopped", fill=self.theme['text_secondary'])
            self.main_container.itemconfig(self.status_indicator, fill=self.theme['text_tertiary'])
        except:
            pass
        
        # Add beautiful stop message
        self.add_stunning_system_message("⏹️ Transcription stopped")
        
        if self.stop_callback:
            self.stop_callback()
    
    def add_stunning_system_message(self, message):
        """Add a system message with beautiful styling"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] ✨ {message}\n"
        
        if hasattr(self, 'transcript_area'):
            self.transcript_area.insert(tk.END, formatted_message, "enhanced")
            self.transcript_area.see(tk.END)
    
    def update_transcript(self, speaker_id, text, timestamp=None, enhanced_result=None):
        """Update transcript with stunning visual effects"""
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
        
        # Beautiful transcript formatting
        if hasattr(self, 'transcript_area'):
            self.transcript_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
            
            # Get speaker color
            speaker_index = hash(speaker_id or "Unknown") % len(self.speaker_colors)
            speaker_tag = f"speaker_{speaker_index}"
            
            self.transcript_area.insert(tk.END, f"{speaker_id or 'Unknown'}: ", speaker_tag)
            self.transcript_area.insert(tk.END, text)
            
            if confidence:
                self.transcript_area.insert(tk.END, confidence, "confidence")
            
            if enhanced_indicator:
                self.transcript_area.insert(tk.END, enhanced_indicator, "enhanced")
            
            self.transcript_area.insert(tk.END, "\n")
            self.transcript_area.see(tk.END)
        
        # Update statistics
        self.update_statistics()
    
    def update_participants(self, participants):
        """Update participants with beautiful display"""
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
            try:
                self.main_container.itemconfig(self.participants_text, text=participant_text, fill=self.theme['text_primary'])
            except:
                pass
        else:
            try:
                self.main_container.itemconfig(self.participants_text, text="No participants detected yet", fill=self.theme['text_secondary'])
            except:
                pass
    
    def update_teams_status(self, is_detected, reason=""):
        """Update Teams status with beautiful indicators"""
        if is_detected:
            try:
                self.main_container.itemconfig(self.teams_indicator, fill=self.theme['success'])
                self.main_container.itemconfig(self.teams_text, text=f"Teams: Connected ({reason})", fill=self.theme['success'])
            except:
                pass
        else:
            try:
                self.main_container.itemconfig(self.teams_indicator, fill=self.theme['text_tertiary'])
                self.main_container.itemconfig(self.teams_text, text="Teams: Not detected", fill=self.theme['text_secondary'])
            except:
                pass
    
    def update_statistics(self):
        """Update statistics with beautiful formatting"""
        speakers = set(entry['speaker'] for entry in self.transcript_data)
        total_words = sum(len(entry['text'].split()) for entry in self.transcript_data)
        
        # Calculate duration
        if self.transcript_data:
            try:
                first_time = datetime.strptime(self.transcript_data[0]['timestamp'], "%H:%M:%S")
                last_time = datetime.strptime(self.transcript_data[-1]['timestamp'], "%H:%M:%S")
                duration_seconds = (last_time - first_time).total_seconds()
                duration_minutes = int(duration_seconds // 60)
                duration_seconds = int(duration_seconds % 60)
                duration_str = f"{duration_minutes}:{duration_seconds:02d}"
            except:
                duration_str = "0:00"
        else:
            duration_str = "0:00"
        
        try:
            self.main_container.itemconfig(
                self.stats_text,
                text=f"Speakers: {len(speakers)} | Duration: {duration_str} | Words: {total_words}"
            )
        except:
            pass
    
    def clear_transcript(self):
        """Clear transcript with beautiful confirmation"""
        if messagebox.askyesno("Clear Transcript", 
                              "🗑️ Clear the beautiful transcript?\n\nThis action cannot be undone.",
                              parent=self.window):
            if hasattr(self, 'transcript_area'):
                self.transcript_area.delete(1.0, tk.END)
            self.transcript_data = []
            self.update_statistics()
            self.add_stunning_system_message("📝 Transcript cleared with style")
    
    def export_transcript(self):
        """Export transcript with beautiful options"""
        if not self.transcript_data:
            messagebox.showwarning("Export", "✨ No beautiful transcript to export!", parent=self.window)
            return
        
        file_path = filedialog.asksaveasfilename(
            parent=self.window,
            title="💾 Export Beautiful Transcript",
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
                
                messagebox.showinfo("Export", f"✨ Beautiful transcript exported to:\n{file_path}", 
                                  parent=self.window)
            except Exception as e:
                messagebox.showerror("Export Error", f"❌ Export failed:\n{e}", 
                                   parent=self.window)
    
    def export_text(self, file_path):
        """Export as beautiful text"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("✨ Albanian Teams Transcriber - Beautiful Transcript ✨\n")
            f.write("=" * 60 + "\n\n")
            
            for entry in self.transcript_data:
                f.write(f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}\n")
    
    def export_json(self, file_path):
        """Export as beautiful JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                'export_time': datetime.now().isoformat(),
                'app_version': 'Stunning Edition',
                'participants': self.participants,
                'transcript': self.transcript_data
            }, f, indent=2, ensure_ascii=False)
    
    def export_markdown(self, file_path):
        """Export as beautiful Markdown"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("# ✨ Albanian Teams Transcriber - Beautiful Transcript\n\n")
            f.write(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("**Version:** Stunning Edition\n\n")
            
            if self.participants:
                f.write("## 👥 Participants\n\n")
                for name, info in self.participants.items():
                    f.write(f"- **{name}** ({info.get('detection_method', 'unknown')})\n")
                f.write("\n")
            
            f.write("## 💬 Transcript\n\n")
            for entry in self.transcript_data:
                f.write(f"**[{entry['timestamp']}] {entry['speaker']}:** {entry['text']}\n\n")
    
    def run(self):
        """Start the stunning UI"""
        self.window.mainloop()
    
    def destroy(self):
        """Close the stunning window"""
        self.window.destroy()
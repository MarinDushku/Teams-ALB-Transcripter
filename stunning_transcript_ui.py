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
        self.window.title("🎭 Albanian Teams Transcriber - Ultra Stunning Edition")
        self.window.geometry("1800x1100")
        self.window.minsize(1400, 800)
        
        # Modern window styling
        self.window.configure(bg='#0a0a0a')
        
        # Center window on screen with beautiful entrance
        self.center_window_with_animation()
        
        # Set beautiful window icon if available
        try:
            self.window.iconbitmap(default='icon.ico')
        except:
            pass
        
        # Ultra stunning color schemes with enhanced gradients
        self.themes = {
            'dark': {
                'bg_primary': '#0d1117',
                'bg_secondary': '#161b22', 
                'bg_tertiary': '#21262d',
                'bg_quaternary': '#30363d',
                'text_primary': '#f0f6fc',
                'text_secondary': '#c9d1d9',
                'text_tertiary': '#8b949e',
                'accent_primary': '#58a6ff',
                'accent_secondary': '#ff7b72',
                'accent_tertiary': '#f0883e',
                'gradient_start': '#1f2937',
                'gradient_middle': '#374151',
                'gradient_end': '#4f46e5',
                'neon_blue': '#00d4ff',
                'neon_purple': '#a855f7',
                'neon_pink': '#ec4899',
                'success': '#3fb950',
                'warning': '#d29922',
                'error': '#f85149',
                'shadow': '#00000040',
                'glass': '#ffffff08',
                'glow': '#58a6ff20'
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
        
        # Ultra beautiful speaker colors with neon gradients
        self.speaker_colors = [
            {'primary': '#ff79c6', 'secondary': '#bd93f9', 'glow': '#ff79c680', 'avatar': '👤'},
            {'primary': '#50fa7b', 'secondary': '#8be9fd', 'glow': '#50fa7b80', 'avatar': '🎭'},
            {'primary': '#ffb86c', 'secondary': '#f1fa8c', 'glow': '#ffb86c80', 'avatar': '🎪'},
            {'primary': '#ff5555', 'secondary': '#ff79c6', 'glow': '#ff555580', 'avatar': '🌟'},
            {'primary': '#8be9fd', 'secondary': '#50fa7b', 'glow': '#8be9fd80', 'avatar': '💫'},
            {'primary': '#f1fa8c', 'secondary': '#ffb86c', 'glow': '#f1fa8c80', 'avatar': '✨'},
            {'primary': '#bd93f9', 'secondary': '#ff79c6', 'glow': '#bd93f980', 'avatar': '🎨'},
            {'primary': '#6272a4', 'secondary': '#8be9fd', 'glow': '#6272a480', 'avatar': '🎵'}
        ]
        
        # Transcript data
        self.transcript_data = []
        self.is_recording = False
        self.participants = {}
        
        # Setup ultra stunning UI
        self.setup_ultra_stunning_ui()
        
        # Start magical animations
        self.start_magical_animations()
        
        # Add window entrance animation
        self.animate_window_entrance()
        
    def center_window_with_animation(self):
        """Center window with beautiful entrance animation"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start with window slightly transparent for entrance effect
        self.window.attributes('-alpha', 0.0)
    
    def animate_window_entrance(self):
        """Animate window entrance with fade-in effect"""
        alpha = 0.0
        def fade_in():
            nonlocal alpha
            alpha += 0.05
            if alpha <= 1.0:
                self.window.attributes('-alpha', alpha)
                self.window.after(20, fade_in)
            else:
                self.window.attributes('-alpha', 1.0)
        fade_in()
    
    def setup_ultra_stunning_ui(self):
        """Setup the ultra stunning, breathtaking UI"""
        # Ultra stunning main container with advanced effects
        self.main_container = tk.Canvas(
            self.window,
            bg=self.theme['bg_primary'],
            highlightthickness=0,
            relief='flat',
            cursor='arrow'
        )
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Add mouse interaction effects
        self.main_container.bind('<Motion>', self.on_mouse_move)
        self.main_container.bind('<Button-1>', self.on_click_effect)
        
        # Create magical animated background
        self.create_magical_background()
        
        # Create floating particles with physics
        self.create_floating_particles()
        
        # Create energy waves
        self.create_energy_waves()
        
        # Header with ultra glassmorphism effect
        self.create_ultra_stunning_header()
        
        # Main content area with breathtaking layout
        self.create_breathtaking_content()
        
        # Setup callbacks
        self.start_callback = None
        self.stop_callback = None
        
        # Bind resize event for responsive design
        self.window.bind('<Configure>', self.on_window_resize)
    
    def create_magical_background(self):
        """Create a magical animated background with multiple layers"""
        width = self.window.winfo_width() or 1800
        height = self.window.winfo_height() or 1100
        
        # Create multi-layer gradient with smooth transitions
        gradient_steps = 80
        for i in range(gradient_steps):
            ratio = i / gradient_steps
            
            # Triple gradient with animated shifts
            r1, g1, b1 = self.hex_to_rgb(self.theme['gradient_start'])
            r2, g2, b2 = self.hex_to_rgb(self.theme['gradient_middle'])
            r3, g3, b3 = self.hex_to_rgb(self.theme['gradient_end'])
            
            # Create wave-like gradient animation
            wave_offset = math.sin(ratio * math.pi * 2 + self.gradient_shift * 10) * 0.2
            animated_ratio = (ratio + self.gradient_shift + wave_offset) % 1.0
            
            if animated_ratio < 0.5:
                # Interpolate between first and second color
                t = animated_ratio * 2
                r = int(r1 + (r2 - r1) * t)
                g = int(g1 + (g2 - g1) * t)
                b = int(b1 + (b2 - b1) * t)
            else:
                # Interpolate between second and third color
                t = (animated_ratio - 0.5) * 2
                r = int(r2 + (r3 - r2) * t)
                g = int(g2 + (g3 - g2) * t)
                b = int(b2 + (b3 - b2) * t)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            y1 = i * height / gradient_steps
            y2 = (i + 1) * height / gradient_steps
            
            self.main_container.create_rectangle(
                0, y1, width, y2,
                fill=color,
                outline="",
                tags="gradient"
            )
        
        # Add constellation overlay
        self.create_constellation_overlay(width, height)
    
    def create_floating_particles(self):
        """Create magical floating particles with physics"""
        width = self.window.winfo_width() or 1800
        height = self.window.winfo_height() or 1100
        
        # Create diverse floating elements
        particle_types = [
            {'color': self.theme['neon_blue'], 'size_range': (3, 10), 'glow': True},
            {'color': self.theme['neon_purple'], 'size_range': (2, 8), 'glow': True},
            {'color': self.theme['neon_pink'], 'size_range': (4, 12), 'glow': True},
            {'color': self.theme['accent_primary'], 'size_range': (1, 6), 'glow': False}
        ]
        
        for i in range(40):  # More particles for richer effect
            x = random.randint(0, width)
            y = random.randint(0, height)
            
            particle_type = random.choice(particle_types)
            size = random.randint(*particle_type['size_range'])
            
            # Create particle with enhanced glow effect
            if particle_type['glow']:
                # Create glow halo first
                glow = self.main_container.create_oval(
                    x-size*2, y-size*2, x+size*2, y+size*2,
                    fill=particle_type['color'] + '20',
                    outline="",
                    tags="particle_glow"
                )
            
            # Create main particle
            particle = self.main_container.create_oval(
                x-size, y-size, x+size, y+size,
                fill=particle_type['color'],
                outline=particle_type['color'],
                width=0,
                tags="particle"
            )
            
            # Store particle info for advanced animation
            self.floating_elements.append({
                'id': particle,
                'glow_id': glow if particle_type['glow'] else None,
                'x': x,
                'y': y,
                'size': size,
                'dx': random.uniform(-1.2, 1.2),
                'dy': random.uniform(-1.2, 1.2),
                'pulse_phase': random.uniform(0, 2 * math.pi),
                'color': particle_type['color'],
                'has_glow': particle_type['glow'],
                'rotation': random.uniform(0, 2 * math.pi),
                'rotation_speed': random.uniform(-0.1, 0.1)
            })
    
    def create_constellation_overlay(self, width, height):
        """Create beautiful constellation overlay"""
        # Create constellation stars
        for i in range(15):
            x = random.randint(int(width*0.1), int(width*0.9))
            y = random.randint(int(height*0.1), int(height*0.4))
            
            star = self.main_container.create_text(
                x, y,
                text=random.choice(['✦', '✨', '★', '☆', '✯']),
                font=("Arial", random.randint(8, 16)),
                fill=self.theme['accent_primary'] + random.choice(['40', '60', '80']),
                tags="constellation"
            )
    
    def create_energy_waves(self):
        """Create flowing energy waves"""
        width = self.window.winfo_width() or 1800
        height = self.window.winfo_height() or 1100
        
        # Create flowing wave lines
        for i in range(3):
            wave_points = []
            y_base = height * (0.3 + i * 0.2)
            
            for x in range(0, width, 20):
                wave_y = y_base + math.sin(x * 0.01 + i * 2) * 30
                wave_points.extend([x, wave_y])
            
            if len(wave_points) >= 4:
                wave = self.main_container.create_line(
                    wave_points,
                    fill=self.theme['accent_primary'] + '30',
                    width=2,
                    smooth=True,
                    tags="energy_wave"
                )
    
    def create_ultra_stunning_header(self):
        """Create an ultra stunning header with advanced glassmorphism"""
        width = self.window.winfo_width() or 1800
        
        # Multi-layer header with advanced glassmorphism
        # Outer glow layer
        header_glow = self.main_container.create_rectangle(
            15, 15, width-15, 125,
            fill="",
            outline=self.theme['glow'],
            width=8,
            tags="header_glow"
        )
        
        # Main header background with enhanced glass effect
        header_bg = self.main_container.create_rectangle(
            20, 20, width-20, 120,
            fill=self.theme['glass'],
            outline=self.theme['accent_primary'],
            width=3,
            tags="header"
        )
        
        # Inner highlight for depth
        header_highlight = self.main_container.create_rectangle(
            25, 25, width-25, 30,
            fill=self.theme['accent_primary'] + '20',
            outline="",
            tags="header_highlight"
        )
        
        # Add subtle shadow
        shadow = self.main_container.create_rectangle(
            25, 25, width-15, 125,
            fill=self.theme['shadow'],
            outline="",
            tags="header_shadow"
        )
        self.main_container.tag_lower(shadow)
        
        # Ultra beautiful title with neon glow effect
        # Title shadow for depth
        title_shadow = self.main_container.create_text(
            52, 52,
            text="🎭 Albanian Teams Transcriber",
            font=("JetBrains Mono", 32, "bold"),
            fill="#000000",
            anchor="w",
            tags="title_shadow"
        )
        
        # Main title with gradient-like effect using multiple colors
        self.title_text = self.main_container.create_text(
            50, 50,
            text="🎭 Albanian Teams Transcriber",
            font=("JetBrains Mono", 32, "bold"),
            fill=self.theme['neon_blue'],
            anchor="w",
            tags="title"
        )
        
        # Ultra animated subtitle with pulsing effect
        self.subtitle_text = self.main_container.create_text(
            50, 90,
            text="✨ Ultra Stunning AI-Powered Real-time Transcription Experience",
            font=("JetBrains Mono", 13, "italic"),
            fill=self.theme['neon_purple'],
            anchor="w",
            tags="subtitle"
        )
        
        # Add version badge
        version_badge = self.main_container.create_rectangle(
            width-250, 45, width-150, 75,
            fill=self.theme['neon_pink'] + '40',
            outline=self.theme['neon_pink'],
            width=2,
            tags="version_badge"
        )
        
        version_text = self.main_container.create_text(
            width-200, 60,
            text="ULTRA v2.0",
            font=("JetBrains Mono", 10, "bold"),
            fill=self.theme['neon_pink'],
            tags="version_text"
        )
        
        # Ultra header controls with enhanced design
        self.create_ultra_header_controls(width)
    
    def create_ultra_header_controls(self, width):
        """Create ultra beautiful header controls with neon effects"""
        # Ultra theme toggle with neon glow
        theme_glow = self.main_container.create_rectangle(
            width-370, 30, width-300, 80,
            fill="",
            outline=self.theme['neon_blue'] + '60',
            width=4,
            tags="theme_btn_glow"
        )
        
        theme_btn_bg = self.main_container.create_rectangle(
            width-365, 35, width-305, 75,
            fill=self.theme['bg_tertiary'],
            outline=self.theme['neon_blue'],
            width=2,
            tags="theme_btn_bg"
        )
        
        self.theme_btn_text = self.main_container.create_text(
            width-335, 55,
            text="🌙" if self.current_theme == 'light' else "☀️",
            font=("Segoe UI Emoji", 24),
            fill=self.theme['neon_blue'],
            tags="theme_btn"
        )
        
        # Ultra settings button with purple glow
        settings_glow = self.main_container.create_rectangle(
            width-290, 30, width-220, 80,
            fill="",
            outline=self.theme['neon_purple'] + '60',
            width=4,
            tags="settings_btn_glow"
        )
        
        settings_btn_bg = self.main_container.create_rectangle(
            width-285, 35, width-225, 75,
            fill=self.theme['bg_tertiary'],
            outline=self.theme['neon_purple'],
            width=2,
            tags="settings_btn_bg"
        )
        
        self.settings_btn_text = self.main_container.create_text(
            width-255, 55,
            text="⚙️",
            font=("Segoe UI Emoji", 22),
            fill=self.theme['neon_purple'],
            tags="settings_btn"
        )
        
        # Add minimize/maximize/close buttons with neon effects
        self.create_window_controls(width)
        
        # Bind enhanced click events with hover effects
        self.bind_button_events("theme_btn", self.toggle_theme, self.theme['neon_blue'])
        self.bind_button_events("settings_btn", self.show_settings, self.theme['neon_purple'])
    
    def create_window_controls(self, width):
        """Create beautiful window control buttons"""
        # Minimize button
        min_btn = self.main_container.create_rectangle(
            width-210, 35, width-185, 60,
            fill=self.theme['warning'] + '40',
            outline=self.theme['warning'],
            width=1,
            tags="min_btn"
        )
        
        min_text = self.main_container.create_text(
            width-197, 47,
            text="−",
            font=("Arial", 12, "bold"),
            fill=self.theme['warning'],
            tags="min_btn_text"
        )
        
        # Close button
        close_btn = self.main_container.create_rectangle(
            width-180, 35, width-155, 60,
            fill=self.theme['error'] + '40',
            outline=self.theme['error'],
            width=1,
            tags="close_btn"
        )
        
        close_text = self.main_container.create_text(
            width-167, 47,
            text="×",
            font=("Arial", 14, "bold"),
            fill=self.theme['error'],
            tags="close_btn_text"
        )
        
        # Bind window control events
        self.main_container.tag_bind("min_btn", "<Button-1>", lambda e: self.window.iconify())
        self.main_container.tag_bind("min_btn_text", "<Button-1>", lambda e: self.window.iconify())
        self.main_container.tag_bind("close_btn", "<Button-1>", lambda e: self.window.destroy())
        self.main_container.tag_bind("close_btn_text", "<Button-1>", lambda e: self.window.destroy())
    
    def bind_button_events(self, tag_prefix, callback, glow_color):
        """Bind enhanced button events with hover effects"""
        def on_enter(event):
            self.add_button_hover_glow(tag_prefix, glow_color)
        
        def on_leave(event):
            self.remove_button_hover_glow(tag_prefix)
        
        def on_click(event):
            self.button_click_animation(tag_prefix)
            callback()
        
        self.main_container.tag_bind(tag_prefix, "<Enter>", on_enter)
        self.main_container.tag_bind(tag_prefix + "_bg", "<Enter>", on_enter)
        self.main_container.tag_bind(tag_prefix, "<Leave>", on_leave)
        self.main_container.tag_bind(tag_prefix + "_bg", "<Leave>", on_leave)
        self.main_container.tag_bind(tag_prefix, "<Button-1>", on_click)
        self.main_container.tag_bind(tag_prefix + "_bg", "<Button-1>", on_click)
    
    def create_breathtaking_content(self):
        """Create the main content area with breathtaking design"""
        width = self.window.winfo_width() or 1800
        height = self.window.winfo_height() or 1100
        
        # Left panel for ultra controls
        self.create_ultra_stunning_left_panel(width, height)
        
        # Right panel for ultra transcript
        self.create_ultra_stunning_right_panel(width, height)
    
    def create_ultra_stunning_left_panel(self, width, height):
        """Create ultra stunning left control panel with neon effects"""
        panel_width = 450
        panel_x = 35
        panel_y = 150
        panel_height = height - 190
        
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
        
        # Ultra stunning main record button with neon effects
        button_width = width - 40
        button_height = 70
        button_x = x + 20
        button_y = y + 60
        
        # Button outer glow
        self.record_btn_glow = self.main_container.create_rectangle(
            button_x - 5, button_y - 5, button_x + button_width + 5, button_y + button_height + 5,
            fill="",
            outline=self.theme['neon_blue'] + '60',
            width=6,
            tags="record_btn_glow"
        )
        
        # Button background with enhanced gradient effect
        self.record_btn_bg = self.main_container.create_rectangle(
            button_x, button_y, button_x + button_width, button_y + button_height,
            fill=self.theme['bg_tertiary'],
            outline=self.theme['neon_blue'],
            width=3,
            tags="record_btn_bg"
        )
        
        # Button inner highlight
        self.record_btn_highlight = self.main_container.create_rectangle(
            button_x + 3, button_y + 3, button_x + button_width - 3, button_y + 8,
            fill=self.theme['neon_blue'] + '30',
            outline="",
            tags="record_btn_highlight"
        )
        
        # Button icon and text with enhanced styling
        self.record_btn_icon = self.main_container.create_text(
            button_x + 40, button_y + button_height//2,
            text="🎙️",
            font=("Segoe UI Emoji", 24),
            fill=self.theme['neon_blue'],
            tags="record_btn_icon"
        )
        
        self.record_btn_text = self.main_container.create_text(
            button_x + button_width//2 + 20, button_y + button_height//2,
            text="Start Ultra Transcription",
            font=("JetBrains Mono", 14, "bold"),
            fill=self.theme['text_primary'],
            tags="record_btn_text"
        )
        
        # Ultra stunning secondary buttons
        secondary_btn_y = button_y + 90
        secondary_btn_height = 50
        
        # Clear button with neon warning glow
        clear_btn_width = (button_width//2 - 5)
        
        self.clear_btn_glow = self.main_container.create_rectangle(
            button_x - 2, secondary_btn_y - 2, button_x + clear_btn_width + 2, secondary_btn_y + secondary_btn_height + 2,
            fill="",
            outline=self.theme['warning'] + '60',
            width=3,
            tags="clear_btn_glow"
        )
        
        self.clear_btn_bg = self.main_container.create_rectangle(
            button_x, secondary_btn_y, button_x + clear_btn_width, secondary_btn_y + secondary_btn_height,
            fill=self.theme['bg_tertiary'],
            outline=self.theme['warning'],
            width=2,
            tags="clear_btn_bg"
        )
        
        self.clear_btn_icon = self.main_container.create_text(
            button_x + 25, secondary_btn_y + secondary_btn_height//2,
            text="🗑️",
            font=("Segoe UI Emoji", 18),
            fill=self.theme['warning'],
            tags="clear_btn_icon"
        )
        
        self.clear_btn_text = self.main_container.create_text(
            button_x + clear_btn_width//2 + 15, secondary_btn_y + secondary_btn_height//2,
            text="Clear",
            font=("JetBrains Mono", 11, "bold"),
            fill=self.theme['text_primary'],
            tags="clear_btn_text"
        )
        
        # Export button with neon purple glow
        export_btn_x = button_x + (button_width//2 + 5)
        export_btn_width = button_width - (button_width//2 + 5)
        
        self.export_btn_glow = self.main_container.create_rectangle(
            export_btn_x - 2, secondary_btn_y - 2, export_btn_x + export_btn_width + 2, secondary_btn_y + secondary_btn_height + 2,
            fill="",
            outline=self.theme['neon_purple'] + '60',
            width=3,
            tags="export_btn_glow"
        )
        
        self.export_btn_bg = self.main_container.create_rectangle(
            export_btn_x, secondary_btn_y, export_btn_x + export_btn_width, secondary_btn_y + secondary_btn_height,
            fill=self.theme['bg_tertiary'],
            outline=self.theme['neon_purple'],
            width=2,
            tags="export_btn_bg"
        )
        
        self.export_btn_icon = self.main_container.create_text(
            export_btn_x + 25, secondary_btn_y + secondary_btn_height//2,
            text="💾",
            font=("Segoe UI Emoji", 18),
            fill=self.theme['neon_purple'],
            tags="export_btn_icon"
        )
        
        self.export_btn_text = self.main_container.create_text(
            export_btn_x + export_btn_width//2 + 15, secondary_btn_y + secondary_btn_height//2,
            text="Export",
            font=("JetBrains Mono", 11, "bold"),
            fill=self.theme['text_primary'],
            tags="export_btn_text"
        )
        
        # Bind enhanced button events with hover and click effects
        self.bind_control_button("record_btn", self.toggle_transcription, self.theme['neon_blue'])
        self.bind_control_button("clear_btn", self.clear_transcript, self.theme['warning'])
        self.bind_control_button("export_btn", self.export_transcript, self.theme['neon_purple'])
    
    def bind_control_button(self, button_prefix, callback, glow_color):
        """Bind enhanced control button events"""
        def on_enter(event):
            # Enhance glow on hover
            glow_items = self.main_container.find_withtag(button_prefix + "_glow")
            for item in glow_items:
                self.main_container.itemconfig(item, width=8, outline=glow_color + '80')
        
        def on_leave(event):
            # Reset glow
            glow_items = self.main_container.find_withtag(button_prefix + "_glow")
            for item in glow_items:
                self.main_container.itemconfig(item, width=3, outline=glow_color + '60')
        
        def on_click(event):
            # Enhanced click animation
            self.control_button_click_animation(button_prefix)
            if callback:
                callback()
        
        # Bind events to all button components
        button_tags = [button_prefix + "_bg", button_prefix + "_text", button_prefix + "_icon"]
        for tag in button_tags:
            self.main_container.tag_bind(tag, "<Enter>", on_enter)
            self.main_container.tag_bind(tag, "<Leave>", on_leave)
            self.main_container.tag_bind(tag, "<Button-1>", on_click)
    
    def control_button_click_animation(self, button_prefix):
        """Enhanced control button click animation"""
        # Create ripple effect
        bg_items = self.main_container.find_withtag(button_prefix + "_bg")
        if bg_items:
            coords = self.main_container.coords(bg_items[0])
            if len(coords) >= 4:
                x1, y1, x2, y2 = coords
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                
                # Create expanding ripple
                ripple = self.main_container.create_oval(
                    center_x - 5, center_y - 5, center_x + 5, center_y + 5,
                    fill="",
                    outline=self.theme['neon_blue'] + '80',
                    width=3,
                    tags="button_ripple"
                )
                
                # Animate ripple
                self.animate_button_ripple(ripple, center_x, center_y)
    
    def animate_button_ripple(self, ripple, x, y):
        """Animate button ripple effect"""
        size = 5
        def expand():
            nonlocal size
            size += 8
            if size <= 80:
                self.main_container.coords(ripple, x-size, y-size, x+size, y+size)
                alpha = int(80 - size)
                if alpha > 0:
                    self.main_container.itemconfig(ripple, outline=self.theme['neon_blue'] + f'{alpha:02x}')
                self.window.after(30, expand)
            else:
                self.main_container.delete(ripple)
        expand()
    
    def create_status_section(self, x, y, width):
        """Create ultra beautiful status section with neon indicators"""
        # Enhanced section title with glow
        self.main_container.create_text(
            x + 22, y + 22,
            text="📊 Live Status",
            font=("JetBrains Mono", 14, "bold"),
            fill="#000000",
            anchor="w",
            tags="status_title_shadow"
        )
        
        self.main_container.create_text(
            x + 20, y + 20,
            text="📊 Live Status",
            font=("JetBrains Mono", 14, "bold"),
            fill=self.theme['neon_blue'],
            anchor="w",
            tags="status_title"
        )
        
        # Ultra animated status indicator with pulsing glow
        self.status_indicator_glow = self.main_container.create_oval(
            x + 25, y + 45, x + 55, y + 75,
            fill="",
            outline=self.theme['text_tertiary'] + '40',
            width=4,
            tags="status_indicator_glow"
        )
        
        self.status_indicator = self.main_container.create_oval(
            x + 30, y + 50, x + 50, y + 70,
            fill=self.theme['text_tertiary'],
            outline=self.theme['text_tertiary'],
            width=2,
            tags="status_indicator"
        )
        
        self.status_text = self.main_container.create_text(
            x + 70, y + 60,
            text="✨ Ready to start ultra transcription",
            font=("JetBrains Mono", 11, "bold"),
            fill=self.theme['text_primary'],
            anchor="w",
            tags="status_text"
        )
        
        # Ultra Teams detection with neon styling and animations
        self.teams_indicator_bg = self.main_container.create_rectangle(
            x + 25, y + 85, x + 55, y + 115,
            fill=self.theme['bg_quaternary'],
            outline=self.theme['text_tertiary'],
            width=2,
            tags="teams_indicator_bg"
        )
        
        self.teams_indicator = self.main_container.create_text(
            x + 40, y + 100,
            text="📱",
            font=("Segoe UI Emoji", 20),
            fill=self.theme['text_tertiary'],
            anchor="center",
            tags="teams_indicator"
        )
        
        self.teams_text = self.main_container.create_text(
            x + 70, y + 100,
            text="🔍 Scanning for Teams meeting...",
            font=("JetBrains Mono", 10),
            fill=self.theme['text_secondary'],
            anchor="w",
            tags="teams_text"
        )
    
    def create_participants_section(self, x, y, width):
        """Create ultra beautiful participants section with avatars"""
        # Enhanced section title with glow effect
        self.main_container.create_text(
            x + 22, y + 22,
            text="👥 Participants",
            font=("JetBrains Mono", 14, "bold"),
            fill="#000000",
            anchor="w",
            tags="participants_title_shadow"
        )
        
        self.main_container.create_text(
            x + 20, y + 20,
            text="👥 Participants",
            font=("JetBrains Mono", 14, "bold"),
            fill=self.theme['neon_purple'],
            anchor="w",
            tags="participants_title"
        )
        
        # Ultra participants area with glassmorphism
        self.participants_bg_glow = self.main_container.create_rectangle(
            x + 15, y + 45, x + width - 15, y + 155,
            fill="",
            outline=self.theme['neon_purple'] + '40',
            width=3,
            tags="participants_bg_glow"
        )
        
        self.participants_bg = self.main_container.create_rectangle(
            x + 20, y + 50, x + width - 20, y + 150,
            fill=self.theme['glass'],
            outline=self.theme['neon_purple'],
            width=2,
            tags="participants_bg"
        )
        
        # Enhanced participants text with animation dots
        self.participants_text = self.main_container.create_text(
            x + 30, y + 60,
            text="🔍 Detecting participants",
            font=("JetBrains Mono", 10),
            fill=self.theme['text_secondary'],
            anchor="nw",
            width=width-60,
            tags="participants_text"
        )
        
        # Add animated dots for loading effect
        self.participants_dots = self.main_container.create_text(
            x + 30, y + 80,
            text="● ● ●",
            font=("JetBrains Mono", 8),
            fill=self.theme['neon_purple'],
            anchor="nw",
            tags="participants_dots"
        )
        
        # Start dots animation
        self.animate_participants_dots()
    
    def animate_participants_dots(self):
        """Animate loading dots for participants"""
        if hasattr(self, 'participants_dots'):
            dot_patterns = ["●   ", "● ● ", "● ● ●", "  ● ●", "    ●", "     "]
            pattern_index = int(time.time() * 2) % len(dot_patterns)
            
            try:
                self.main_container.itemconfig(
                    self.participants_dots, 
                    text=dot_patterns[pattern_index]
                )
            except:
                pass
            
            self.window.after(200, self.animate_participants_dots)
    
    def create_statistics_section(self, x, y, width):
        """Create ultra beautiful statistics section with live charts"""
        # Enhanced section title with glow
        self.main_container.create_text(
            x + 22, y + 22,
            text="📈 Live Statistics",
            font=("JetBrains Mono", 14, "bold"),
            fill="#000000",
            anchor="w",
            tags="stats_title_shadow"
        )
        
        self.main_container.create_text(
            x + 20, y + 20,
            text="📈 Live Statistics",
            font=("JetBrains Mono", 14, "bold"),
            fill=self.theme['neon_pink'],
            anchor="w",
            tags="stats_title"
        )
        
        # Ultra stats display with individual metrics
        metrics_y = y + 50
        
        # Speakers metric
        self.speakers_metric = self.main_container.create_text(
            x + 30, metrics_y,
            text="🗣️ Speakers: 0",
            font=("JetBrains Mono", 9, "bold"),
            fill=self.theme['neon_blue'],
            anchor="nw",
            tags="speakers_metric"
        )
        
        # Duration metric
        self.duration_metric = self.main_container.create_text(
            x + 30, metrics_y + 20,
            text="⏱️ Duration: 0:00",
            font=("JetBrains Mono", 9, "bold"),
            fill=self.theme['neon_purple'],
            anchor="nw",
            tags="duration_metric"
        )
        
        # Words metric
        self.words_metric = self.main_container.create_text(
            x + 30, metrics_y + 40,
            text="💬 Words: 0",
            font=("JetBrains Mono", 9, "bold"),
            fill=self.theme['neon_pink'],
            anchor="nw",
            tags="words_metric"
        )
        
        # Quality metric
        self.quality_metric = self.main_container.create_text(
            x + 30, metrics_y + 60,
            text="✨ Quality: Excellent",
            font=("JetBrains Mono", 9, "bold"),
            fill=self.theme['success'],
            anchor="nw",
            tags="quality_metric"
        )
    
    def create_ultra_stunning_right_panel(self, width, height):
        """Create ultra stunning right transcript panel with enhanced effects"""
        panel_x = 500
        panel_y = 150
        panel_width = width - 540
        panel_height = height - 190
        
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
    
    def start_magical_animations(self):
        """Start all magical animations with enhanced effects"""
        self.animate_magical_gradient()
        self.animate_magical_particles()
        self.animate_neon_pulse()
        self.animate_energy_waves()
        self.animate_title_glow()
        self.animate_constellation_twinkle()
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def on_mouse_move(self, event):
        """Handle mouse movement for interactive effects"""
        # Create ripple effect at mouse position
        if not hasattr(self, 'mouse_ripples'):
            self.mouse_ripples = []
        
        if len(self.mouse_ripples) < 3:
            ripple = self.main_container.create_oval(
                event.x-10, event.y-10, event.x+10, event.y+10,
                fill="",
                outline=self.theme['neon_blue'] + '60',
                width=2,
                tags="mouse_ripple"
            )
            
            self.mouse_ripples.append(ripple)
            
            # Animate ripple expansion
            self.animate_mouse_ripple(ripple, event.x, event.y)
    
    def on_click_effect(self, event):
        """Create click effect animation"""
        # Create explosion effect
        for i in range(8):
            angle = i * (math.pi * 2 / 8)
            end_x = event.x + math.cos(angle) * 30
            end_y = event.y + math.sin(angle) * 30
            
            spark = self.main_container.create_line(
                event.x, event.y, end_x, end_y,
                fill=self.theme['neon_pink'],
                width=3,
                tags="click_spark"
            )
            
            # Animate spark fade
            self.animate_spark_fade(spark)
    
    def animate_mouse_ripple(self, ripple, x, y):
        """Animate mouse ripple expansion"""
        size = 10
        def expand():
            nonlocal size
            size += 5
            if size <= 60:
                self.main_container.coords(ripple, x-size, y-size, x+size, y+size)
                alpha = int(60 - size)
                if alpha > 0:
                    self.main_container.itemconfig(ripple, outline=self.theme['neon_blue'] + f'{alpha:02x}')
                self.window.after(50, expand)
            else:
                self.main_container.delete(ripple)
                if ripple in self.mouse_ripples:
                    self.mouse_ripples.remove(ripple)
        expand()
    
    def animate_spark_fade(self, spark):
        """Animate spark fade effect"""
        alpha = 255
        def fade():
            nonlocal alpha
            alpha -= 20
            if alpha > 0:
                hex_alpha = f'{alpha:02x}'
                self.main_container.itemconfig(spark, fill=self.theme['neon_pink'] + hex_alpha)
                self.window.after(30, fade)
            else:
                self.main_container.delete(spark)
        fade()
    
    def add_button_hover_glow(self, tag_prefix, glow_color):
        """Add glow effect on button hover"""
        glow_tag = tag_prefix + "_hover_glow"
        
        # Get button coordinates
        items = self.main_container.find_withtag(tag_prefix + "_bg")
        if items:
            coords = self.main_container.coords(items[0])
            if len(coords) >= 4:
                x1, y1, x2, y2 = coords
                
                # Create hover glow
                glow = self.main_container.create_rectangle(
                    x1-3, y1-3, x2+3, y2+3,
                    fill="",
                    outline=glow_color + '80',
                    width=4,
                    tags=glow_tag
                )
                
                # Move glow behind button
                self.main_container.tag_lower(glow)
    
    def remove_button_hover_glow(self, tag_prefix):
        """Remove glow effect on button leave"""
        glow_tag = tag_prefix + "_hover_glow"
        self.main_container.delete(glow_tag)
    
    def button_click_animation(self, tag_prefix):
        """Animate button click effect"""
        # Get button items
        bg_items = self.main_container.find_withtag(tag_prefix + "_bg")
        text_items = self.main_container.find_withtag(tag_prefix)
        
        if bg_items and text_items:
            # Scale down effect
            def scale_down():
                coords = self.main_container.coords(bg_items[0])
                if len(coords) >= 4:
                    x1, y1, x2, y2 = coords
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    
                    # Shrink button
                    self.main_container.coords(bg_items[0], 
                        center_x - (x2-x1)*0.45/2, center_y - (y2-y1)*0.45/2,
                        center_x + (x2-x1)*0.45/2, center_y + (y2-y1)*0.45/2)
                    
                    # Restore after brief delay
                    self.window.after(100, lambda: self.main_container.coords(bg_items[0], x1, y1, x2, y2))
            
            scale_down()
    
    def animate_magical_gradient(self):
        """Animate the magical gradient background"""
        if hasattr(self, 'main_container'):
            self.gradient_shift += 0.003
            if self.gradient_shift >= 1.0:
                self.gradient_shift = 0.0
            
            # Recreate gradient with new shift
            self.main_container.delete("gradient")
            self.create_magical_background()
            
            self.window.after(50, self.animate_magical_gradient)
    
    def animate_magical_particles(self):
        """Animate magical floating particles with physics"""
        if hasattr(self, 'floating_elements'):
            for element in self.floating_elements:
                try:
                    # Update position with physics
                    element['x'] += element['dx']
                    element['y'] += element['dy']
                    
                    # Bounce off edges
                    width = self.window.winfo_width() or 1800
                    height = self.window.winfo_height() or 1100
                    
                    if element['x'] <= element['size'] or element['x'] >= width - element['size']:
                        element['dx'] *= -0.8  # Energy loss on bounce
                    if element['y'] <= element['size'] or element['y'] >= height - element['size']:
                        element['dy'] *= -0.8
                    
                    # Keep particles in bounds
                    element['x'] = max(element['size'], min(width - element['size'], element['x']))
                    element['y'] = max(element['size'], min(height - element['size'], element['y']))
                    
                    # Update pulse animation
                    element['pulse_phase'] += 0.1
                    pulse_scale = 1 + 0.3 * math.sin(element['pulse_phase'])
                    
                    # Update rotation
                    element['rotation'] += element['rotation_speed']
                    
                    # Apply transformations
                    size = element['size'] * pulse_scale
                    
                    # Update particle position
                    self.main_container.coords(
                        element['id'],
                        element['x'] - size,
                        element['y'] - size,
                        element['x'] + size,
                        element['y'] + size
                    )
                    
                    # Update glow if present
                    if element['has_glow'] and element['glow_id']:
                        glow_size = size * 2
                        self.main_container.coords(
                            element['glow_id'],
                            element['x'] - glow_size,
                            element['y'] - glow_size,
                            element['x'] + glow_size,
                            element['y'] + glow_size
                        )
                        
                        # Animate glow opacity
                        glow_alpha = int(50 + 30 * math.sin(element['pulse_phase'] * 0.5))
                        glow_color = element['color'] + f'{glow_alpha:02x}'
                        self.main_container.itemconfig(element['glow_id'], fill=glow_color)
                    
                    # Add slight gravity effect
                    element['dy'] += 0.02
                    
                    # Add air resistance
                    element['dx'] *= 0.999
                    element['dy'] *= 0.999
                    
                except Exception:
                    pass
            
            self.window.after(30, self.animate_magical_particles)
    
    def animate_neon_pulse(self):
        """Animate neon pulsing effects"""
        if hasattr(self, 'main_container'):
            self.pulse_alpha += 0.15
            
            # Pulse glow effects
            pulse_intensity = 0.5 + 0.5 * math.sin(self.pulse_alpha)
            
            # Update accent colors with pulse
            items_to_pulse = [
                'header', 'theme_btn_bg', 'settings_btn_bg', 
                'record_btn_bg', 'left_panel', 'right_panel'
            ]
            
            for tag in items_to_pulse:
                try:
                    items = self.main_container.find_withtag(tag)
                    for item in items:
                        # Get current outline color and adjust opacity
                        current_color = self.main_container.itemcget(item, 'outline')
                        if current_color and '#' in current_color:
                            base_color = current_color[:7]  # Remove alpha if present
                            alpha = int(80 + 50 * pulse_intensity)
                            new_color = base_color + f'{alpha:02x}'
                            self.main_container.itemconfig(item, outline=new_color)
                except Exception:
                    pass
            
            self.window.after(60, self.animate_neon_pulse)
    
    def animate_energy_waves(self):
        """Animate flowing energy waves"""
        if hasattr(self, 'main_container'):
            self.wave_offset += 0.1
            
            # Update wave positions
            try:
                wave_items = self.main_container.find_withtag('energy_wave')
                width = self.window.winfo_width() or 1800
                height = self.window.winfo_height() or 1100
                
                for i, wave in enumerate(wave_items):
                    wave_points = []
                    y_base = height * (0.3 + i * 0.2)
                    
                    for x in range(0, width, 20):
                        wave_y = y_base + math.sin(x * 0.01 + self.wave_offset + i * 2) * 40
                        wave_points.extend([x, wave_y])
                    
                    if len(wave_points) >= 4:
                        self.main_container.coords(wave, *wave_points)
                        
                        # Animate wave opacity
                        wave_alpha = int(30 + 20 * math.sin(self.wave_offset + i))
                        wave_color = self.theme['accent_primary'] + f'{wave_alpha:02x}'
                        self.main_container.itemconfig(wave, fill=wave_color)
            except Exception:
                pass
            
            self.window.after(40, self.animate_energy_waves)
    
    def animate_title_glow(self):
        """Animate title glow effect"""
        if hasattr(self, 'main_container'):
            glow_phase = time.time() * 2
            
            try:
                # Animate title color shifting
                title_items = self.main_container.find_withtag('title')
                subtitle_items = self.main_container.find_withtag('subtitle')
                
                # Color cycle for title
                colors = [self.theme['neon_blue'], self.theme['neon_purple'], self.theme['neon_pink']]
                color_index = int(glow_phase) % len(colors)
                
                for item in title_items:
                    self.main_container.itemconfig(item, fill=colors[color_index])
                
                # Subtitle pulsing
                subtitle_alpha = int(200 + 55 * math.sin(glow_phase * 1.5))
                subtitle_color = self.theme['neon_purple'][:7] + f'{subtitle_alpha:02x}'
                
                for item in subtitle_items:
                    self.main_container.itemconfig(item, fill=subtitle_color)
                    
            except Exception:
                pass
            
            self.window.after(100, self.animate_title_glow)
    
    def animate_constellation_twinkle(self):
        """Animate constellation twinkling"""
        if hasattr(self, 'main_container'):
            try:
                constellation_items = self.main_container.find_withtag('constellation')
                
                for item in constellation_items:
                    # Random twinkling
                    if random.random() < 0.1:  # 10% chance to twinkle
                        # Brightness variation
                        alpha_values = ['20', '40', '60', '80', 'ff']
                        alpha = random.choice(alpha_values)
                        color = self.theme['accent_primary'] + alpha
                        self.main_container.itemconfig(item, fill=color)
                        
                        # Size variation
                        if random.random() < 0.05:  # 5% chance for size change
                            font_size = random.randint(8, 18)
                            current_font = self.main_container.itemcget(item, 'font')
                            font_family = current_font.split()[0] if current_font else 'Arial'
                            new_font = (font_family, font_size)
                            self.main_container.itemconfig(item, font=new_font)
                            
            except Exception:
                pass
            
            self.window.after(500, self.animate_constellation_twinkle)
    
    # Essential UI methods for functionality
    def toggle_theme(self):
        \"\"\"Toggle between dark and light themes with smooth transition\"\"\"
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme = self.themes[self.current_theme]
        
        # Update theme button
        theme_icon = \"🌙\" if self.current_theme == 'light' else \"☀️\"
        try:
            theme_items = self.main_container.find_withtag('theme_btn')
            for item in theme_items:
                self.main_container.itemconfig(item, text=theme_icon)
        except:
            pass
        
        # Recreate UI with new theme
        self.refresh_ui_theme()
    
    def refresh_ui_theme(self):
        \"\"\"Refresh UI elements with new theme colors\"\"\"
        # This would recreate the entire UI - simplified for now
        print(f\"✨ Switched to {self.current_theme} theme\")
    
    def show_settings(self):
        \"\"\"Show ultra stunning settings window\"\"\"
        settings_window = tk.Toplevel(self.window)
        settings_window.title(\"⚙️ Ultra Settings\")
        settings_window.geometry(\"800x600\")
        settings_window.configure(bg=self.theme['bg_primary'])
        settings_window.transient(self.window)
        
        # Center settings window
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 400
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 300
        settings_window.geometry(f\"800x600+{x}+{y}\")
        
        # Add settings content
        settings_label = tk.Label(
            settings_window,
            text=\"🎨 Ultra Premium Settings\",
            font=(\"JetBrains Mono\", 20, \"bold\"),
            fg=self.theme['neon_blue'],
            bg=self.theme['bg_primary']
        )
        settings_label.pack(pady=30)
        
        # Settings info
        info_text = \"\"\"
🎯 Audio Quality: Ultra Premium
🎨 Visual Effects: Maximum
⚡ Performance: Optimized
🔊 Voice Recognition: Advanced AI
🌟 Animation Level: Stunning
💾 Auto-Save: Enabled
🎪 Theme: {}
        \"\"\".format(self.current_theme.title())
        
        info_label = tk.Label(
            settings_window,
            text=info_text,
            font=(\"JetBrains Mono\", 12),
            fg=self.theme['text_primary'],
            bg=self.theme['bg_primary'],
            justify=tk.LEFT
        )
        info_label.pack(pady=20)
    
    def toggle_transcription(self):
        \"\"\"Toggle transcription on/off with stunning visual feedback\"\"\"
        self.is_recording = not self.is_recording
        
        if self.is_recording:
            # Start transcription
            button_text = \"🛑 Stop Transcription\"
            button_color = self.theme['error']
            status_text = \"🎙️ Recording in progress...\"
            status_color = self.theme['success']
            print(\"✨ Ultra transcription started!\")
            
            # Call start callback if set
            if self.start_callback:
                threading.Thread(target=self.start_callback, daemon=True).start()
        else:
            # Stop transcription
            button_text = \"🎙️ Start Transcription\"
            button_color = self.theme['neon_blue']
            status_text = \"⏸️ Ready to start\"
            status_color = self.theme['text_tertiary']
            print(\"✨ Ultra transcription stopped!\")
            
            # Call stop callback if set
            if self.stop_callback:
                threading.Thread(target=self.stop_callback, daemon=True).start()
        
        # Update UI elements
        try:
            # Update record button
            record_btn_items = self.main_container.find_withtag('record_btn_text')
            for item in record_btn_items:
                self.main_container.itemconfig(item, text=button_text)
            
            record_btn_bg_items = self.main_container.find_withtag('record_btn_bg')
            for item in record_btn_bg_items:
                self.main_container.itemconfig(item, outline=button_color)
            
            # Update status indicator
            status_items = self.main_container.find_withtag('status_indicator')
            for item in status_items:
                self.main_container.itemconfig(item, fill=status_color, outline=status_color)
            
            status_text_items = self.main_container.find_withtag('status_text')
            for item in status_text_items:
                self.main_container.itemconfig(item, text=status_text)
        except:
            pass
    
    def clear_transcript(self):
        \"\"\"Clear transcript with confirmation and beautiful animation\"\"\"
        if self.transcript_data:
            result = messagebox.askyesno(
                \"Clear Transcript\",
                \"Are you sure you want to clear the entire transcript?\\n\\nThis action cannot be undone.\",
                icon=messagebox.WARNING
            )
            
            if result:
                self.transcript_data.clear()
                self.transcript_area.config(state=tk.NORMAL)
                self.transcript_area.delete(1.0, tk.END)
                self.transcript_area.config(state=tk.DISABLED)
                
                # Add cleared message with animation
                self.add_system_message(\"🗑️ Transcript cleared\", \"system_message\")
                print(\"✨ Ultra transcript cleared!\")
    
    def export_transcript(self):
        \"\"\"Export transcript with multiple format options\"\"\"
        if not self.transcript_data:
            messagebox.showinfo(\"Export Transcript\", \"No transcript data to export.\")
            return
        
        # File format selection
        file_types = [
            (\"Text files\", \"*.txt\"),
            (\"JSON files\", \"*.json\"),
            (\"Word documents\", \"*.docx\"),
            (\"All files\", \"*.*\")\n        ]\n        \n        filename = filedialog.asksaveasfilename(\n            title=\"Export Ultra Transcript\",\n            defaultextension=\".txt\",\n            filetypes=file_types\n        )\n        \n        if filename:\n            try:\n                if filename.endswith('.json'):\n                    self.export_json(filename)\n                elif filename.endswith('.docx'):\n                    self.export_docx(filename)\n                else:\n                    self.export_text(filename)\n                \n                messagebox.showinfo(\"Export Complete\", f\"Transcript exported to:\\n{filename}\")\n                print(f\"✨ Ultra transcript exported to: {filename}\")\n            except Exception as e:\n                messagebox.showerror(\"Export Error\", f\"Failed to export transcript:\\n{e}\")\n    \n    def export_text(self, filename):\n        \"\"\"Export as plain text\"\"\"\n        with open(filename, 'w', encoding='utf-8') as f:\n            f.write(\"🎭 Albanian Teams Transcriber - Ultra Premium Edition\\n\")\n            f.write(\"=\" * 60 + \"\\n\\n\")\n            \n            for entry in self.transcript_data:\n                f.write(f\"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}\\n\")\n                if 'confidence' in entry:\n                    f.write(f\"   Confidence: {entry['confidence']}\\n\")\n                if 'engine' in entry:\n                    f.write(f\"   Engine: {entry['engine']}\\n\")\n                f.write(\"\\n\")\n    \n    def export_json(self, filename):\n        \"\"\"Export as JSON with metadata\"\"\"\n        export_data = {\n            \"metadata\": {\n                \"app\": \"Albanian Teams Transcriber - Ultra Premium\",\n                \"export_time\": datetime.now().isoformat(),\n                \"total_entries\": len(self.transcript_data),\n                \"participants\": list(self.participants.keys()) if hasattr(self, 'participants') else []\n            },\n            \"transcript\": self.transcript_data\n        }\n        \n        with open(filename, 'w', encoding='utf-8') as f:\n            json.dump(export_data, f, indent=2, ensure_ascii=False)\n    \n    def export_docx(self, filename):\n        \"\"\"Export as Word document (requires python-docx)\"\"\"\n        try:\n            from docx import Document\n            from docx.shared import Inches, RGBColor\n            from docx.enum.text import WD_ALIGN_PARAGRAPH\n            \n            doc = Document()\n            \n            # Add title\n            title = doc.add_heading('🎭 Albanian Teams Transcriber', 0)\n            title.alignment = WD_ALIGN_PARAGRAPH.CENTER\n            \n            subtitle = doc.add_heading('Ultra Premium Edition - Transcript Export', level=2)\n            subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER\n            \n            # Add metadata\n            doc.add_paragraph(f\"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\")\n            doc.add_paragraph(f\"Total Entries: {len(self.transcript_data)}\")\n            doc.add_paragraph(\"\")\n            \n            # Add transcript entries\n            for entry in self.transcript_data:\n                p = doc.add_paragraph()\n                p.add_run(f\"[{entry['timestamp']}] \").bold = True\n                p.add_run(f\"{entry['speaker']}: \").bold = True\n                p.add_run(entry['text'])\n                \n                if 'confidence' in entry or 'engine' in entry:\n                    meta_p = doc.add_paragraph()\n                    meta_text = \"\"\n                    if 'confidence' in entry:\n                        meta_text += f\"Confidence: {entry['confidence']} \"\n                    if 'engine' in entry:\n                        meta_text += f\"Engine: {entry['engine']}\"\n                    meta_p.add_run(meta_text).italic = True\n            \n            doc.save(filename)\n        except ImportError:\n            # Fallback to text export if python-docx not available\n            self.export_text(filename.replace('.docx', '.txt'))\n    \n    def add_system_message(self, message, tag=\"system_message\"):\n        \"\"\"Add a system message to the transcript\"\"\"\n        self.transcript_area.config(state=tk.NORMAL)\n        \n        timestamp = datetime.now().strftime(\"%H:%M:%S\")\n        full_message = f\"[{timestamp}] {message}\\n\\n\"\n        \n        self.transcript_area.insert(tk.END, full_message, tag)\n        \n        if self.auto_scroll_enabled:\n            self.transcript_area.see(tk.END)\n        \n        self.transcript_area.config(state=tk.DISABLED)\n    \n    def update_transcript(self, speaker, text, timestamp, enhanced_result=None):\n        \"\"\"Update transcript with ultra stunning formatting\"\"\"\n        # Add to transcript data\n        entry = {\n            'timestamp': timestamp,\n            'speaker': speaker,\n            'text': text\n        }\n        \n        if enhanced_result:\n            if 'confidence' in enhanced_result:\n                entry['confidence'] = enhanced_result['confidence']\n            if 'engine' in enhanced_result:\n                entry['engine'] = enhanced_result['engine']\n        \n        self.transcript_data.append(entry)\n        \n        # Update UI\n        self.transcript_area.config(state=tk.NORMAL)\n        \n        # Speaker name with avatar\n        speaker_color_index = hash(speaker) % len(self.speaker_colors)\n        avatar = self.speaker_colors[speaker_color_index]['avatar']\n        \n        # Add speaker line\n        speaker_line = f\"\\n{avatar} {speaker}\\n\"\n        self.transcript_area.insert(tk.END, speaker_line, f\"speaker_name_{speaker_color_index}\")\n        \n        # Add timestamp\n        time_line = f\"[{timestamp}] \"\n        self.transcript_area.insert(tk.END, time_line, \"timestamp\")\n        \n        # Add text\n        self.transcript_area.insert(tk.END, f\"{text}\\n\", f\"speaker_{speaker_color_index}\")\n        \n        # Add metadata if available\n        if enhanced_result:\n            metadata_parts = []\n            if 'confidence' in enhanced_result:\n                conf = enhanced_result['confidence']\n                if isinstance(conf, (int, float)):\n                    if conf > 0.8:\n                        conf_tag = \"confidence_high\"\n                        conf_text = f\"✅ {conf:.1%}\"\n                    elif conf > 0.6:\n                        conf_tag = \"confidence_medium\"\n                        conf_text = f\"⚠️ {conf:.1%}\"\n                    else:\n                        conf_tag = \"confidence_low\"\n                        conf_text = f\"❌ {conf:.1%}\"\n                else:\n                    conf_tag = \"confidence_medium\"\n                    conf_text = f\"📊 {conf}\"\n                \n                self.transcript_area.insert(tk.END, f\"   Confidence: {conf_text}\", conf_tag)\n            \n            if 'engine' in enhanced_result:\n                engine_text = f\"   🔧 Engine: {enhanced_result['engine']}\"\n                self.transcript_area.insert(tk.END, engine_text, \"engine_info\")\n            \n            if 'enhancements_applied' in enhanced_result and enhanced_result['enhancements_applied']:\n                self.transcript_area.insert(tk.END, \"   ✨ Enhanced\", \"enhanced\")\n        \n        self.transcript_area.insert(tk.END, \"\\n\")\n        \n        # Auto-scroll if enabled\n        if self.auto_scroll_enabled:\n            self.transcript_area.see(tk.END)\n        \n        self.transcript_area.config(state=tk.DISABLED)\n    \n    def update_participants(self, participants):\n        \"\"\"Update participants display with avatars\"\"\"\n        self.participants = participants\n        \n        if participants:\n            participant_text = \"✨ Active Participants:\\n\\n\"\n            for i, (name, info) in enumerate(participants.items()):\n                color_index = i % len(self.speaker_colors)\n                avatar = self.speaker_colors[color_index]['avatar']\n                detection_method = info.get('detection_method', 'Unknown')\n                confidence = info.get('confidence', 'Medium')\n                \n                participant_text += f\"{avatar} {name}\\n\"\n                participant_text += f\"   📡 {detection_method}\\n\"\n                participant_text += f\"   🎯 {confidence}\\n\\n\"\n        else:\n            participant_text = \"🔍 Detecting participants...\"\n        \n        try:\n            participants_items = self.main_container.find_withtag('participants_text')\n            for item in participants_items:\n                self.main_container.itemconfig(item, text=participant_text)\n        except:\n            pass\n    \n    def update_teams_status(self, is_meeting, reason):\n        \"\"\"Update Teams status with beautiful indicators\"\"\"\n        if is_meeting:\n            teams_text = f\"✅ Teams: Active meeting\\n   📡 {reason}\"\n            teams_color = self.theme['success']\n            teams_icon = \"📱\"\n        else:\n            teams_text = f\"🔍 Teams: Scanning...\\n   📡 {reason}\"\n            teams_color = self.theme['warning']\n            teams_icon = \"📴\"\n        \n        try:\n            teams_items = self.main_container.find_withtag('teams_text')\n            for item in teams_items:\n                self.main_container.itemconfig(item, text=teams_text)\n            \n            teams_indicator_items = self.main_container.find_withtag('teams_indicator')\n            for item in teams_indicator_items:\n                self.main_container.itemconfig(item, text=teams_icon, fill=teams_color)\n        except:\n            pass\n    \n    def set_callbacks(self, start_callback=None, stop_callback=None):\n        \"\"\"Set callback functions for start/stop transcription\"\"\"\n        self.start_callback = start_callback\n        self.stop_callback = stop_callback\n    \n    def on_window_resize(self, event):\n        \"\"\"Handle window resize with smooth animations\"\"\"\n        if event.widget == self.window:\n            # Recreate gradient background for new size\n            if hasattr(self, 'main_container'):\n                self.main_container.delete(\"gradient\")\n                self.create_magical_background()\n    \n    def run(self):\n        \"\"\"Run the ultra stunning UI\"\"\"\n        try:\n            self.window.mainloop()\n        except KeyboardInterrupt:\n            print(\"\\n✨ Ultra stunning UI closed gracefully\")\n    \n    def destroy(self):\n        \"\"\"Destroy the UI window\"\"\"\n        try:\n            self.window.destroy()\n        except:\n            pass
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
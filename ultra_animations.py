import math
import random

class UltraAnimations:
    """Ultra beautiful animation methods for the stunning UI"""
    
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
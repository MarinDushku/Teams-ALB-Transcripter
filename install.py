#!/usr/bin/env python3
"""
Installation script for Albanian Teams Transcriber
Handles dependencies, shortcuts, and setup
"""

import os
import sys
import subprocess
import platform
import tkinter as tk
from tkinter import messagebox, ttk
import threading
from pathlib import Path

class TranscriberInstaller:
    def __init__(self):
        self.system = platform.system()
        self.app_dir = Path(__file__).parent.absolute()
        
        # GUI setup
        self.root = tk.Tk()
        self.root.title("Albanian Teams Transcriber - Installer")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        self.center_window()
        self.setup_ui()
        
        # Installation state
        self.installation_steps = [
            ("Checking Python installation", self.check_python),
            ("Installing Python dependencies", self.install_dependencies),
            ("Setting up Albanian ASR", self.setup_albanian_asr),
            ("Creating desktop shortcuts", self.create_shortcuts),
            ("Finalizing installation", self.finalize_installation)
        ]
        self.current_step = 0
        self.total_steps = len(self.installation_steps)
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the installer UI"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2196F3', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Albanian Teams Transcriber",
            font=("Arial", 20, "bold"),
            fg='white',
            bg='#2196F3'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Installation & Setup Wizard",
            font=("Arial", 12),
            fg='white',
            bg='#2196F3'
        )
        subtitle_label.pack()
        
        # Main content
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Welcome message
        welcome_label = tk.Label(
            content_frame,
            text="Welcome to the Albanian Teams Transcriber installer!\n\n"
                 "This wizard will help you set up everything needed for real-time\n"
                 "Albanian transcription of Microsoft Teams meetings.",
            font=("Arial", 11),
            bg='#f0f0f0',
            justify=tk.LEFT
        )
        welcome_label.pack(pady=(0, 20))
        
        # System info
        info_frame = tk.LabelFrame(content_frame, text="System Information", font=("Arial", 10, "bold"))
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        system_info = f"""Operating System: {platform.system()} {platform.release()}
Python Version: {platform.python_version()}
Architecture: {platform.machine()}
Installation Directory: {self.app_dir}"""
        
        info_label = tk.Label(
            info_frame,
            text=system_info,
            font=("Courier", 9),
            bg='white',
            relief=tk.SUNKEN,
            anchor=tk.W,
            justify=tk.LEFT
        )
        info_label.pack(fill=tk.X, padx=10, pady=10)
        
        # Progress section
        progress_frame = tk.LabelFrame(content_frame, text="Installation Progress", font=("Arial", 10, "bold"))
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(padx=10, pady=(10, 5))
        
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to install",
            font=("Arial", 10),
            bg='#f0f0f0'
        )
        self.status_label.pack(pady=(0, 10))
        
        # Log area
        log_frame = tk.LabelFrame(content_frame, text="Installation Log", font=("Arial", 10, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.log_text = tk.Text(
            log_frame,
            height=8,
            font=("Courier", 8),
            bg='black',
            fg='green',
            wrap=tk.WORD
        )
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10, padx=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        self.install_btn = tk.Button(
            button_frame,
            text="Start Installation",
            command=self.start_installation,
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            width=15,
            height=2
        )
        self.install_btn.pack(side=tk.LEFT)
        
        self.cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.root.quit,
            font=("Arial", 10),
            bg='#f44336',
            fg='white',
            width=10
        )
        self.cancel_btn.pack(side=tk.RIGHT)
        
    def log(self, message):
        """Add message to installation log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_progress(self, step_name):
        """Update progress bar and status"""
        progress = (self.current_step / self.total_steps) * 100
        self.progress_var.set(progress)
        self.status_label.config(text=f"Step {self.current_step + 1}/{self.total_steps}: {step_name}")
        self.root.update()
    
    def start_installation(self):
        """Start the installation process"""
        self.install_btn.config(state=tk.DISABLED, text="Installing...")
        self.log("Starting Albanian Teams Transcriber installation...")
        
        # Run installation in separate thread
        threading.Thread(target=self.run_installation, daemon=True).start()
    
    def run_installation(self):
        """Run all installation steps"""
        try:
            for i, (step_name, step_function) in enumerate(self.installation_steps):
                self.current_step = i
                self.update_progress(step_name)
                self.log(f"\n--- {step_name} ---")
                
                success = step_function()
                if not success:
                    self.log(f"ERROR: {step_name} failed!")
                    self.installation_failed()
                    return
                
                self.log(f"✓ {step_name} completed successfully")
            
            # Installation completed
            self.current_step = self.total_steps
            self.update_progress("Installation Complete")
            self.installation_completed()
            
        except Exception as e:
            self.log(f"FATAL ERROR: {e}")
            self.installation_failed()
    
    def check_python(self):
        """Check Python installation"""
        try:
            version = sys.version_info
            self.log(f"Python {version.major}.{version.minor}.{version.micro} detected")
            
            if version.major < 3 or (version.major == 3 and version.minor < 7):
                self.log("ERROR: Python 3.7+ required")
                return False
            
            self.log("Python version OK")
            return True
            
        except Exception as e:
            self.log(f"Python check failed: {e}")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        try:
            self.log("Installing dependencies from requirements.txt...")
            
            # Read requirements
            req_file = self.app_dir / "requirements.txt"
            if not req_file.exists():
                self.log("requirements.txt not found")
                return False
            
            # Install via pip
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(req_file)
            ], capture_output=True, text=True, cwd=self.app_dir)
            
            self.log(result.stdout)
            if result.stderr:
                self.log(f"Warnings: {result.stderr}")
            
            if result.returncode == 0:
                self.log("Dependencies installed successfully")
                return True
            else:
                self.log(f"Dependency installation failed with code {result.returncode}")
                return False
            
        except Exception as e:
            self.log(f"Dependency installation error: {e}")
            return False
    
    def setup_albanian_asr(self):
        """Setup Albanian ASR model"""
        try:
            self.log("Setting up Albanian ASR model...")
            
            # Check if already exists
            asr_dir = self.app_dir / "Albanian-ASR"
            if asr_dir.exists():
                self.log("Albanian-ASR directory already exists")
                return True
            
            # Clone repository
            self.log("Cloning Albanian-ASR repository...")
            result = subprocess.run([
                "git", "clone", "https://github.com/florijanqosja/Albanian-ASR.git"
            ], capture_output=True, text=True, cwd=self.app_dir)
            
            if result.returncode != 0:
                self.log("Git clone failed - Albanian ASR will need manual setup")
                self.log("You can download from: https://github.com/florijanqosja/Albanian-ASR")
                return True  # Don't fail installation for this
            
            self.log("Albanian-ASR cloned successfully")
            
            # Install ASR dependencies
            asr_req = asr_dir / "requirements.txt"
            if asr_req.exists():
                self.log("Installing Albanian-ASR dependencies...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(asr_req)
                ], cwd=asr_dir)
            
            return True
            
        except Exception as e:
            self.log(f"Albanian ASR setup warning: {e}")
            return True  # Don't fail installation for this
    
    def create_shortcuts(self):
        """Create desktop shortcuts"""
        try:
            self.log("Creating desktop shortcuts...")
            
            # Run the shortcut creation script
            shortcut_script = self.app_dir / "create_desktop_shortcut.py"
            if shortcut_script.exists():
                result = subprocess.run([
                    sys.executable, str(shortcut_script)
                ], capture_output=True, text=True)
                
                self.log(result.stdout)
                if result.stderr:
                    self.log(f"Shortcut warnings: {result.stderr}")
            
            return True
            
        except Exception as e:
            self.log(f"Shortcut creation warning: {e}")
            return True  # Don't fail installation for this
    
    def finalize_installation(self):
        """Finalize the installation"""
        try:
            self.log("Finalizing installation...")
            
            # Create installation marker
            marker_file = self.app_dir / ".installed"
            with open(marker_file, 'w') as f:
                f.write(f"Installed on {platform.system()} at {self.app_dir}\n")
            
            self.log("Installation marker created")
            return True
            
        except Exception as e:
            self.log(f"Finalization error: {e}")
            return False
    
    def installation_completed(self):
        """Handle successful installation"""
        self.progress_var.set(100)
        self.status_label.config(text="Installation completed successfully!")
        
        self.install_btn.config(
            text="Launch Application",
            command=self.launch_application,
            state=tk.NORMAL,
            bg='#4CAF50'
        )
        
        self.log("\n" + "="*50)
        self.log("INSTALLATION COMPLETED SUCCESSFULLY!")
        self.log("="*50)
        self.log("\nYou can now:")
        self.log("• Click 'Launch Application' to start the transcriber")
        self.log("• Use the desktop shortcut")
        self.log("• Run 'python main.py' from the command line")
        
        messagebox.showinfo(
            "Installation Complete",
            "Albanian Teams Transcriber has been installed successfully!\n\n"
            "You can now launch the application or find it on your desktop."
        )
    
    def installation_failed(self):
        """Handle failed installation"""
        self.status_label.config(text="Installation failed - see log for details")
        self.install_btn.config(text="Installation Failed", state=tk.DISABLED, bg='#f44336')
        
        messagebox.showerror(
            "Installation Failed",
            "The installation encountered errors. Please check the log for details.\n\n"
            "You may need to install dependencies manually or run as administrator."
        )
    
    def launch_application(self):
        """Launch the main application"""
        try:
            launcher_script = self.app_dir / "run_transcriber.py"
            subprocess.Popen([sys.executable, str(launcher_script)])
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch application:\n{e}")
    
    def run(self):
        """Start the installer"""
        self.root.mainloop()

def main():
    """Main installer entry point"""
    installer = TranscriberInstaller()
    installer.run()

if __name__ == "__main__":
    main()
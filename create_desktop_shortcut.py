#!/usr/bin/env python3
"""
Script to create desktop shortcuts for Albanian Teams Transcriber
Works on Windows, macOS, and Linux
"""

import os
import sys
import platform
from pathlib import Path

class ShortcutCreator:
    def __init__(self):
        self.app_name = "Albanian Teams Transcriber"
        self.app_dir = Path(__file__).parent.absolute()
        self.system = platform.system()
        
    def create_shortcuts(self):
        """Create desktop shortcuts for the current operating system"""
        try:
            if self.system == "Windows":
                self.create_windows_shortcuts()
            elif self.system == "Darwin":  # macOS
                self.create_macos_shortcuts()
            elif self.system == "Linux":
                self.create_linux_shortcuts()
            else:
                print(f"Unsupported operating system: {self.system}")
                return False
            
            print(f"Desktop shortcuts created successfully for {self.system}!")
            return True
            
        except Exception as e:
            print(f"Error creating shortcuts: {e}")
            return False
    
    def create_windows_shortcuts(self):
        """Create Windows desktop shortcuts"""
        try:
            import winshell
            from win32com.client import Dispatch
        except ImportError:
            print("Installing required packages for Windows shortcuts...")
            os.system("pip install winshell pywin32")
            import winshell
            from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        
        # Create shortcut for GUI launcher
        shortcut_path = os.path.join(desktop, f"{self.app_name}.lnk")
        target = str(self.app_dir / "run_transcriber.py")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = str(self.app_dir)
        shortcut.IconLocation = sys.executable
        shortcut.Description = "Albanian Teams Transcriber - Real-time meeting transcription"
        shortcut.save()
        
        # Create shortcut for batch file
        batch_shortcut_path = os.path.join(desktop, f"{self.app_name} (Batch).lnk")
        batch_target = str(self.app_dir / "Albanian_Teams_Transcriber.bat")
        
        batch_shortcut = shell.CreateShortCut(batch_shortcut_path)
        batch_shortcut.Targetpath = batch_target
        batch_shortcut.WorkingDirectory = str(self.app_dir)
        batch_shortcut.Description = "Albanian Teams Transcriber - Command line launcher"
        batch_shortcut.save()
        
        print(f"Created shortcuts:")
        print(f"  - {shortcut_path}")
        print(f"  - {batch_shortcut_path}")
    
    def create_macos_shortcuts(self):
        """Create macOS desktop shortcuts (aliases)"""
        desktop = Path.home() / "Desktop"
        
        # Create alias for GUI launcher
        alias_path = desktop / f"{self.app_name}.command"
        target = self.app_dir / "run_transcriber.py"
        
        script_content = f"""#!/bin/bash
cd "{self.app_dir}"
python3 "{target}"
"""
        
        with open(alias_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(alias_path, 0o755)
        
        print(f"Created shortcut: {alias_path}")
    
    def create_linux_shortcuts(self):
        """Create Linux desktop shortcuts (.desktop files)"""
        desktop = Path.home() / "Desktop"
        applications = Path.home() / ".local/share/applications"
        
        # Ensure applications directory exists
        applications.mkdir(parents=True, exist_ok=True)
        
        # Desktop entry content
        desktop_entry = f"""[Desktop Entry]
Name={self.app_name}
Comment=Real-time Albanian transcription for Teams meetings
Exec=python3 "{self.app_dir}/run_transcriber.py"
Path={self.app_dir}
Icon=audio-recorder
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Recorder;
Keywords=transcription;teams;albanian;speech;recording;
StartupNotify=true
"""
        
        # Create desktop shortcut
        desktop_file = desktop / f"{self.app_name.replace(' ', '_')}.desktop"
        with open(desktop_file, 'w') as f:
            f.write(desktop_entry)
        os.chmod(desktop_file, 0o755)
        
        # Create applications menu entry
        app_file = applications / f"{self.app_name.replace(' ', '_')}.desktop"
        with open(app_file, 'w') as f:
            f.write(desktop_entry)
        os.chmod(app_file, 0o755)
        
        print(f"Created shortcuts:")
        print(f"  - Desktop: {desktop_file}")
        print(f"  - Applications: {app_file}")
    
    def create_start_menu_entry(self):
        """Create Windows Start Menu entry"""
        if self.system != "Windows":
            return
        
        try:
            import winshell
            programs = winshell.programs()
            
            # Create application folder
            app_folder = os.path.join(programs, self.app_name)
            os.makedirs(app_folder, exist_ok=True)
            
            # Create start menu shortcut
            shortcut_path = os.path.join(app_folder, f"{self.app_name}.lnk")
            target = str(self.app_dir / "run_transcriber.py")
            
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = str(self.app_dir)
            shortcut.IconLocation = sys.executable
            shortcut.save()
            
            print(f"Created Start Menu entry: {shortcut_path}")
            
        except Exception as e:
            print(f"Failed to create Start Menu entry: {e}")

def main():
    """Main function"""
    print("Creating desktop shortcuts for Albanian Teams Transcriber...")
    print("=" * 60)
    
    creator = ShortcutCreator()
    
    # Create desktop shortcuts
    success = creator.create_shortcuts()
    
    # Create Start Menu entry on Windows
    if creator.system == "Windows":
        creator.create_start_menu_entry()
    
    if success:
        print("\n" + "=" * 60)
        print("SUCCESS! Shortcuts have been created.")
        print("\nYou can now:")
        if creator.system == "Windows":
            print("  - Double-click the desktop shortcut")
            print("  - Find the app in Start Menu")
            print("  - Run the .bat file directly")
        else:
            print("  - Double-click the desktop shortcut")
            print("  - Find the app in your applications menu (Linux)")
        
        print(f"\nTo remove shortcuts later, delete them from:")
        if creator.system == "Windows":
            print(f"  - Desktop")
            print(f"  - Start Menu > {creator.app_name}")
        elif creator.system == "Linux":
            print(f"  - Desktop and ~/.local/share/applications/")
        else:
            print(f"  - Desktop")

if __name__ == "__main__":
    main()
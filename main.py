#!/usr/bin/env python3
"""
SyndraShell - Main Application
Powered by Fabric Framework
"""

import os
import gi

gi.require_version("GLib", "2.0")
import setproctitle
from fabric import Application
from fabric.utils import exec_shell_command_async, get_relative_path
from gi.repository import GLib

from config.data import APP_NAME, APP_NAME_CAP, CACHE_DIR, CONFIG_FILE, HOME_DIR
from modules.bar import Bar
from modules.notch import Notch
from modules.dock import Dock

fonts_updated_file = f"{CACHE_DIR}/fonts_updated"

if __name__ == "__main__":
    setproctitle.setproctitle(APP_NAME)

    # Ensure config exists
    if not os.path.isfile(CONFIG_FILE):
        config_script_path = get_relative_path("config/config.py")
        exec_shell_command_async(f"python {config_script_path}")

    # Set default wallpaper if none exists
    current_wallpaper = os.path.expanduser("~/.current.wall")
    if not os.path.exists(current_wallpaper):
        example_wallpaper = os.path.expanduser(
            f"~/.config/{APP_NAME_CAP}/assets/wallpapers_example/example-1.jpg"
        )
        if os.path.exists(example_wallpaper):
            os.system(f"cp '{example_wallpaper}' '{current_wallpaper}'")

    # Download fonts if not already done
    if not os.path.exists(fonts_updated_file):
        os.system(f"mkdir -p {CACHE_DIR}")
        
        def download_fonts():
            font_dir = os.path.expanduser("~/.fonts")
            os.makedirs(font_dir, exist_ok=True)
            
            # Download Zed Sans font
            os.system(
                f"wget -q https://github.com/zed-industries/zed-fonts/releases/latest/download/zed-sans.zip -O /tmp/zed-sans.zip && "
                f"unzip -q -o /tmp/zed-sans.zip -d {font_dir} && "
                f"rm /tmp/zed-sans.zip"
            )
            
            # Update font cache
            os.system("fc-cache -f")
            
            # Mark fonts as updated
            with open(fonts_updated_file, "w") as f:
                f.write("1")
            
            print("Fonts downloaded successfully")
        
        GLib.idle_add(download_fonts)

    # Create app components
    app_components = []
    
    # Create bar, notch, and dock
    bar = Bar()
    notch = Notch()
    dock = Dock()
    
    app_components.extend([bar, notch, dock])

    # Create the application with all components
    app = Application(f"{APP_NAME}", *app_components)

    def set_css():
        """Load main stylesheet"""
        app.set_stylesheet_from_file(
            get_relative_path("main.css"),
        )
    
    app.set_css = set_css
    app.set_css()

    app.run()

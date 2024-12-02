import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk  # For handling icons
import platform
import psutil
import subprocess
import os

# Function to retrieve and format system information
def get_system_info():
    info = platform.uname()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    cpu_count = psutil.cpu_count(logical=True)
    total_ram = memory.total / (1024 ** 3)  # Convert bytes to GB
    available_ram = memory.available / (1024 ** 3)
    used_ram = memory.used / (1024 ** 3)
    total_disk = disk.total / (1024 ** 3)
    used_disk = disk.used / (1024 ** 3)
    free_disk = disk.free / (1024 ** 3)
    disk_usage = disk.percent

    # Return the formatted system info string
    return (
        f"System: {info.system}\n"
        f"Node Name: {info.node}\n"
        f"Release: {info.release}\n"
        f"Version: {info.version}\n"
        f"Machine: {info.machine}\n"
        f"Processor: {info.processor}\n\n"
        f"CPU Count: {cpu_count}\n"
        f"Total RAM: {total_ram:.2f} GB\n"
        f"Available RAM: {available_ram:.2f} GB\n"
        f"Used RAM: {used_ram:.2f} GB\n"
        f"Disk Total: {total_disk:.2f} GB\n"
        f"Disk Used: {used_disk:.2f} GB\n"
        f"Disk Free: {free_disk:.2f} GB\n"
        f"Disk Usage: {disk_usage}%\n"
    )

# Function to retrieve event logs (Windows only)
def get_event_logs():
    try:
        process = subprocess.Popen(
            ["powershell", "-Command", "Get-EventLog -LogName System -Newest 10"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()
        
        if stdout:
            return f"Event Logs (Newest 10):\n{stdout}"
        if stderr:
            return f"Error:\n{stderr}"
        return "No event logs found."

    except Exception as e:
        return f"Error: {e}"

# Function to display system information in the text box
def display_system_info():
    output_box.config(state=tk.NORMAL)  # Enable editing for displaying
    output_box.delete("1.0", tk.END)  # Clear the text box
    output_box.insert(tk.END, get_system_info())  # Insert system info
    output_box.config(state=tk.DISABLED)  # Make it read-only again

# Function to display event logs in the text box
def display_event_logs():
    output_box.config(state=tk.NORMAL)  # Enable editing for displaying
    output_box.delete("1.0", tk.END)  # Clear the text box
    output_box.insert(tk.END, get_event_logs())  # Insert event logs
    output_box.config(state=tk.DISABLED)  # Make it read-only again

# Function to clean up temporary files
def cleanup_temp_files():
    try:
        output_box.config(state=tk.NORMAL)  # Enable editing for displaying
        output_box.insert(tk.END, "Cleaning temporary files...\n")
        os.system("del /q /s %TEMP%\\*")
        output_box.config(state=tk.DISABLED)  # Make it read-only again
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, "Temporary files cleaned.\n\n")
        output_box.config(state=tk.DISABLED)
    except Exception as e:
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, f"Error: {e}\n")
        output_box.config(state=tk.DISABLED)

# Function to run disk cleanup
def cleanup_disk():
    try:
        output_box.config(state=tk.NORMAL)  # Enable editing for displaying
        output_box.insert(tk.END, "Running Disk Cleanup...\n")
        subprocess.run("cleanmgr /sagerun:1", shell=True)
        output_box.config(state=tk.DISABLED)  # Make it read-only again
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, "Disk Cleanup completed.\n\n")
        output_box.config(state=tk.DISABLED)
    except Exception as e:
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, f"Error: {e}\n")
        output_box.config(state=tk.DISABLED)

# Function to optimize the disk
def optimize_disk():
    try:
        output_box.config(state=tk.NORMAL)  # Enable editing for displaying
        output_box.insert(tk.END, "Optimizing disk...\n")
        os.system("defrag C:")
        output_box.config(state=tk.DISABLED)  # Make it read-only again
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, "Disk optimization completed.\n\n")
        output_box.insert(tk.END, "All tasks completed!\n")
        output_box.config(state=tk.DISABLED)
    except Exception as e:
        output_box.config(state=tk.NORMAL)
        output_box.insert(tk.END, f"Error: {e}\n")
        output_box.config(state=tk.DISABLED)

# Create the main GUI window
window = tk.Tk()
window.title("System Info and Cleanup App")
window.geometry("700x800")
window.resizable(False, False)

# Set the style
style = ttk.Style()
style.theme_use("clam")  # Use a modern theme
style.configure("TButton", font=("Arial", 12), padding=5)

# Load icons for buttons, with error handling if icons are missing
try:
    system_info_icon = ImageTk.PhotoImage(Image.open("system_info_icon.png").resize((32, 32)))
    event_logs_icon = ImageTk.PhotoImage(Image.open("event_logs_icon.png").resize((32, 32)))
    cleanup_icon = ImageTk.PhotoImage(Image.open("cleanup_icon.png").resize((32, 32)))  # Cleanup button icon
except FileNotFoundError:
    system_info_icon = event_logs_icon = cleanup_icon = None

# Frame for buttons
button_frame = ttk.Frame(window, padding=10)
button_frame.pack(side=tk.TOP, fill=tk.X)

# Buttons with icons
btn_system_info = ttk.Button(
    button_frame,
    text="System Info",
    image=system_info_icon if system_info_icon else "",
    compound=tk.LEFT,
    command=display_system_info,
    width=20,
)
btn_system_info.grid(row=0, column=0, padx=10, pady=5)

btn_event_logs = ttk.Button(
    button_frame,
    text="Event Logs",
    image=event_logs_icon if event_logs_icon else "",
    compound=tk.LEFT,
    command=display_event_logs,
    width=20,
)
btn_event_logs.grid(row=0, column=1, padx=10, pady=5)

btn_cleanup_temp = ttk.Button(
    button_frame,
    text="Cleanup Temp Files",
    image=cleanup_icon if cleanup_icon else "",
    compound=tk.LEFT,
    command=cleanup_temp_files,
    width=20,
)
btn_cleanup_temp.grid(row=1, column=0, padx=10, pady=5)

btn_cleanup_disk = ttk.Button(
    button_frame,
    text="Run Disk Cleanup",
    image=cleanup_icon if cleanup_icon else "",
    compound=tk.LEFT,
    command=cleanup_disk,
    width=20,
)
btn_cleanup_disk.grid(row=1, column=1, padx=10, pady=5)

btn_optimize_disk = ttk.Button(
    button_frame,
    text="Optimize Disk",
    image=cleanup_icon if cleanup_icon else "",
    compound=tk.LEFT,
    command=optimize_disk,
    width=20,
)
btn_optimize_disk.grid(row=1, column=2, padx=10, pady=5)

# Add a scrolled text box to display output
output_box = ScrolledText(window, width=80, height=20, font=("Courier New", 10))
output_box.pack(padx=10, pady=10)

# Run the main event loop
window.mainloop()


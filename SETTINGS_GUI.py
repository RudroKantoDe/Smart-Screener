import tkinter as tk
from tkinter import messagebox

def launch_settings():
    settings_win = tk.Toplevel()
    settings_win.title("⚙️ Settings")
    settings_win.geometry("400x400")
    settings_win.configure(bg="#f7faff")

    tk.Label(settings_win, text="Settings", font=("Arial", 18, "bold"), bg="#f7faff").pack(pady=20)

    theme_var = tk.StringVar(value="Light")
    tk.Label(settings_win, text="Theme:", font=("Arial", 12), bg="#f7faff").pack(anchor="w", padx=20)
    tk.OptionMenu(settings_win, theme_var, "Light", "Dark").pack(padx=20, pady=5)

    notify_var = tk.BooleanVar(value=True)
    tk.Checkbutton(settings_win, text="Enable Notifications", variable=notify_var,
                   bg="#f7faff", font=("Arial", 12)).pack(anchor="w", padx=20, pady=10)

    def clear_cache():
        messagebox.showinfo("Cache Cleared", "Temporary data has been cleared.")

    tk.Button(settings_win, text="🗑️ Clear Cache/Data", command=clear_cache,
              bg="#dc3545", fg="white", font=("Arial", 11)).pack(pady=10)

    tk.Label(settings_win, text="Developed by Rudro, Final Year CSE",
             font=("Arial", 10, "italic"), bg="#f7faff", fg="#555").pack(side="bottom", pady=10)

    settings_win.grab_set()
    settings_win.focus_force()

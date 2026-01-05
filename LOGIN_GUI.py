import tkinter as tk
from tkinter import messagebox
import entry_sql as sql
import FORGOTPASSWORD_GUI as fpsw
import session


def go_to_REGISTER():
    login_window.destroy()
    import REGISTER_GUI # Replace with your actual sign-in filename (without .py)
    REGISTER_GUI.launch_REGISTER_GUI()


def open_forgot_password():
    login_window.destroy()
    fpsw.launch_forgot_password()  #✅ Use the correct alias


def login(nav_buttons):
    username = entry_username.get()
    password = entry_password.get()

    if sql.exists(username):
        if sql.exists_psw(username, password):
            session.is_logged_in = True
            messagebox.showinfo("Login Success", f"Welcome, {username}!")

            # Enable navbar buttons
            for label, btn in nav_buttons.items():
                if label != "📊 Dashboard":
                    btn.config(state="normal")

            login_window.destroy()  # Close login popup only
        else:
            messagebox.showerror("Password Incorrect")
    else:
        messagebox.showerror("Login Failed", "Invalid Username")
            
# Tkinter Login Page
def launch_signin(nav_buttons):
    global login_window, entry_username, entry_password 
    
    login_window = tk.Toplevel()
    login_window.title("Login - Stock Screener")
    login_window.geometry("400x350")
    login_window.configure(bg="#f0f0f0")

    show_password = tk.BooleanVar(value=False)

    # Toggle password
    def toggle_password():
        if show_password.get():
            entry_password.config(show="")
        else:
            entry_password.config(show="*")

    tk.Label(login_window, text="Login", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

    frame = tk.Frame(login_window, bg="#f0f0f0")
    frame.pack()

    tk.Label(frame, text="Username:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, pady=10, sticky="e")
    entry_username = tk.Entry(frame, width=25)
    entry_username.grid(row=0, column=1, pady=10)

    tk.Label(frame, text="Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, pady=10, sticky="e")
    entry_password = tk.Entry(frame, width=25, show="*")
    entry_password.grid(row=1, column=1, pady=10)

    tk.Button(login_window, text="Login", width=15, command=lambda: login(nav_buttons), bg="#4CAF50", fg="white").pack(pady=20)

    show_pw_checkbox = tk.Checkbutton(frame, text="Show Password", variable=show_password,
                                      command=toggle_password, bg="#f0f0f0")
    show_pw_checkbox.grid(row=2, column=1, sticky="w", pady=5)

    tk.Button(login_window, text="Forgot Password?", font=("Arial", 10, "underline"),
              fg="#007ACC", bg="#f0f0f0", bd=0, command=open_forgot_password).pack()
    tk.Button(login_window, text="Don’t have an account? Register now", font=("Arial", 10, "underline"),
              fg="#007ACC", bg="#f0f0f0", bd=0, command=go_to_REGISTER).pack()

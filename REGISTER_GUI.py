import tkinter as tk
from tkinter import messagebox
import PSWCHECK as pw
import entry_sql as sq


# Placeholder function to check if email already exists
'''
def email_exists(email):
    try:
        result = sq.sqlread(email, 'check')  # Adjust logic if needed
        return True if result else False
    except:
        return False
'''



# GUI setup
root = tk.Tk()
root.title("User Registration")
root.geometry("500x540")
root.configure(bg="#f5f5f5")

show_password = tk.BooleanVar(value=False)

#Jumps to the sign-in page 
def go_to_signin():
    root.destroy()
    import LOGIN_GUI 
    LOGIN_GUI.launch_signin()  #Launching the sign in again in case of account being already created 
                                

    # ------------------ Submit Handler ------------------
def launch_REGISTER_GUI():
    def register_user():
        name = entry_name.get()
        email = entry_email.get()
        mobile = entry_mobile.get()
        state = entry_state.get()
        city = entry_city.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        # Validation
        if not name or not email or not mobile or not state or not city or not password or not confirm_password:
            messagebox.showwarning("Incomplete", "All fields are required.")
            return

        if not pw.CheckEmail(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        if sq.exists(email):
            messagebox.showerror("Already Exists", "This email is already registered.")
            return

        if not pw.CheckMobile(mobile):
            messagebox.showerror("Invalid Number", "Enter a valid 10-digit mobile number.")
            return

        if not pw.CheckPassword(password):
            messagebox.showerror("Weak Password", "Password does not meet security requirements.")
            return

        if password != confirm_password:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        try:
            sq.sqlsave(name, email, int(mobile), state, city, password)
            messagebox.showinfo("Success", "Registration completed successfully!")
            root.destroy()
            import LOGIN_GUI  # Replace with your actual sign-in module name
            LOGIN_GUI.launch_signin()

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save data: {e}")

    # ------------------ Password Show/Hide ------------------

    def toggle_password():
        if show_password.get():
            entry_password.config(show="")
            entry_confirm_password.config(show="")
        else:
            entry_password.config(show="*")
            entry_confirm_password.config(show="*")

    # ------------------ GUI Layout ------------------

    form_frame = tk.Frame(root, bg="#f5f5f5")
    form_frame.pack(pady=25)

    # Name
    tk.Label(form_frame, text="Name:", font=("Arial", 12), bg="#f5f5f5").grid(row=0, column=0, pady=8, sticky="e")
    entry_name = tk.Entry(form_frame, width=30)
    entry_name.grid(row=0, column=1)

    # Email
    tk.Label(form_frame, text="Email (Username):", font=("Arial", 12), bg="#f5f5f5").grid(row=1, column=0, pady=8, sticky="e")
    entry_email = tk.Entry(form_frame, width=30)
    entry_email.grid(row=1, column=1)

    # Mobile
    tk.Label(form_frame, text="WhatsApp Number:", font=("Arial", 12), bg="#f5f5f5").grid(row=2, column=0, pady=8, sticky="e")
    entry_mobile = tk.Entry(form_frame, width=30)
    entry_mobile.grid(row=2, column=1)

    # State
    tk.Label(form_frame, text="State:", font=("Arial", 12), bg="#f5f5f5").grid(row=3, column=0, pady=8, sticky="e")
    entry_state = tk.Entry(form_frame, width=30)
    entry_state.grid(row=3, column=1)

    # City
    tk.Label(form_frame, text="City/Town:", font=("Arial", 12), bg="#f5f5f5").grid(row=4, column=0, pady=8, sticky="e")
    entry_city = tk.Entry(form_frame, width=30)
    entry_city.grid(row=4, column=1)

    # Password
    tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="#f5f5f5").grid(row=5, column=0, pady=8, sticky="e")
    entry_password = tk.Entry(form_frame, width=30, show="*")
    entry_password.grid(row=5, column=1)

    # Confirm Password
    tk.Label(form_frame, text="Confirm Password:", font=("Arial", 12), bg="#f5f5f5").grid(row=6, column=0, pady=8, sticky="e")
    entry_confirm_password = tk.Entry(form_frame, width=30, show="*")
    entry_confirm_password.grid(row=6, column=1)

    # Show Password Checkbox
    show_pw_checkbox = tk.Checkbutton(form_frame, text="Show Password", variable=show_password,
                                      command=toggle_password, bg="#f5f5f5")
    show_pw_checkbox.grid(row=7, column=1, sticky="w", pady=5)

    # Register Button
    tk.Button(root, text="Register", command=register_user,
              bg="#007ACC", fg="white", font=("Arial", 13), width=20).pack(pady=20)
    tk.Button(root, text="Already have an account? Sign In", command=go_to_signin,
              bg="#f5f5f5", fg="#007ACC", font=("Arial", 11, "underline"), bd=0).pack()
    root.mainloop()

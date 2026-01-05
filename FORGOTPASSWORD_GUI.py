import tkinter as tk
from tkinter import messagebox
import entry_sql as sq
import sql_pass_modify as sq1
import random
import pywhatkit
import PSWCHECK as pw

def launch_forgot_password():
    # Global state
    current_user = {"email": "", "otp": 0, "mobile": ""}

    # GUI Root Window
    global root 
    root = tk.Tk()
    root.title("Account Recovery")
    root.geometry("500x500")
    root.configure(bg="#f0f0f0")

    # ---------- STEP 1: GET MOBILE FROM EMAIL & SEND OTP ----------

    def send_otp():
        email = entry_email.get()
        try:        
            mobile = sq1.sql_user_mob(email)
            mobile=str(mobile)
                
            if len(str(mobile)) == 10 and mobile.isdigit():
                current_user["email"] = email
                current_user["mobile"] = mobile

                email_frame.pack_forget()
                otp_frame.pack(pady=20)
            else:
                messagebox.showerror("Error", "Invalid or missing mobile number in DB.")
        except:
            messagebox.showerror("Error", "User ID not found.")

    # ---------- STEP 2: VERIFY OTP ----------

    def verify_otp():
        entered = entry_otp.get()
        if entered == str(current_user["mobile"]):
            messagebox.showinfo("Success", "Mobile number verified. You may reset your password.")
            otp_frame.pack_forget()
            reset_frame.pack(pady=20)
        else:
            messagebox.showerror("Incorrect mobile", "The mobile no. you entered is incorrect.")

    # ---------- STEP 3: RESET PASSWORD ----------

    def reset_password():
        new_pass = entry_new_pass.get()
        confirm_pass = entry_confirm_pass.get()

        if not pw.CheckPassword(new_pass):
            messagebox.showwarning("Weak Password", "Password doesn't meet security requirements.")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        try:
            sq1.sqlmodify(current_user["email"], new_pass)
            messagebox.showinfo("Success", "Password updated successfully!")
            root.destroy()            
        except:
            messagebox.showerror("Error", "Could not update password.")

    # ---------------- GUI LAYOUT ----------------

    # Email Frame
    email_frame = tk.Frame(root, bg="#f0f0f0")
    email_frame.pack(pady=40)

    tk.Label(email_frame, text="Enter User ID (Email):", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
    entry_email = tk.Entry(email_frame, width=30)
    entry_email.grid(row=0, column=1, padx=10)

    tk.Button(email_frame, text="Next", command=send_otp, bg="#007ACC", fg="white", font=("Arial", 12)).grid(row=1, columnspan=2, pady=15)

    # OTP Frame
    otp_frame = tk.Frame(root, bg="#f0f0f0")

    tk.Label(otp_frame, text="Enter Registered Mobile Number:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
    entry_otp = tk.Entry(otp_frame, width=15)
    entry_otp.grid(row=0, column=1, padx=10)

    tk.Button(otp_frame, text="Verify Mobile No", command=verify_otp, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=1, columnspan=2, pady=10)

    # Password Reset Frame
    reset_frame = tk.Frame(root, bg="#f0f0f0")

    tk.Label(reset_frame, text="New Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10)
    entry_new_pass = tk.Entry(reset_frame, width=25, show="*")
    entry_new_pass.grid(row=0, column=1, padx=10)

    tk.Label(reset_frame, text="Confirm Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10)
    entry_confirm_pass = tk.Entry(reset_frame, width=25, show="*")
    entry_confirm_pass.grid(row=1, column=1, padx=10)

    tk.Button(reset_frame, text="Reset Password", command=reset_password,
              bg="#E91E63", fg="white", font=("Arial", 12)).grid(row=2, columnspan=2, pady=15)

    root.mainloop()

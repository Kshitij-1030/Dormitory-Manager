from tkinter import *
from tkinter import messagebox
import re

class UserWindow:
    def __init__(self, title):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry('925x500+300+200')

    def destroy(self):
        self.root.destroy()

    def toggle_password_visibility(self):
        if self.show_password.get():
            self.password_entry.config(show='')
            if hasattr(self, 'confirm_password_entry'):
                self.confirm_password_entry.config(show='')
        else:
            self.password_entry.config(show='*')
            if hasattr(self, 'confirm_password_entry'):
                self.confirm_password_entry.config(show='*')

    def check_password_length(self, password):
        return len(password) >= 8

    def check_special_character(self, password):
        return bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    def check_number_used(self, password):
        return any(char.isdigit() for char in password)

    def validate_password(self, password, confirm_password):
        if not self.check_password_length(password):
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return False
        elif not self.check_special_character(password):
            messagebox.showerror("Error", "Password must contain at least one special character.")
            return False
        elif not self.check_number_used(password):
            messagebox.showerror("Error", "Password must contain at least one number.")
            return False
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return False
        return True
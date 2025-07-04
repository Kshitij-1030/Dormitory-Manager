from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from user_window import UserWindow
from users_database import is_username_exists
import sqlite3
import ssl
import smtplib
from email.message import EmailMessage
import random
import string

def generate_otp():
    otp = "".join(random.choices(string.digits, k=4))
    return otp

class SignUpWindow(UserWindow):
    def __init__(self):
        super().__init__('Sign Up')
        self.root.configure(bg="#3E3E42")

        self.raw_image = Image.open("IMAGES/MySchool.png")
        self.raw_image = self.raw_image.resize((400, 250))
        self.image = ImageTk.PhotoImage(self.raw_image, master=self.root)

        self.image_label = Label(self.root, image=self.image, bg="#3E3E42")
        self.image_label.place(x=50, y=100)

        self.frame = Frame(self.root,
                            width=350,
                            height=400,
                            bg="#3E3E42")
        self.frame.place(x=450, y=40)

        self.heading = Label(self.frame,
                            text='Sign Up',
                            fg='#00965C',
                            bg='#3E3E42',
                            font=('Helvetica', 26, 'bold'))
        self.heading.place(x=105, y=5)

        self.email_label = Label(self.frame,
                                text='Email',
                                fg='#00965C',
                                bg='#3E3E42',
                                font=('Helvetica', 15))
        self.email_label.place(x=50, y=80)

        self.email_entry = Entry(self.frame,
                                width=15,
                                fg='black',
                                border=0,
                                bg='white',
                                font=('Helvetica', 13))
        self.email_entry.place(x=170, y=80)

        self.line1 = Frame(self.frame,
                            width=295,
                            height=2,
                            bg='black')
        self.line1.place(x=25, y=110)

        self.username_label = Label(self.frame,
                                    text='Username',
                                    fg='#00965C',
                                    bg='#3E3E42',
                                    font=('Helvetica', 15))
        self.username_label.place(x=40, y=136)

        self.username_entry = Entry(self.frame,
                                    width=15,
                                    fg='black',
                                    border=0,
                                    bg='white',
                                    font=('Helvetica', 13))
        self.username_entry.place(x=170, y=140)

        self.line2 = Frame(self.frame,
                            width=295,
                            height=2,
                            bg='black')
        self.line2.place(x=25, y=170)

        self.password_label = Label(self.frame,
                                    text='Password',
                                    fg='#00965C',
                                    bg='#3E3E42',
                                    font=('Helvetica', 15))
        self.password_label.place(x=40, y=196)

        self.password_entry = Entry(self.frame,
                                    width=15,
                                    fg='black',
                                    border=0,
                                    bg='white',
                                    font=('Helvetica', 13),
                                    show='*')
        self.password_entry.place(x=170, y=200)

        self.line3 = Frame(self.frame,
                            width=295,
                            height=2,
                            bg='black')
        self.line3.place(x=25, y=230)

        self.confirm_password_label = Label(self.frame,
                                            text='Confirm \nPassword',
                                            fg='#00965C',
                                            bg='#3E3E42',
                                            font=('Helvetica', 14))
        self.confirm_password_label.place(x=42, y=236)

        self.confirm_password_entry = Entry(self.frame,
                                            width=15,
                                            fg='black',
                                            border=0,
                                            bg='white',
                                            font=('Helvetica', 13),
                                            show='*')
        self.confirm_password_entry.place(x=170, y=260)

        self.line4 = Frame(self.frame,
                            width=295,
                            height=2,
                            bg='black')
        self.line4.place(x=25, y=289)

        self.show_password = BooleanVar()
        self.show_password.set(False)

        self.show_password_checkbox = Checkbutton(self.frame,
                                                text='Show Password',
                                                variable=self.show_password,
                                                command=self.toggle_password_visibility,
                                                fg='#00965C',
                                                bg='#3E3E42',
                                                activebackground='#3E3E42',
                                                font=('Helvetica', 12, 'bold'))
        self.show_password_checkbox.place(x=160, y=300)

        self.sign_up_button = Button(self.frame,
                                    width=15,
                                    text='Sign up',
                                    fg='#00965C',
                                    bg='#3E3E42',
                                    activebackground='#3E3E42',
                                    font=('Helvetica', 14, 'bold'),
                                    command=self.sign_up)
        self.sign_up_button.place(x=80, y=330)

        self.sign_in_button = Button(self.frame,
                                    width=13,
                                    text='Return to Sign in',
                                    border=0,
                                    bg='#3E3E42',
                                    cursor='hand2',
                                    fg='#00965C', 
                                    font=('Helvetica', 12, 'underline'), 
                                    activebackground='#3E3E42', 
                                    command=self.open_sign_in_window)
        self.sign_in_button.place(x=115, y=370)

    def sign_up(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.confirm_password = self.confirm_password_entry.get()
        self.email = self.email_entry.get()

        if not self.username and not self.password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        elif not self.username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return
        elif not self.password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        elif not self.validate_password(self.password, self.confirm_password):
            return

        if not "@" in self.email:
            messagebox.showerror("Error", "Invalid email address. Please enter a valid email.")
            return

        if is_username_exists(self.username):
            messagebox.showerror("Error", "Username already exists. Choose a different username.")
            return

        try:
            otp = generate_otp()

            email_sender = "dormitorymanager69420@gmail.com"
            email_password = "wmcu itmv mnjt eaub"
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = self.email  
            em['Subject'] = "OTP"
            em.set_content("Your OTP is " + otp)

            context = ssl.create_default_context()

            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls(context=context)
                smtp.login(email_sender, email_password)
                smtp.send_message(em)

            from verify_email_window import VerifyEmailWindow
            verify_email_window = VerifyEmailWindow(self,
                                                    self.username,
                                                    self.email,
                                                    otp,
                                                    self.raw_image)
            self.root.withdraw()
            verify_email_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
            verify_email_window.mainloop()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "An error occurred. Please try again.")

    def open_sign_in_window(self):
        self.root.destroy()
        from sign_in_window import SignInWindow
        self.sign_in_window = SignInWindow()
        self.sign_in_window.run()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    sign_up_window = SignUpWindow()
    sign_up_window.run()

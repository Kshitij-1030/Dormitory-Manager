from tkinter import *
from tkinter import messagebox
from sign_up_window import SignUpWindow
from sign_in_window import SignInWindow
from users_database import insert_user 

class VerifyEmailWindow(Toplevel):
    def __init__(self, sign_up_window, username, gmail, otp, image):
        super().__init__()
        self.title('Verification')
        self.geometry('260x180')
        self.configure(bg="#3E3E42")

        label1 = Label(self,
                        text='Please check your email for a \nOne Time Password (OTP)',
                        fg='#00965C',
                        bg='#3E3E42',
                        font=('Helvetica', 14))
        label1.grid(row=0, column=0, columnspan=2, pady=10)

        label2 = Label(self,
                        text='OTP:',
                        fg='#00965C',
                        bg='#3E3E42',
                        font=('Helvetica', 12))
        label2.grid(row=1, column=0, pady=5)

        self.otp_entry = Entry(self, width=15, font=('Helvetica', 12))
        self.otp_entry.grid(row=1, column=1, pady=5)

        verify_button = Button(self,
                                text='Verify',
                                fg='#00965C',
                                bg='#3E3E42',
                                activebackground='#3E3E42',
                                font=('Helvetica', 12, 'bold'),
                                command=lambda: self.verify_otp(otp, username, gmail, sign_up_window))
        verify_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.username = username
        self.gmail = gmail
        self.image = image 
        self.sign_in_window = None

    def verify_otp(self, expected_otp, username, gmail, sign_up_window):
        entered_otp = self.otp_entry.get()

        if entered_otp == expected_otp:
            insert_user(username, sign_up_window.password)
            messagebox.showinfo("Success",
                                "Email address verified successfully!")
            self.destroy()
            self.open_sign_in_window()
        else:
            messagebox.showerror("Error",
                                "Invalid OTP. Please try again.")
            sign_up_window.root.deiconify()
            self.destroy()

    def open_sign_in_window(self):
        if self.sign_in_window is None or not self.sign_in_window.winfo_exists():
            self.sign_in_window = SignInWindow(image=self.image)
            self.sign_in_window.run()

if __name__ == "__main__":
    username = "example_username" 
    sign_up_window = SignUpWindow()
    verify_email_window = VerifyEmailWindow(sign_up_window, username, "example@gmail.com", "1234")
    verify_email_window.mainloop()

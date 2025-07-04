from tkinter import *
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from user_window import UserWindow
from users_database import check_user

class SignInWindow(UserWindow):
    def __init__(self, image=None):
        super().__init__('Sign In')
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
                            text='Sign In',
                            fg='#00965C',
                            bg='#3E3E42',
                            font=('Helvetica', 26, 'bold'))
        self.heading.place(x=105, y=25)

        self.username_label = Label(self.frame,
                                    text='Username',
                                    fg='#00965C',
                                    bg='#3E3E42',
                                    font=('Helvetica', 15))
        self.username_label.place(x=40, y=116)

        self.username_entry = Entry(self.frame,
                                    width=15,
                                    fg='black',
                                    border=0,
                                    bg='white',
                                    highlightbackground='#3E3E42',
                                    font=('Helvetica', 13))
        self.username_entry.place(x=170, y=120)

        self.line1 = Frame(self.frame,
                            width=295,
                            height=2,
                            bg='black')
        self.line1.place(x=25, y=150)

        self.password_label = Label(self.frame,
                                    text='Password',
                                    fg='#00965C',
                                    bg='#3E3E42',
                                    font=('Helvetica', 15))
        self.password_label.place(x=40, y=186)

        self.password_entry = Entry(self.frame,
                                    width=15,
                                    fg='black',
                                    border=0,
                                    bg='white',
                                    font=('Helvetica', 13),
                                    show='*')
        self.password_entry.place(x=170, y=190)

        self.line2 = Frame(self.frame,
                            width=295,
                            height=2,
                            bg='black')
        self.line2.place(x=25, y=220)

        self.show_password = BooleanVar()
        self.show_password.set(False)

        self.show_password_checkbox = Checkbutton(self.frame, text='Show Password',
                                                variable=self.show_password,
                                                command=self.toggle_password_visibility,
                                                fg='#00965C',
                                                bg='#3E3E42',
                                                activebackground='#3E3E42', 
                                                font=('Helvetica', 12, 'bold'))
        self.show_password_checkbox.place(x=160, y=230)

        self.sign_in_button = Button(self.frame,
                                    width=15,
                                    text='Sign in',
                                    fg='#00965C',
                                    bg='#3E3E42',
                                    activebackground='#3E3E42',  
                                    font=('Helvetica', 14, 'bold'),
                                    command=self.sign_in)
        self.sign_in_button.place(x=80, y=260)

        self.label = Label(self.frame,
                            text="Don't have an account?",
                            fg='#00965C',
                            bg='#3E3E42',
                            font=('Helvetica', 12))
        self.label.place(x=60, y=310)

        self.sign_up = Button(self.frame,
                            width=6,
                            text='Sign up',
                            border=0,
                            bg='#3E3E42',
                            cursor='hand2',
                            fg='#00965C', 
                            font=('Helvetica', 12, 'underline'), 
                            activebackground='#3E3E42', 
                            command=self.open_sign_up_window)
        self.sign_up.place(x=225, y=307)

    def sign_in(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        # Check if the username and password are provided
        if not self.username or not self.password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Disable the sign-in button to prevent multiple clicks
        self.sign_in_button.config(state=DISABLED)

        # Check if the user exists in the database
        user = check_user(self.username, self.password)

        if user:
            self.root.withdraw()

            loading_window = Toplevel(self.root)
            loading_window.title("LOADING...")
            loading_window.geometry("300x150")
            loading_window.configure(bg="#3E3E42")

            # Add labels
            label1 = Label(loading_window, text="Dormitory Manager", font=('Helvetica', 20, 'bold'), bg='#3E3E42', fg='#00965C', activebackground='#3E3E42')
            label1.pack(pady=10)

            label2 = Label(loading_window, text="Loading Home Page...", font=('Helvetica', 14), bg='#3E3E42', fg='#00965C', activebackground='#3E3E42')
            label2.pack(pady=10)

            progress_bar = ttk.Progressbar(loading_window, mode='determinate')
            progress_bar.pack()
            progress_bar.start()

            loading_window.after(5900, lambda: self.process_sign_in(loading_window, progress_bar))
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            self.sign_in_button.config(state=NORMAL)

    def process_sign_in(self, loading_window, progress_bar):
        progress_bar.stop()
        user = check_user(self.username, self.password)

        if user:
            self.open_home_window()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

        try:
            if loading_window.winfo_exists():
                loading_window.after(6000, lambda: self.destroy_loading_window(loading_window))
        except TclError:
            pass 


    def destroy_loading_window(self, loading_window):
        if loading_window.winfo_exists():
            loading_window.destroy()

    def open_home_window(self):
        try:
            if self.root.winfo_exists(): 
                self.root.destroy()
        except TclError:
            pass

        from home_window import HomeWindow
        self.home_window = HomeWindow(username=self.username)
        self.home_window.run()

    def open_sign_up_window(self):
        self.destroy()
        from sign_up_window import SignUpWindow
        self.sign_up_window = SignUpWindow()
        self.sign_up_window.run()

    def run(self):
        self.root.mainloop()
from tkinter import *
from PIL import Image, ImageTk
from sign_in_window import SignInWindow


class HomeWindow:
    def __init__(self, username):
        self.root = Tk()
        self.root.title('Home Page')
        self.root.geometry('1000x600')
        self.root.configure(bg="#3E3E42")
        self.username = username

        self.insert_students_window = None
        
        self.indus_raw_image = Image.open("IMAGES/MySchool.png")  
        self.indus_raw_image = self.indus_raw_image.resize((300, 200))  
        self.indus_image = ImageTk.PhotoImage(self.indus_raw_image, master=self.root)

        self.indus_image_label = Label(self.root,
                                        image=self.indus_image,
                                        bg="#3E3E42")
        self.indus_image_label.place(x=370, y=270)

        self.logOut_raw_image = Image.open("IMAGES/LogOut.png")
        self.logOut_raw_image = self.logOut_raw_image.resize((30,30))
        self.logOut_image = ImageTk.PhotoImage(self.logOut_raw_image, master=self.root)

        self.topRight_button = Button(self.root,
                                    image=self.logOut_image,
                                    command=self.toggle_log_out_button,
                                    bg="#3E3E42",
                                    activebackground='#3E3E42')
        self.topRight_button.place(x=964,y=0)

        self.logOut_button = Button(self.root, text="Log Out..",
                                    command=self.log_out,
                                    font=('Arial', 14),
                                    bg="#3E3E42",
                                    fg = '#66FF00',
                                    activebackground='#3E3E42')
        self.logOut_button.grid_remove()

        self.root.bind("<Button-1>", self.on_click)

        self.welcomeFrame = LabelFrame(self.root,
                            text = '',
                            bg="#3E3E42")
        self.welcomeFrame.pack()

        self.hiMessage = Label(self.welcomeFrame,
                        text=f'Hi, {username.upper()}',
                        bg = "#3E3E42",
                        fg = '#66FF00',
                        font=('Times', 30, 'bold', 'underline'))
        self.hiMessage.pack()

        self.welcomeMessage = Label(self.welcomeFrame,
                        text='Welcome to Dormitory Manager!',
                        font=('Times', 30, 'italic', 'underline'),
                        bg = "#3E3E42",
                        fg = '#66FF00')
        self.welcomeMessage.pack()

        self.RAM_Button = Button(self.root,
                        text='Room Assignment &\nManagement',
                        font=('Arial', 20, 'bold'),
                        bg = '#171717',
                        fg = '#55A860',
                        activebackground='#3E3E42',
                        command=self.open_room_management)
        self.RAM_Button.place(x=70, y=200)

        self.AT_Button = Button(self.root,
                        text='Attendance Tracking',
                        height=2,
                        font=('Arial', 20, 'bold'),
                        bg = '#171717',
                        fg = '#55A860',
                        activebackground='#3E3E42',
                        command=self.open_attendance_window)
        self.AT_Button.place(x=70, y=400)

        self.SPR_Button = Button(self.root,
                        text='Student Profiles &\nRecords',
                        width=16,
                        font=('Arial', 20, 'bold'),
                        bg = '#171717',
                        fg = '#55A860',
                        activebackground='#3E3E42',
                        command=self.open_student_profiles)
        self.SPR_Button.place(x=670, y=200)

        self.IS_Button = Button(self.root,
                        text='Insert Students',
                        height=2,
                        width=16,
                        font=('Arial', 20, 'bold'),
                        bg = '#171717',
                        fg = '#55A860',
                        activebackground='#3E3E42',
                        command=self.open_insert_students)
        self.IS_Button.place(x=670, y=400)

    def toggle_log_out_button(self):
        self.topRight_button.place_forget()
        self.logOut_button.place(x=910, y=0)

    def log_out(self):
        self.root.destroy()
        self.open_sign_in_window()
    
    def open_sign_in_window(self):
        self.sign_in_window = SignInWindow()
        self.sign_in_window.run()

    def open_room_management(self):
        from room_management import RoomManagement
        self.root.destroy()
        room_management_window = RoomManagement(home_window=self, username=self.username) 
        room_management_window.run()  

    def open_attendance_window(self):
        from student_attendance import StudentAttendance
        self.root.destroy()
        self.attendance_window = StudentAttendance(home_window=self, username=self.username)
        self.attendance_window.run()

    def open_student_profiles(self):
        from student_profiles import StudentProfile
        self.root.destroy()
        student_profile_window = StudentProfile(home_window=self, username=self.username)
        student_profile_window.run()

    def open_insert_students(self):
        from insert_students import InsertStudents
        self.root.destroy()
        self.insert_students_window = InsertStudents(home_window=self, username=self.username)
        self.insert_students_window.run()

    def on_click(self, event):
        if event.widget == self.root:
            self.logOut_button.place_forget()
            self.topRight_button.place(x=964,y=0)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HomeWindow()
    app.run()

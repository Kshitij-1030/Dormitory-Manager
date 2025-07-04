import pandas as pd
import os
from tkinter import *
from tkinter import filedialog, messagebox
from datetime import datetime
from tkcalendar import Calendar
from students_database import Database
from home_window import HomeWindow

class StudentAttendance:
    def __init__(self, home_window=None, username=None):
        self.root = Tk()
        self.root.title('Attendance')
        self.root.geometry('1000x600')
        self.root.configure(bg="#3E3E42")
        self.home_window = home_window
        self.username = username

        self.attendance_label = Label(self.root,
                                        text='ATTENDANCE',
                                        bg="#3E3E42",
                                        fg='#00b300',
                                        font=('Langdon', 30, 'bold', 'underline'))
        self.attendance_label.grid(row=0, column=0, pady=10)

        self.canvas = Canvas(self.root, bg='#3E3E42', highlightthickness=0, width=600, height=500)
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(row=1, column=1, sticky=N+S)
        self.canvas.grid(row=1, column=0, pady=10, padx=10, sticky=N+S+E+W)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = Frame(self.canvas, bg='#3E3E42', width=800, height=500)
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.db = Database()
        self.all_names = self.db.get_student_names()

        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.frame.bind('<Configure>', self.on_frame_configure)

        self.calendar_frame = Frame(self.root, bg="#3E3E42")
        self.calendar_frame.grid(row=1, column=2, sticky=E)

        spacer_frame = Frame(self.root, bg="#3E3E42", height=10)
        spacer_frame.grid(row=2, column=0, pady=5)

        self.search_frame = Frame(self.root, bg="#3E3E42")
        self.search_frame.grid(row=0, column=2, pady=(50, 0), padx=(10, 51), sticky=E)

        self.calendar_container = Frame(self.calendar_frame, bg="#3E3E42")
        self.calendar_container.grid(row=1, column=0, pady=(0, 10), sticky=W)

        self.calendar_label = Label(self.calendar_container,
                                    text="Select Date:",
                                    bg="#3E3E42",
                                    fg='#00b300',
                                    font=('Arial', 12, 'bold'))
        self.calendar_label.pack(side=TOP)

        initial_date = datetime(2023, 6, 12)
        self.cal = Calendar(self.calendar_container,
                            selectmode="day",
                            background='#3E3E42',
                            foreground='#00b300',
                            headersbackground='#3E3E42',
                            normalbackground='#3E3E42',
                            weekendbackground='#3E3E42',
                            dayforeground='#00b300',
                            normalforeground='#00b300',
                            weekendforeground='#00b300',
                            year=initial_date.year,
                            month=initial_date.month,
                            day=initial_date.day)
        self.cal.pack(side=TOP, pady=5)
        self.cal.bind("<<CalendarSelected>>", self.on_date_select)

        self.search_entry = Entry(self.search_frame, font=('Arial', 12))
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky=W)
        self.create_canvases(self.all_names)

        search_button = Button(self.search_frame, text="Search", bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.search_student)
        search_button.grid(row=0, column=1, padx=(0, 10), sticky=W)

        self.buttons_frame = Frame(self.calendar_frame, bg="#3E3E42")
        self.buttons_frame.grid(row=2, column=0, pady=(0, 10), padx=30, sticky=W)

        self.save_button = Button(self.buttons_frame, text="Save", bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.save_attendance)
        self.save_button.pack(pady=(0, 5), padx=10, anchor="center")

        self.clear_all_button = Button(self.buttons_frame, text="Clear All", bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.clear_all_attendance)
        self.clear_all_button.pack(pady=(0, 5), padx=10, anchor="center")

        self.download_attendance_button = Button(self.buttons_frame, text="Download Attendance", bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.download_attendance)
        self.download_attendance_button.pack(pady=(0, 5), padx=10, anchor="center")

        self.exit_button = Button(self.buttons_frame, text='Exit', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.exit_command)
        self.exit_button.pack(pady=(0, 5), padx=10, anchor="center")

        self.current_date = None
        self.attendance_data = {}   

        self.root.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def create_canvases(self, names):
        self.clear_canvases()
        names.sort()
        self.frame.grid_columnconfigure(0, weight=1)
        self.checkbutton_vars = {}
    
        search_query = self.search_entry.get().lower() 
        row_index = 0 
        for name in names:
            if search_query in name.lower():
                student_frame = Frame(self.frame, bg='#3E3E42', bd=2, relief=SOLID)
                student_frame.grid(row=row_index, column=0, pady=5, padx=(20, 10), sticky="ew") 
                row_index += 1 

                name_label = Label(student_frame,
                                    text=name,
                                    bg='#1C1C1E',
                                    fg='#00b300',
                                    font=('Langdon', 20, 'bold'))
                name_label.grid(row=0, column=0, pady=2, padx=2, sticky="w")

                checkbuttons_frame = Frame(student_frame, bg='#3E3E42')
                checkbuttons_frame.grid(row=0, column=1, pady=2, padx=10, sticky="e")

                var_present = IntVar()
                present_checkbox = Checkbutton(checkbuttons_frame, text="Present", bg="#3E3E42", fg="#00b300",
                                            selectcolor="#3E3E42", activebackground="#3E3E42", font=('Arial', 12, 'bold'), variable=var_present,
                                            command=lambda var=var_present, name=name: self.on_present_select(var, name))
                present_checkbox.pack(side=RIGHT, padx=5)
                self.checkbutton_vars[(name, "present")] = var_present

                var_absent = IntVar()
                absent_checkbox = Checkbutton(checkbuttons_frame, text="Absent", bg="#3E3E42", fg="#00b300",
                                            selectcolor="#3E3E42", activebackground="#3E3E42", font=('Arial', 12, 'bold'), variable=var_absent,
                                            command=lambda var=var_absent, name=name: self.on_absent_select(var, name))
                absent_checkbox.pack(side=RIGHT, padx=5)
                self.checkbutton_vars[(name, "absent")] = var_absent

            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def search_student(self):
        search_query = self.search_entry.get().lower()
        filtered_names = [name for name in self.all_names if search_query in name.lower()]
        self.create_canvases(filtered_names)

    def clear_canvases(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def on_present_select(self, var, name):
        if var.get() == 1:
            self.checkbutton_vars[(name, "absent")].set(0)

    def on_absent_select(self, var, name):
        if var.get() == 1:
            self.checkbutton_vars[(name, "present")].set(0)

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.frame_id, width=event.width)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_date_select(self, event):
        selected_date = self.cal.get_date()
        self.current_date = selected_date 
        if selected_date in self.attendance_data:
            self.load_attendance(selected_date)
        else:
            self.clear_attendance()

    def save_attendance(self):
        if self.current_date is None:
            messagebox.showerror("Error", "Please select a date first.")
            return

        attendance = {}
        for (name, state), var in self.checkbutton_vars.items():
            attendance[name] = {
                "present": var.get() == 1,
                "absent": var.get() == 0
            }
        self.attendance_data[self.current_date] = attendance
        messagebox.showinfo("Success", "Attendance saved for {}".format(self.current_date))

    def load_attendance(self, selected_date):
        attendance = self.attendance_data[selected_date]
        for (name, state), var in self.checkbutton_vars.items():
            if name in attendance:
                var_present = attendance[name]["present"]
                var_absent = attendance[name]["absent"]
                if state == "present":
                    var.set(1 if var_present else 0)
                elif state == "absent":
                    var.set(1 if var_absent else 0)
            else:
                var.set(0)

    def clear_attendance(self):
        for var in self.checkbutton_vars.values():
            var.set(0)

    def clear_all_attendance(self):
        for var in self.checkbutton_vars.values():
            var.set(0)
        messagebox.showinfo("Success", "Attendance cleared")

    def download_attendance(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        selected_date = self.cal.get_date()
        if selected_date not in self.attendance_data:
            messagebox.showerror("Error", "Attendance data not available for selected date.")
            return
        attendance = self.attendance_data[selected_date]

        attendance_list = []
        for name, status in attendance.items():
            attendance_list.append([name, "Present" if status["present"] else "Absent"])

        df = pd.DataFrame(attendance_list, columns=["Student Name", "Attendance"])

        try:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Attendance saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save attendance: {e}")

    def exit_command(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        if self.home_window is not None:
            new_home_window = HomeWindow(username=self.username)
            new_home_window.run()

if __name__ == "__main__":
    app = StudentAttendance()
    app.run()

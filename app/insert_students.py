import tkinter as tk
import os
import datetime
from tkinter import *
from tkinter import filedialog, messagebox
from students_database import Database
from home_window import HomeWindow 

class InsertStudents:
    def __init__(self, home_window, username):
        self.root = Tk()
        self.root.title("Insert Students...")
        self.root.geometry('1300x790')
        self.root.configure(bg="#3E3E42")
        self.home_window = home_window
        self.username = username

        self.main_frame = Frame(self.root,
                                relief="solid",
                                borderwidth=30,
                                bg="#3E3E42")
        self.main_frame.pack(fill="both", expand=True)

        self.buttons_frame = Frame(self.main_frame, bg="#3E3E42")
        self.buttons_frame.place(relx=0.9, rely=0.9, anchor='se')

        self.create_title_label()
        self.create_student_details_frame()
        self.create_equipment_details_frame()
        self.create_parent_details_frame()
        self.create_guardian_details_frame()
        self.create_buttons_frame()

    def create_title_label(self):
        self.title_label = Label(self.main_frame,
                                text="Student Registration Form",
                                bg="#3E3E42",
                                fg="#00b300",
                                font=("Slab Serifs", 30, "bold"))
        self.title_label.place(x=400, y=0)

    def create_student_details_frame(self):
        self.student_details_frame = LabelFrame(self.main_frame,
                                                text="Student Details",
                                                bg="#3E3E42",
                                                fg="#00b300",
                                                width=300,
                                                height=200,
                                                font=("Slab Serifs", 18, "bold"))
        self.student_details_frame.place(x=40, y=60)

        self.student_labels_text = ["Student's Full Name:",
                                    "Student's Email:",
                                    "Student's ID Card Number:",
                                    "Student's Date of Birth:",
                                    "Student's Grade:",
                                    "Student's Food Preference:"]
        self.student_entries = {}

        for i, text in enumerate(self.student_labels_text):
            label = self.create_label(self.student_details_frame, text, i, columnspan=None)
            entry = self.create_entry(self.student_details_frame, i)
            self.student_entries[text] = entry

    def create_equipment_details_frame(self):
        self.equipment_details_frame = LabelFrame(self.main_frame,
                                                text="Electronic Equipment Details",
                                                bg="#3E3E42",
                                                fg="#00b300",
                                                width=300,
                                                height=200,
                                                font=("Slab Serifs", 18, "bold"))
        self.equipment_details_frame.place(x=40, y=320)

        self.equipment_labels_text = ["Phone Number:",
                                    "Phone Brand:",
                                    "Phone Color:",
                                    "Laptop Brand:",
                                    "Laptop Serial Number:",
                                    "Peripherals:",
                                    "Laptop Description:"]
        self.equipment_entries = {}

        for i, text in enumerate(self.equipment_labels_text):
            label = self.create_label(self.equipment_details_frame, text, i, columnspan=None)
            entry = self.create_entry(self.equipment_details_frame, i)
            self.equipment_entries[text] = entry

    def create_parent_details_frame(self):
        self.parent_details_frame = LabelFrame(self.main_frame,
                                                text="Parent Details",
                                                bg="#3E3E42",
                                                fg="#00b300",
                                                width=300,
                                                height=200,
                                                font=("Slab Serifs", 18, "bold"))
        self.parent_details_frame.place(x=480, y=60)

        self.parent_labels_text = [
            "Father's Full Name:",
            "Father's Phone Number:",
            "Father's Email:",
            "Mother's Full Name:",
            "Mother's Phone Number:",
            "Mother's Email:",
            "Parent's Address",
            "Line 1:",
            "Line 2:",
            "Line 3:"]
        self.parent_entries = {}

        for i, text in enumerate(self.parent_labels_text):
            if i == 6:
                label = self.create_label(self.parent_details_frame, text, i, columnspan=2)
            else:
                label = self.create_label(self.parent_details_frame, text, i, columnspan=None)
                if i != 6:
                    entry = self.create_entry(self.parent_details_frame, i)
                    self.parent_entries[text] = entry

    def create_guardian_details_frame(self):
        self.guardian_details_frame = LabelFrame(self.main_frame,
                                                text="Guardian Details",
                                                bg="#3E3E42",
                                                fg="#00b300",
                                                width=300,
                                                height=200,
                                                font=("Slab Serifs", 18, "bold"))
        self.guardian_details_frame.place(x=480, y=450)

        self.guardian_labels_text = [
            "Guardian's Full Name:",
            "Guardian's Phone Number:",
            "Guardian's Email:",
            "Guardian's Address",
            "Line 1:",
            "Line 2:",
            "Line 3:"]
        self.guardian_entries = {}

        for i, text in enumerate(self.guardian_labels_text):
            if i == 3:
                label = self.create_label(self.guardian_details_frame, text, i, columnspan=2)
            else:
                label = self.create_label(self.guardian_details_frame, text, i, columnspan=None)
                if i != 3:
                    entry = self.create_entry(self.guardian_details_frame, i)
                    self.guardian_entries[text] = entry

    def create_buttons_frame(self):
        self.clear_button = Button(self.buttons_frame,
                                    text="Clear",
                                    bg="#00b300",
                                    fg="#3E3E42",
                                    font=("Slab Serifs", 14, "bold"),
                                    command=self.clear_all_entries)
        self.clear_button.pack(pady=10, side=TOP)

        self.save_button = Button(self.buttons_frame,
                                    text="Save",
                                    bg="#00b300",
                                    fg="#3E3E42",
                                    font=("Slab Serifs", 14, "bold"),
                                    command=self.save_students)
        self.save_button.pack(pady=10, side=TOP)

        self.exit_button = Button(self.buttons_frame,
                                    text="Exit",
                                    bg="#00b300",
                                    fg="#3E3E42",
                                    font=("Slab Serifs", 14, "bold"),
                                    command=self.exit_command)
        self.exit_button.pack(pady=10, side=TOP)

    def validate_name(self, name):
        return all(char.isalpha() or char.isspace() for char in name)

    def validate_data(self):
        for text, entry in self.student_entries.items():
            print(f"{text}: {entry.get()}")
        for text, entry in self.equipment_entries.items():
            print(f"{text}: {entry.get()}")
        for text, entry in self.parent_entries.items():
            print(f"{text}: {entry.get()}")
        for text, entry in self.guardian_entries.items():
            print(f"{text}: {entry.get()}")

    def save_students(self):
        student_name = self.student_entries["Student's Full Name:"].get()
        if not student_name:
            messagebox.showerror("Error", "Student's Full Name cannot be empty.")
            return

        db = Database()
        if db.get_student_id_by_name(student_name):
            messagebox.showerror("Error", "Student's Full Name already exists in the database.")
            return

        student_email = self.student_entries["Student's Email:"].get()
        if not student_email:
            messagebox.showerror("Error", "Student's Email cannot be empty.")
            return
        if '@' not in student_email:
            messagebox.showerror("Error", "Invalid Email format.")
            return

        student_id_card = self.student_entries["Student's ID Card Number:"].get()
        if not student_id_card:
            messagebox.showerror("Error", "Student's ID Card Number cannot be empty.")
            return
        if db.check_id_card_number(student_id_card):
            messagebox.showerror("Error", "Student's ID Card Number already exists in the database.")
            return

        student_dob = self.student_entries["Student's Date of Birth:"].get()
        if not student_dob:
            messagebox.showerror("Error", "Student's Date of Birth cannot be empty.")
            return
        if not self.validate_date_format(student_dob):
            messagebox.showerror("Error", "Invalid Date of Birth format. Use 'DD/MM/YYYY'.")
            return

        student_grade = self.student_entries["Student's Grade:"].get()
        if not student_grade:
            messagebox.showerror("Error", "Student's Grade cannot be empty.")
            return
        if not student_grade.isdigit():
            messagebox.showerror("Error", "Student's Grade should only contain digits.")
            return

        student_food_preference = self.student_entries["Student's Food Preference:"].get()
        if not student_food_preference:
            messagebox.showerror("Error", "Student's Food Preference cannot be empty.")
            return
        if student_food_preference.lower() not in ['veg', 'non veg']:
            messagebox.showerror("Error", "Student's Food Preference should be either 'Veg' or 'Non Veg'.")
            return

        phone_number = self.equipment_entries["Phone Number:"].get()
        if not phone_number:
            messagebox.showerror("Error", "Phone Number cannot be empty.")
            return
        if not phone_number.startswith('+') or not phone_number[1:].isdigit():
            messagebox.showerror("Error", "Invalid Phone Number format.")
            return

        phone_brand = self.equipment_entries["Phone Brand:"].get()
        if not phone_brand:
            messagebox.showerror("Error", "Phone Brand cannot be empty.")
            return

        phone_color = self.equipment_entries["Phone Color:"].get()
        if not phone_color:
            messagebox.showerror("Error", "Phone Color cannot be empty.")
            return

        laptop_brand = self.equipment_entries["Laptop Brand:"].get()
        if not laptop_brand:
            messagebox.showerror("Error", "Laptop Brand cannot be empty.")
            return

        laptop_serial_number = self.equipment_entries["Laptop Serial Number:"].get()
        if not laptop_serial_number:
            messagebox.showerror("Error", "Laptop Serial Number cannot be empty.")
            return
        if db.check_laptop_serial_number(laptop_serial_number):
            messagebox.showerror("Error", "Laptop Serial Number already exists in the database.")
            return

        peripherals = self.equipment_entries["Peripherals:"].get()
        if not peripherals:
            messagebox.showerror("Error", "Peripherals cannot be empty.")
            return

        laptop_description = self.equipment_entries["Laptop Description:"].get()
        if not laptop_description:
            messagebox.showerror("Error", "Laptop Description cannot be empty.")
            
        father_name = self.parent_entries["Father's Full Name:"].get()
        if not father_name:
            messagebox.showerror("Error", "Father's Full Name cannot be empty.")
            return

        mother_name = self.parent_entries["Mother's Full Name:"].get()
        if not mother_name:
            messagebox.showerror("Error", "Mother's Full Name cannot be empty.")
            return

        father_phone = self.parent_entries["Father's Phone Number:"].get()
        if not father_phone:
            messagebox.showerror("Error", "Father's Phone Number cannot be empty.")
            return
        if not father_phone.startswith('+') or not father_phone[1:].isdigit():
            messagebox.showerror("Error", "Invalid Father's Phone Number format.")
            return

        mother_phone = self.parent_entries["Mother's Phone Number:"].get()
        if not mother_phone:
            messagebox.showerror("Error", "Mother's Phone Number cannot be empty.")
            return
        if not mother_phone.startswith('+') or not mother_phone[1:].isdigit():
            messagebox.showerror("Error", "Invalid Mother's Phone Number format.")
            return
        
        father_email = self.parent_entries["Father's Email:"].get()
        if not father_email:
            messagebox.showerror("Error", "Father's Email cannot be empty.")
            return
        if '@' not in father_email:
            messagebox.showerror("Error", "Invalid Email format for father.")
            return
        
        mother_email = self.parent_entries["Mother's Email:"].get()
        if not mother_email:
            messagebox.showerror("Error", "Mother's Email cannot be empty.")
            return
        if '@' not in mother_email:
            messagebox.showerror("Error", "Invalid Email format for mother.")
            return

        address_line1 = self.parent_entries["Line 1:"].get()
        if not address_line1:
            messagebox.showerror("Error", "Address Line 1 cannot be empty.")
            return

        guardian_name = self.guardian_entries["Guardian's Full Name:"].get()
        if not guardian_name:
            messagebox.showerror("Error", "Guardian's Full Name cannot be empty.")
            return

        guardian_phone = self.guardian_entries["Guardian's Phone Number:"].get()
        if not guardian_phone:
            messagebox.showerror("Error", "Guardian's Phone Number cannot be empty.")
            return
        if not guardian_phone.startswith('+') or not guardian_phone[1:].isdigit():
            messagebox.showerror("Error", "Invalid Guardian's Phone Number format.")
            return
        
        guardian_email = self.guardian_entries["Guardian's Email:"].get()
        if not guardian_email:
            messagebox.showerror("Error", "Guardian's Email cannot be empty.")
            return
        if '@' not in guardian_email:
            messagebox.showerror("Error", "Invalid Email format for guardian.")
            return

        guardian_address_line1 = self.guardian_entries["Line 1:"].get()
        if not guardian_address_line1:
            messagebox.showerror("Error", "Guardian's Address Line 1 cannot be empty.")
            return

        student_data = [entry.get() for text, entry in self.student_entries.items()]
        electronics_data = [entry.get() for text, entry in self.equipment_entries.items()]
        parent_data = [entry.get() for text, entry in self.parent_entries.items()]
        guardian_data = [entry.get() for text, entry in self.guardian_entries.items()]

        db.insert_student(student_data)
        db.insert_electronics(electronics_data)
        db.insert_parent(parent_data)
        db.insert_guardian(guardian_data)
        db.close()
        messagebox.showinfo("Success", "Saved successfully")
        self.clear_all_entries()

    def validate_date_format(self, date_string):
        try:
            datetime.datetime.strptime(date_string, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    def clear_all_entries(self):
        for entry in self.student_entries.values():
            entry.delete(0, END)
        for entry in self.equipment_entries.values():
            entry.delete(0, END)
        for entry in self.parent_entries.values():
            entry.delete(0, END)
        for entry in self.guardian_entries.values():
            entry.delete(0, END)

        print("All entries cleared.")

    def create_label(self, frame, text, row, columnspan=None):
        label = Label(frame,
                        text=text,
                        bg="#3E3E42",
                        fg="#00b300",
                        font=("Slab Serifs", 13, "bold"))

        if columnspan is not None:
            label.grid(column=0, row=row, columnspan=columnspan, pady=5)
        else:
            label.grid(column=0, row=row, padx=10, pady=5, sticky=W)

        return label

    def create_entry(self, frame, row, width=22):
        entry = Entry(frame, width=width)
        entry.grid(column=1, row=row, padx=10, pady=5, sticky=E)
        return entry
    
    def exit_command(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        new_home_window = HomeWindow(username=self.username)
        new_home_window.run()

if __name__ == "__main__":
    app = InsertStudents()
    app.run()

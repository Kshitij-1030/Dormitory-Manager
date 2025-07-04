from tkinter import *
from tkinter import messagebox, StringVar, filedialog
from students_database import Database
import pandas as pd
import os
import zipfile
import io
from home_window import HomeWindow 

class StudentProfile:
    def __init__(self, home_window, username):
        self.root = Tk()
        self.root.title('Student Profiles & Records')
        self.root.geometry('1000x600')
        self.root.configure(bg='#3E3E42')
        self.home_window = home_window
        self.username = username

        self.header_label = Label(self.root,
                                    text='Student Profiles & Records',
                                    bg='#3E3E42',
                                    fg='#00b300',
                                    font=('Langdon', 24, 'bold', 'underline'))
        self.header_label.grid(row=0, column=0, pady=10, padx=150)

        self.canvas = Canvas(self.root, bg='#3E3E42', highlightthickness=0, width=800, height=500)
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(row=1, column=1, sticky=N+S)
        self.canvas.grid(row=1, column=0, pady=10, padx=10, sticky=N+S+E+W)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = Frame(self.canvas, bg='#3E3E42', bd=3, relief=SOLID, width=800, height=500)
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.widget_frame = Frame(self.root, bg='#3E3E42')
        self.widget_frame.grid(row=1, column=2, pady=10, sticky=N+S+E)

        self.search_entry = Entry(self.widget_frame, font=('Langdon', 12), width=15)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)

        self.search_button = Button(self.widget_frame, text='Search', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.search_students)
        self.search_button.grid(row=1, column=0, padx=5, pady=5)

        self.edit_button = Button(self.widget_frame, text='Edit', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.edit_students)
        self.edit_button.grid(row=2, column=0, padx=5, pady=20)

        self.download_button = Button(self.widget_frame, text='Download Records', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.download_records)
        self.download_button.grid(row=3, column=0, padx=5, pady=20)

        self.download_button = Button(self.widget_frame, text='Download All \nRecords', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.download_all_records)
        self.download_button.grid(row=4, column=0, padx=5, pady=20)

        self.exit_button = Button(self.widget_frame, text='Exit', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.exit_command)
        self.exit_button.grid(row=5, column=0, padx=5, pady=20)

        self.db = Database()
        self.all_names = self.db.get_student_names()
        self.create_canvases(self.all_names)

        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.frame.bind('<Configure>', self.on_frame_configure)

        self.root.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_canvases(self, names):
        self.clear_canvases()
        names.sort()    
        row, col = 0, 0 
        for name in names:
            canvas = Canvas(self.frame, bg='#3E3E42')
            canvas.grid(row=row, column=col, pady=5, padx=10)

            name_label = Label(canvas,
                                text=name,
                                bg='#1C1C1E',
                                fg='#00b300',
                                font=('Langdon', 20, 'bold'))
            name_label.pack(pady=2)

            listbox = Listbox(canvas, bg='#1C1C1E', fg='#FFFFFF', font=('Langdon', 15), selectbackground='#3E3E42', width=22, height=4, justify='center')
            listbox.pack(pady=10)

            items = ['Student Details', 'Equipment Details', 'Parent Details', 'Guardian Details']
            for item in items:
                listbox.insert(END, item)

            col += 1
            if col == 3: 
                col = 0
                row += 1

    def clear_canvases(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.frame_id, width=event.width)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def search_students(self):
        search_query = self.search_entry.get().lower()
        filtered_names = [name for name in self.all_names if search_query in name.lower()]
        self.create_canvases(filtered_names)

    def edit_students(self):
        selected_item = self.get_selected_item()
        if selected_item:
            selected_student_name = self.get_selected_student_name()

            student_details = self.db.get_student_details(selected_student_name)
            details_labels_entries = self.get_labels_entries(selected_item, student_details)

            edit_window = Toplevel(self.root)
            edit_window.configure(bg='#3E3E42')
            edit_window.title(f'Edit {selected_item} for {selected_student_name}')

            for i, (label_text, entry_var, _) in enumerate(details_labels_entries):
                label = Label(edit_window, text=label_text, font=('Langdon', 12), bg='#3E3E42', fg='white')
                label.grid(row=i, column=0, padx=10, pady=5, sticky='e')

                entry = Entry(edit_window, textvariable=entry_var, font=('Langdon', 12),width=25)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')

            save_button = Button(edit_window, text='Save', command=lambda ssn=selected_student_name,
                                si=selected_item, dle=details_labels_entries, ew=edit_window: self.save_edited_data(ssn, si, dle, ew),
                                font=('Langdon', 12))
            save_button.grid(row=i+1, column=0, columnspan=2, pady=10)

            for i, entry_info in enumerate(details_labels_entries):
                _, entry_var, *rest = entry_info
                if rest:
                    entry_var.set(rest[0])

    def get_selected_student_name(self):
        selected_indices = self.get_selected_indices()
        if selected_indices:
            widget, index = selected_indices[0]
            name_label = widget.winfo_children()[0]
            return name_label.cget("text")
        return ""

    def get_labels_entries(self, selected_item, student_details):
        labels_entries = []

        if selected_item == 'Student Details':
            labels_entries = [
                ('Student\'s Full Name:', StringVar(), student_details.get('full_name', '')),
                ('Student\'s Email:', StringVar(), student_details.get('email', '')),
                ('Student\'s ID Card Number:', StringVar(), student_details.get('id_card_number', '')),
                ('Student\'s Date of Birth:', StringVar(), student_details.get('date_of_birth', '')),
                ('Student\'s Grade:', StringVar(), student_details.get('grade', '')),
                ('Student\'s Food Preference:', StringVar(), student_details.get('food_preference', '')),
            ]
        elif selected_item == 'Equipment Details':
            equipment_details = self.db.get_equipment_details(student_details['id'])
            labels_entries = [
                ('Phone Number:', StringVar(), equipment_details.get('phone_number', '')),
                ('Phone Brand:', StringVar(), equipment_details.get('phone_brand', '')),
                ('Phone Color:', StringVar(), equipment_details.get('phone_color', '')),
                ('Laptop Brand:', StringVar(), equipment_details.get('laptop_brand', '')),
                ('Laptop Serial Number:', StringVar(), equipment_details.get('serial_number', '')),
                ('Peripherals:', StringVar(), equipment_details.get('peripherals', '')),
                ('Laptop Description:', StringVar(), equipment_details.get('laptop_description', '')),
            ]
        elif selected_item == 'Parent Details':
            parent_details = self.db.get_parent_details(student_details['id'])
            labels_entries = [
                ('Father\'s Full Name:', StringVar(), parent_details.get('father_name', '')),
                ('Father\'s Phone Number:', StringVar(), parent_details.get('father_mobile', '')),
                ('Father\'s Email:', StringVar(), parent_details.get('father_email', '')),
                ('Mother\'s Full Name:', StringVar(), parent_details.get('mother_name', '')),
                ('Mother\'s Phone Number:', StringVar(), parent_details.get('mother_mobile', '')),
                ('Mother\'s Email:', StringVar(), parent_details.get('mother_email', '')),
                ('Parent\'s Address Line 1:', StringVar(), parent_details.get('address_line1', '')),
                ('Parent\'s Address Line 2:', StringVar(), parent_details.get('address_line2', '')),
                ('Parent\'s Address Line 3:', StringVar(), parent_details.get('address_line3', '')),
            ]
        elif selected_item == 'Guardian Details':
            guardian_details = self.db.get_guardian_details(student_details['id'])
            labels_entries = [
                ('Guardian\'s Full Name:', StringVar(), guardian_details.get('guardian_name', '')),
                ('Guardian\'s Phone Number:', StringVar(), guardian_details.get('guardian_mobile', '')),
                ('Guardian\'s Email:', StringVar(), guardian_details.get('guardian_email', '')),
                ('Guardian\'s Address Line 1:', StringVar(), guardian_details.get('address_line1', '')),
                ('Guardian\'s Address Line 2:', StringVar(), guardian_details.get('address_line2', '')),
                ('Guardian\'s Address Line 3:', StringVar(), guardian_details.get('address_line3', '')),
            ]

        return labels_entries

    def save_edited_data(self, student_name, selected_item, details_labels_entries, edit_window):
        edited_data = {label_text[:-1]: entry_var.get() for label_text, entry_var, _ in details_labels_entries}
        self.db.update_student_details(student_name, selected_item, edited_data)
        self.create_canvases(self.db.get_student_names())  
        edit_window.destroy()  

    def get_selected_indices(self):
        selected_indices = []
        for widget in self.frame.winfo_children():
            if isinstance(widget, Canvas):
                listbox_widget = widget.winfo_children()[1]
                selected_index = listbox_widget.curselection()
                if selected_index:
                    selected_indices.append((widget, selected_index[0]))
        return selected_indices

    def get_selected_item(self):
        selected_indices = self.get_selected_indices()
        if selected_indices:
            widget, index = selected_indices[0]  
            listbox_widget = widget.winfo_children()[1]
            return listbox_widget.get(index)
        return None

    def download_records(self):
        selected_item = self.get_selected_item()
        if selected_item:
            selected_student_name = self.get_selected_student_name()

            student_details = self.db.get_student_details(selected_student_name)
            equipment_details = self.db.get_equipment_details(student_details['id'])
            parent_details = self.db.get_parent_details(student_details['id'])
            guardian_details = self.db.get_guardian_details(student_details['id'])

            student_details.pop('id', None)
            equipment_details.pop('id', None)
            parent_details.pop('id', None)
            guardian_details.pop('id', None)

            student_df = pd.DataFrame(student_details.items(), columns=['Details', 'Values'])
            equipment_df = pd.DataFrame(equipment_details.items(), columns=['Details', 'Values'])
            parent_df = pd.DataFrame(parent_details.items(), columns=['Details', 'Values'])
            guardian_df = pd.DataFrame(guardian_details.items(), columns=['Details', 'Values'])

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

            if file_path:
                with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                    student_df.to_excel(writer, sheet_name='Student_Details', index=False)
                    equipment_df.to_excel(writer, sheet_name='Equipment_Details', index=False)
                    parent_df.to_excel(writer, sheet_name='Parent_Details', index=False)
                    guardian_df.to_excel(writer, sheet_name='Guardian_Details', index=False)

                messagebox.showinfo("Download Complete", f"Records for {selected_student_name} downloaded successfully!")

    def download_all_records(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            zip_file_path = os.path.join(folder_path, "all_student_records.zip")

            with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                for student_name in self.all_names:
                    student_details = self.db.get_student_details(student_name)
                    equipment_details = self.db.get_equipment_details(student_details['id'])
                    parent_details = self.db.get_parent_details(student_details['id'])
                    guardian_details = self.db.get_guardian_details(student_details['id'])

                    student_details.pop('id', None)
                    equipment_details.pop('id', None)
                    parent_details.pop('id', None)
                    guardian_details.pop('id', None)

                    student_df = pd.DataFrame(student_details.items(), columns=['Details', 'Values'])
                    equipment_df = pd.DataFrame(equipment_details.items(), columns=['Details', 'Values'])
                    parent_df = pd.DataFrame(parent_details.items(), columns=['Details', 'Values'])
                    guardian_df = pd.DataFrame(guardian_details.items(), columns=['Details', 'Values'])

                    student_buffer = io.BytesIO()
                    with pd.ExcelWriter(student_buffer, engine='xlsxwriter') as writer:
                        student_df.to_excel(writer, sheet_name='Student_Details', index=False)
                        equipment_df.to_excel(writer, sheet_name='Equipment_Details', index=False)
                        parent_df.to_excel(writer, sheet_name='Parent_Details', index=False)
                        guardian_df.to_excel(writer, sheet_name='Guardian_Details', index=False)

                    zipf.writestr(f'{student_name}_record.xlsx', student_buffer.getvalue())
            messagebox.showinfo("Download Complete", f"All records downloaded successfully and saved in {zip_file_path}")
    
    def exit_command(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        new_home_window = HomeWindow(username=self.username)
        new_home_window.run()

if __name__ == "__main__":
    app = StudentProfile()
    app.run()

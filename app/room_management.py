from tkinter import *
from tkinter import ttk, messagebox, filedialog
from students_database import Database
import pandas as pd
from home_window import HomeWindow 

class RoomManagement:
    def __init__(self, home_window, username):
        self.room_data = {}
        self.root = Tk()
        self.root.title('Room Assignment & Management')
        self.root.geometry('1000x600')
        self.root.configure(bg='#3E3E42')
        self.selected_room_number = None
        self.home_window = home_window
        self.username = username

        self.title_label = Label(self.root,
                                text='Room Assignment & Management',
                                bg='#3E3E42',
                                fg='#00b300',
                                font=('Langdon', 24, 'bold', 'underline'))
        self.title_label.place(relx=0.38, rely=0.05, anchor='center')

        # Create a Canvas and a Scrollbar
        self.canvas = Canvas(self.root, bg='#3E3E42', highlightthickness=0, width=800, height=500)
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.place(relx=0.77, rely=0.12, relheight=0.84, anchor=NE)
        self.canvas.place(relx=0.41, rely=0.54, anchor='center')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a Frame inside the Canvas to hold the rooms
        self.frame = Frame(self.canvas, bg='#3E3E42', bd=3, relief=SOLID, width=800, height=500)
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # Create rooms
        self.create_rooms()

        # Widget Frame
        self.widget_frame = Frame(self.root, bg='#3E3E42')
        self.widget_frame.place(relx=0.885, rely=0.1, anchor='n')

        self.search_entry = Entry(self.widget_frame, font=('Langdon', 12), width=15)
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)

        self.search_button = Button(self.widget_frame, text='Search', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.search_rooms)
        self.search_button.grid(row=1, column=0, padx=5, pady=20)

        self.add_room_button = Button(self.widget_frame, text='Add Room', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.add_room)
        self.add_room_button.grid(row=2, column=0, padx=5, pady=20)

        self.delete_room_button = Button(self.widget_frame, text='Delete Room', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.delete_room)
        self.delete_room_button.grid(row=3, column=0, padx=5, pady=20)

        self.edit_room_button = Button(self.widget_frame, text='Edit Room', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.edit_room)
        self.edit_room_button.grid(row=4, column=0, padx=5, pady=20)

        self.download_room_button = Button(self.widget_frame, text='Download Room Allotment', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.download_room)
        self.download_room_button.grid(row=5, column=0, padx=5, pady=20)

        self.exit_button = Button(self.widget_frame, text='Exit', bg="#00b300", fg="#3E3E42", font=('Langdon', 12, "bold"), command=self.exit_command)
        self.exit_button.grid(row=6, column=0, padx=5, pady=20)

        # Bind the canvas to the scrollbar
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.scrollbar.bind('<B1-Motion>', self.on_scroll)

    def create_rooms(self):
        num_rows = 3
        num_columns = 3
        for row in range(num_rows):
            for col in range(num_columns):
                room_number = row * num_columns + col + 1
                self.room_data[room_number] = ["", "", ""] 

                room_info_canvas = Canvas(self.frame, bg='#3E3E42', width=220, height=160)
                room_info_canvas.grid(row=row, column=col, padx=10, pady=10)

                room_number_label = Label(room_info_canvas, text=f'{room_number:03d}', bg='#1C1C1E', fg='#00b300', font=('Langdon', 24, 'bold'))
                room_number_label.place(relx=0.5, rely=0.2, anchor=CENTER)

                listbox = Listbox(room_info_canvas, bg='#1C1C1E', fg='#FFFFFF', font=('Langdon', 15), selectbackground='#3E3E42', width=20, height=3, justify='center')
                for _ in range(3):
                    listbox.insert(END, " ")  # Insert an empty item
                listbox.place(relx=0.5, rely=0.65, anchor=CENTER)

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_scroll(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def search_rooms(self):
        room_to_search = self.search_entry.get()

        if not room_to_search.strip():
            self.frame.destroy()
            self.frame = Frame(self.canvas, bg='#3E3E42', bd=3, relief=SOLID, width=800, height=500)
            self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
            self.create_rooms()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return

        if not room_to_search.isdigit():
            messagebox.showerror("Error", "Please enter a valid room number.")
            return

        room_to_search = int(room_to_search)

        if not (0 <= room_to_search <= 999):
            messagebox.showerror("Error", "Please enter a valid room number between 0 and 999.")
            return

        room_to_search_str = str(room_to_search)  
        room_to_search_str = room_to_search_str.lstrip('0')  

        if len(room_to_search_str) == 0:
            room_to_search_str = '0'  

        if int(room_to_search_str) not in self.room_data.keys():
            messagebox.showerror("Error", f"Room {room_to_search} does not exist.")
            return

        self.frame.destroy()
        self.frame = Frame(self.canvas, bg='#3E3E42', bd=3, relief=SOLID, width=800, height=500)
        self.frame_id = self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.create_single_room(int(room_to_search_str))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def create_single_room(self, room_number):
        num_rows = 1
        num_columns = 1
        for row in range(num_rows):
            for col in range(num_columns):
                room_info_canvas = Canvas(self.frame, bg='#3E3E42', width=220, height=160)
                room_info_canvas.grid(row=row, column=col, padx=10, pady=10)

                room_number_label = Label(room_info_canvas, text=f'{room_number:03d}', bg='#1C1C1E', fg='#00b300', font=('Langdon', 24, 'bold'))
                room_number_label.place(relx=0.5, rely=0.2, anchor=CENTER)

                listbox = Listbox(room_info_canvas, bg='#1C1C1E', fg='#FFFFFF', font=('Langdon', 15), selectbackground='#3E3E42', width=20, height=3, justify='center')
                for _ in range(3):
                    listbox.insert(END, " ")  
                listbox.place(relx=0.5, rely=0.65, anchor=CENTER)
    
    def add_room(self):
        current_rooms = len(self.frame.winfo_children())

        empty_spaces = [
            room.winfo_children()[0].cget("text") 
            for room in self.frame.winfo_children()
        ]

        for i in range(1, current_rooms + 2):
            room_number = f"{i:03d}"
            if room_number not in empty_spaces:
                break

        row = (i - 1) // 3
        col = (i - 1) % 3

        room_info_canvas = Canvas(self.frame, bg='#3E3E42', width=220, height=160)
        room_info_canvas.grid(row=row, column=col, padx=10, pady=10)

        room_number_label = Label(room_info_canvas, 
                                    text=room_number,
                                    bg='#1C1C1E',
                                    fg='#00b300',
                                    font=('Langdon', 24, 'bold'))
        room_number_label.place(relx=0.5, rely=0.2, anchor=CENTER)

        listbox = Listbox(room_info_canvas,
                            bg='#1C1C1E',
                            fg='#FFFFFF',
                            font=('Langdon', 15),
                            selectbackground='#3E3E42',
                            width=20,
                            height=3,
                            justify='center')
        for _ in range(3):
            listbox.insert(END, " ")
        listbox.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.root.after(100, self.update_scroll)

    def update_scroll(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        current_rooms = len(self.frame.winfo_children())
        normalized_position = (current_rooms - 1) / (current_rooms // 3)

        self.canvas.yview_moveto(normalized_position)

    def delete_room(self):
        selected_item = self.canvas.focus_get()
        if selected_item and isinstance(selected_item, Listbox):
            selected_index = selected_item.curselection()
            if selected_index:
                room_number = selected_item.get(selected_index[0])

                for room in self.frame.winfo_children():
                    for widget in room.winfo_children():
                        if isinstance(widget, Listbox) and widget == selected_item:
                            room.destroy()
                            break

                self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def edit_room(self):
        selected_item = self.canvas.focus_get()
        if selected_item and isinstance(selected_item, Listbox):
            selected_index = selected_item.curselection()
            if selected_index:
                room_number = int(selected_item.master.winfo_children()[0].cget("text"))  

                edit_window = Toplevel(self.root)
                edit_window.title(f"Editing Room Number {room_number}...")
                edit_window.configure(bg='#3E3E42')

                student_names = self.get_all_student_names_from_database()
                student_names.sort()

                labels = ["Enter the first student:",
                        "Enter the second student:",
                        "Enter the third student:"]
                dropdowns = []

                if len(self.room_data[room_number]) < 3:
                    self.room_data[room_number] += [''] * (3 - len(self.room_data[room_number]))

                for i, label_text in enumerate(labels):
                    label = Label(edit_window,
                                text=label_text,
                                font=('Langdon', 12),
                                bg='#3E3E42', fg='white')
                    label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
                    dropdown = ttk.Combobox(edit_window, values=student_names)
                    dropdown.grid(row=i, column=1, padx=10, pady=5, sticky='w')
                    dropdowns.append(dropdown)
                    dropdown.set(self.room_data[room_number][i] if i < len(self.room_data[room_number]) else '')

                save_button = Button(edit_window,
                                    text="Save",
                                    command=lambda: self.save_edited_room(edit_window, room_number, dropdowns))
                save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)
        else:
            messagebox.showinfo("Error", "No listbox selected for editing.")

    def save_edited_room(self, edit_window, room_number, dropdowns):
        selected_students = [dropdown.get() for dropdown in dropdowns]
        selected_students = list(filter(None, selected_students))

        if len(set(selected_students)) != len(selected_students):
            messagebox.showerror("Error", "Each student in a room must be unique.")
            return

        for other_room_number, students in self.room_data.items():
            if other_room_number != room_number:
                common_students = set(students) & set(selected_students)
                if common_students:
                    messagebox.showerror("Error",
                                        f"Student(s) {', '.join(common_students)} is/are already assigned to Room {other_room_number}.")
                    return

        self.room_data[room_number] = selected_students

        for room in self.frame.winfo_children():
            room_number_label = room.winfo_children()[0] 
            current_room_number = int(room_number_label.cget("text"))
            if current_room_number == room_number:
                listbox = room.winfo_children()[1] 
                listbox.delete(0, END) 
                for student in self.room_data[room_number]:
                    listbox.insert(END, student) 
                edit_window.destroy()
                break

    def get_all_student_names_from_database(self):
        with Database() as db:
            return db.get_student_names()

    def download_room(self):
        data = {
            'Room Number': [],
            'Student 1': [],
            'Student 2': [],
            'Student 3': []
        }

        for room_number, students in self.room_data.items():
            if any(students):
                data['Room Number'].append(room_number)
                data['Student 1'].append(students[0])
                data['Student 2'].append(students[1] if len(students) > 1 else "") 
                data['Student 3'].append(students[2] if len(students) > 2 else "")  

        room_df = pd.DataFrame(data)

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

        if file_path:
            room_df.to_excel(file_path, index=False)

            messagebox.showinfo("Success", "Room allotment data has been successfully exported to Excel.")


    def exit_command(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        new_home_window = HomeWindow(username=self.username)
        new_home_window.run()

if __name__ == "__main__":
    app = RoomManagement()
    app.run()
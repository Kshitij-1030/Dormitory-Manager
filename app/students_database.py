import sqlite3
import threading

class Database:
    lock = threading.Lock()

    def __enter__(self):
        self.conn = sqlite3.connect('students.db', isolation_level=None)
        self.cursor = self.conn.cursor()
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.create_tables()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def __init__(self):
        self.conn = sqlite3.connect('students.db', isolation_level=None)
        self.cursor = self.conn.cursor()
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                email TEXT,
                id_card_number TEXT,
                date_of_birth DATE,
                grade TEXT,
                food_preference TEXT
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS electronics (
                id INTEGER PRIMARY KEY,
                phone_number TEXT,
                phone_brand TEXT,
                phone_color TEXT,
                laptop_brand TEXT,
                serial_number TEXT,
                peripherals TEXT,
                laptop_description TEXT
            )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS parents (
            id INTEGER PRIMARY KEY,
            father_name TEXT,
            father_mobile TEXT,
            father_email TEXT,
            mother_name TEXT,
            mother_mobile TEXT,
            mother_email TEXT,
            address_line1 TEXT,
            address_line2 TEXT,
            address_line3 TEXT
        )
    ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS guardians (
                id INTEGER PRIMARY KEY,
                guardian_name TEXT,
                guardian_mobile TEXT,
                guardian_email TEXT,
                address_line1 TEXT,
                address_line2 TEXT,
                address_line3 TEXT
            )
        ''')

        self.conn.commit()

    def get_student_names(self):
        self.cursor.execute("SELECT full_name FROM students")
        return [row[0] for row in self.cursor.fetchall()]

    def insert_student(self, student_data):
        sql = '''
            INSERT INTO students (full_name, email, id_card_number, date_of_birth, grade, food_preference)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(sql, student_data)
        self.conn.commit()

    def insert_electronics(self, data):
        self.cursor.execute('''
            INSERT INTO electronics 
            (phone_number, phone_brand, phone_color, laptop_brand, serial_number, peripherals, laptop_description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()

    def insert_parent(self, data):
        self.cursor.execute('''
            INSERT INTO parents 
            (father_name, father_mobile, father_email, mother_name, mother_mobile, mother_email, address_line1, address_line2, address_line3)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()

    def insert_guardian(self, data):
        self.cursor.execute('''
            INSERT INTO guardians 
            (guardian_name, guardian_mobile, guardian_email, address_line1, address_line2, address_line3)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()
    
    def get_student_details(self, full_name):
        self.cursor.execute("SELECT * FROM students WHERE full_name=?", (full_name,))
        result = self.cursor.fetchone()
        if result:
            columns = [column[0] for column in self.cursor.description]
            return dict(zip(columns, result))
        else:
            return None

    def get_equipment_details(self, student_id):
        self.cursor.execute("SELECT * FROM electronics WHERE id=?", (student_id,))
        columns = [desc[0] for desc in self.cursor.description]
        equipment_details = self.cursor.fetchone()
        if equipment_details is None:
            return {}  
        else:
            return dict(zip(columns, equipment_details))

    def get_parent_details(self, student_id):
        self.cursor.execute("SELECT * FROM parents WHERE id=?", (student_id,))
        columns = [desc[0] for desc in self.cursor.description]
        parent_details = self.cursor.fetchone()
        if parent_details is None:
            return {}  
        else:
            return dict(zip(columns, parent_details))

    def get_guardian_details(self, student_id):
        self.cursor.execute("SELECT * FROM guardians WHERE id=?", (student_id,))
        columns = [desc[0] for desc in self.cursor.description]
        guardian_details = self.cursor.fetchone()
        if guardian_details is None:
            return {} 
        else:
            return dict(zip(columns, guardian_details))

    def update_student_details(self, student_name, selected_item, edited_data):
        if selected_item == 'Student Details':
            if not edited_data['Student\'s Full Name']:
                raise ValueError("Student's name cannot be empty")

            self.cursor.execute(
                '''
                UPDATE students
                SET full_name=?, email=?, id_card_number=?, date_of_birth=?, grade=?, food_preference=?
                WHERE full_name=?
                ''',
                (edited_data['Student\'s Full Name'], edited_data['Student\'s Email'],
                edited_data['Student\'s ID Card Number'], edited_data['Student\'s Date of Birth'],
                edited_data['Student\'s Grade'], edited_data['Student\'s Food Preference'], student_name)
            )
        elif selected_item == 'Equipment Details':
            if not edited_data['Phone Number']:
                raise ValueError("Phone number cannot be empty")

            student_id = self.get_student_id_by_name(student_name)
            self.cursor.execute(
                '''
                UPDATE electronics
                SET phone_number=?, phone_brand=?, phone_color=?, laptop_brand=?, serial_number=?, peripherals=?, laptop_description=?
                WHERE id=?
                ''',
                (edited_data['Phone Number'], edited_data['Phone Brand'], edited_data['Phone Color'],
                edited_data['Laptop Brand'], edited_data['Laptop Serial Number'], edited_data['Peripherals'],
                edited_data['Laptop Description'], student_id)
            )
        elif selected_item == 'Parent Details':
            if not edited_data['Father\'s Full Name']:
                raise ValueError("Father's name cannot be empty")

            student_id = self.get_student_id_by_name(student_name)
            self.cursor.execute(
                '''
                UPDATE parents
                SET father_name=?, father_mobile=?, father_email=?, mother_name=?, mother_mobile=?, mother_email=?,
                address_line1=?, address_line2=?, address_line3=?
                WHERE id=?
                ''',
                (edited_data['Father\'s Full Name'], edited_data['Father\'s Phone Number'],
                edited_data['Father\'s Email'], edited_data['Mother\'s Full Name'],
                edited_data['Mother\'s Phone Number'], edited_data['Mother\'s Email'],
                edited_data['Parent\'s Address Line 1'], edited_data['Parent\'s Address Line 2'],
                edited_data['Parent\'s Address Line 3'], student_id)
            )
        elif selected_item == 'Guardian Details':
            if not edited_data['Guardian\'s Full Name']:
                raise ValueError("Guardian's name cannot be empty")

            # Update guardian details
            student_id = self.get_student_id_by_name(student_name)
            self.cursor.execute(
                '''
                UPDATE guardians
                SET guardian_name=?, guardian_mobile=?, guardian_email=?,
                address_line1=?, address_line2=?, address_line3=?
                WHERE id=?
                ''',
                (edited_data['Guardian\'s Full Name'], edited_data['Guardian\'s Phone Number'],
                edited_data['Guardian\'s Email'], edited_data['Guardian\'s Address Line 1'],
                edited_data['Guardian\'s Address Line 2'], edited_data['Guardian\'s Address Line 3'],
                student_id)
            )

        self.conn.commit()

    def get_student_id_by_name(self, student_name):
        self.cursor.execute("SELECT id FROM students WHERE full_name=?", (student_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def check_id_card_number(self, id_card_number):
        self.cursor.execute("SELECT id_card_number FROM students WHERE id_card_number=?", (id_card_number,))
        result = self.cursor.fetchone()
        return result is not None
    
    def check_laptop_serial_number(self, serial_number):
        self.cursor.execute("SELECT serial_number FROM electronics WHERE serial_number=?", (serial_number,))
        result = self.cursor.fetchone()
        return result is not None

    def close(self):
        self.conn.close()
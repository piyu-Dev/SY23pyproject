import tkinter as tk

#from tkcalendar import DateEntry
from tkinter import messagebox, ttk, Menu
import sqlite3

# Database Initialization
def init_db():
    with sqlite3.connect('crimemanagement.db') as conn:
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS criminal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            address TEXT NOT NULL,
            crime TEXT NOT NULL
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS victim (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            address TEXT NOT NULL,
            report TEXT NOT NULL
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS court_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            criminal_id INTEGER NOT NULL,
            judge_name TEXT NOT NULL,
            verdict TEXT NOT NULL,
            FOREIGN KEY (criminal_id) REFERENCES criminal (id)
        )''')

DB_PATH = 'crimemanagement.db'
# Styling
FONT = ("Consolas", 12)
BUTTON_FONT = ("Consolas", 10, "bold")
BG_COLOR = "#858481"
ENTRY_BG = "#ffffff"  # Background color for entry widgets
ENTRY_FG = "#000000"  # Text color for entry widgets

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn, conn.cursor()

# Base Application
class CrimeManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crime Management System")
        self.geometry("600x440")
        self.configure(bg=BG_COLOR)

        # Initialize the database
        init_db()

        # Set up the UI
        self.setup_ui()

    def setup_ui(self):
        # Creating menu bar
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        # Manage menu
        manage_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Manage", menu=manage_menu)
        manage_menu.add_command(label="Victims", command=self.open_victim_window)
        manage_menu.add_command(label="Court Records", command=self.open_court_records_window)

        # Criminal Data Entry
        entry_frame = tk.Frame(self, bg=BG_COLOR)
        entry_frame.pack(padx=10, pady=10)

        tk.Label(entry_frame, text='Name', font=FONT, bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(entry_frame, font=FONT)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(entry_frame, text='Age', font=FONT, bg=BG_COLOR).grid(row=1, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(entry_frame, font=FONT)
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(entry_frame, text='Address', font=FONT, bg=BG_COLOR).grid(row=2, column=0, padx=10, pady=5)
        self.address_entry = tk.Entry(entry_frame, font=FONT)
        self.address_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(entry_frame, text='Crime', font=FONT, bg=BG_COLOR).grid(row=3, column=0, padx=10, pady=5)
        self.crime_entry = tk.Entry(entry_frame, font=FONT)
        self.crime_entry.grid(row=3, column=1, padx=10, pady=5)

        # Add Criminal Record Button
        tk.Button(entry_frame, text='Add Criminal Record', command=self.add_criminal_record, font=BUTTON_FONT, bg=BG_COLOR).grid(row=4, columnspan=2, pady=10)

        # Show Criminal Records Button
        tk.Button(entry_frame, text='Show Criminal Records', command=self.show_criminal_records, font=BUTTON_FONT, bg=BG_COLOR).grid(row=5, columnspan=2, pady=10)

    def add_criminal_record(self):
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        address = self.address_entry.get().strip()
        crime = self.crime_entry.get().strip()

        if not name or not age.isdigit() or not address or not crime:
            messagebox.showerror("Error", "Invalid input.")
            return

        conn, cursor = get_db_connection()
        try:
            cursor.execute('INSERT INTO criminal (name, age, address, crime) VALUES (?, ?, ?, ?)',
                           (name, int(age), address, crime))
            conn.commit()
            messagebox.showinfo("Success", "Criminal record added successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()
            self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.crime_entry.delete(0, tk.END)

    def show_criminal_records(self):
        ShowDetailsWindow(self, "criminal")

    def open_victim_window(self):
        VictimsManagement(self)

    def open_court_records_window(self):
        CourtRecordsManagement(self)

    def open_show_details_window(self):
        details_window = ShowDetailsWindow(self, "table_name")
        details_window.grab_set()


# Sub-Window for Showing Details
class ShowDetailsWindow(tk.Toplevel):
    def __init__(self, parent, table_name):
        super().__init__(parent)
        self.title(f"{table_name.capitalize()} Details")
        self.geometry("600x400")
        self.configure(bg=BG_COLOR)
        self.table_name = table_name
        self.setup_ui()

    def show_details(self, table_name):
        # Correctly create an instance of the ShowDetailsWindow
        ShowDetailsWindow(self, table_name)

    def setup_ui(self):
        self.tree = ttk.Treeview(self, columns=('1', '2', '3', '4', '5'), show="headings", height=15)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        if self.table_name == "criminal":
            self.tree.heading(1, text="ID")
            self.tree.heading(2, text="Name")
            self.tree.heading(3, text="Age")
            self.tree.heading(4, text="Address")
            self.tree.heading(5, text="Crime")
            self.fetch_data("SELECT id, name, age, address, crime FROM criminal")

        elif self.table_name == "victim":
            self.tree.heading(1, text="ID")
            self.tree.heading(2, text="Name")
            self.tree.heading(3, text="Age")
            self.tree.heading(4, text="Address")
            self.tree.heading(5, text="Report")
            self.fetch_data("SELECT id, name, age, address, report FROM victim")

        elif self.table_name == "court_record":
            self.tree.heading(1, text="ID")
            self.tree.heading(2, text="Criminal ID")
            self.tree.heading(3, text="Judge Name")
            #self.tree.heading(4, text="Hearing Date")
            self.tree.heading(4, text="Verdict")
            self.fetch_data("SELECT id, criminal_id, judge_name, verdict FROM court_record")

        # Adjusting column widths
        for col in ('1', '2', '3', '4'):
            self.tree.column(col, width=100, anchor='center')  # Adjust the width as needed

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.tree.configure(yscrollcommand=scrollbar.set)

    def fetch_data(self, query):
        conn, cursor = get_db_connection()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


class VictimsManagement(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Victim Management")
        self.geometry("600x400")
        self.configure(bg=BG_COLOR)

        tk.Label(self, text='Name', bg=BG_COLOR, font=FONT).grid(row=0, column=0, padx=10, pady=5, sticky='s')
        self.name_entry = tk.Entry(self, bg=ENTRY_BG, fg=ENTRY_FG, font=FONT)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text='Age', bg=BG_COLOR, font=FONT).grid(row=1, column=0, padx=10, pady=5, sticky='s')
        self.age_entry = tk.Entry(self, bg=ENTRY_BG, fg=ENTRY_FG, font=FONT, validate='key')
        self.age_entry['validatecommand'] = (self.register(self.validate_age), '%P')
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text='Address', bg=BG_COLOR, font=FONT).grid(row=2, column=0, padx=10, pady=5, sticky='s')
        self.address_entry = tk.Entry(self, bg=ENTRY_BG, fg=ENTRY_FG, font=FONT)
        self.address_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text='Report', bg=BG_COLOR, font=FONT).grid(row=3, column=0, padx=10, pady=5, sticky='s')
        self.report_text = tk.Text(self, height=4, width=30, bg=ENTRY_BG, fg=ENTRY_FG, font=FONT)
        self.report_text.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self, text='Add Victim', command=self.add_victim, bg=BG_COLOR, font=BUTTON_FONT).grid(row=4, columnspan=2,pady=10)

        tk.Button(self, text='Show Victim Records', command=self.show_victim_records, bg=BG_COLOR,
                  font=BUTTON_FONT).grid(row=5, columnspan=2, pady=10)

    def show_victim_records(self):
        ShowDetailsWindow(self, "victim")

    def validate_age(self, value):
        return value.isdigit() or value == ""

    def add_victim(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        address = self.address_entry.get()
        report = self.report_text.get("1.0", tk.END)

        if not (name and age.isdigit() and address and report):
            messagebox.showerror("Error", "Invalid input.")
            return

        conn = None
        try:
            conn = sqlite3.connect('crimemanagement.db')
            cursor = conn.cursor()

            cursor.execute('INSERT INTO victim (name, age, address, report) VALUES (?, ?, ?, ?)',
                           (name, age, address, report))
            conn.commit()
            messagebox.showinfo("Success", "Victim record added successfully.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))

        finally:
            if conn:
                conn.close()


# Court Records Management Sub-Window
class CourtRecordsManagement(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Court Records Management")
        self.geometry("500x400")
        self.configure(bg=BG_COLOR)

        tk.Label(self, text='Criminal ID', bg=BG_COLOR, font=FONT).grid(row=0, column=0, padx=10, pady=5, sticky='s')
        self.criminal_id_entry = tk.Entry(self, font=FONT)
        self.criminal_id_entry.grid(row=0, column=1, pady=5)

        tk.Label(self, text='Judge Name', bg=BG_COLOR, font=FONT).grid(row=1, column=0, padx=10, pady=5, sticky='s')
        self.judge_name_entry = tk.Entry(self, font=FONT)
        self.judge_name_entry.grid(row=1, column=1, pady=5)

        #tk.Label(self, text='Hearing Date', bg=BG_COLOR, font=FONT).grid(row=2, column=0, padx=10, pady=5, sticky='s')
        #self.hearing_date_entry = DateEntry(self, font=FONT, date_pattern='y-mm-dd')
        #self.hearing_date_entry.grid(row=2, column=1, pady=5)

        tk.Label(self, text='Verdict', bg=BG_COLOR, font=FONT).grid(row=3, column=0, padx=10, pady=5, sticky='s')
        self.verdict_entry = tk.Entry(self, font=FONT)
        self.verdict_entry.grid(row=3, column=1, pady=5)

        tk.Button(self, text='Add Court Record', command=self.add_court_record, bg=BG_COLOR).grid(row=4, column=1, pady=10)

        tk.Button(self, text='Show Court Records', command=self.show_court_records, bg=BG_COLOR, font=BUTTON_FONT).grid(
            row=5, columnspan=2, pady=10)

    def show_court_records(self):
        ShowDetailsWindow(self, "court_record")


    def add_court_record(self):
        criminal_id = self.criminal_id_entry.get()
        judge_name = self.judge_name_entry.get()
        #hearing_date = self.hearing_date_entry.get()
        verdict = self.verdict_entry.get()

        if not (criminal_id.isdigit() and judge_name and verdict):
            messagebox.showerror("Error", "Invalid input.")
            return

        conn = sqlite3.connect('crimemanagement.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
            INSERT INTO court_record (criminal_id, judge_name, verdict)
            VALUES (?, ?, ?)
            ''', (criminal_id, judge_name, verdict))
            conn.commit()
            messagebox.showinfo("Success", "Court record added successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

if __name__ == "__main__":
    app = CrimeManagementApp()
    app.mainloop()

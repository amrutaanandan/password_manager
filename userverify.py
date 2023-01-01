from tkinter import *
from tkinter import messagebox
import sqlite3

FONT = ('Arial', 25, 'italic')
FONT2 = ('Consolas', 12, 'bold')
FONT3 = ('Consolas', 12, 'bold')
FONT4 = ('Arial', 10, 'normal')

DEEP_BLUE = "#1b4b98"
LIGHT_BLUE = "#00bde4"
GRAY = "#c8d2db"

STATUS = False
USER = None

conn = sqlite3.connect("password.db")
cursor = conn.cursor()


class UserVerify(Tk):
    def __init__(self):
        super().__init__()
        self.newuser_button = None
        self.pwd_verify_entry = None
        self.pwd_verify_label = None
        self.uid_verify_entry = None
        self.verify_button = None
        self.uid_verify_label = None
        self.title("User Verification")
        self.geometry("350x200")
        self.resizable(False, False)
        self.focus()
        self.config(bg="white")

    def verify_credentials_window(self):
        new_label = Label(text="Enter user credentials to proceed", font=FONT4, bg="white")
        new_label.place(x=80, y=20)

        self.uid_verify_label = Label(text="Username: ", font=FONT4, bg="white")
        self.uid_verify_label.place(x=70, y=60)

        self.uid_verify_entry = Text(font=FONT4, width=20, height=0, relief="solid", border=0, bg=GRAY,
                                     highlightcolor=LIGHT_BLUE)
        self.uid_verify_entry.focus()
        self.uid_verify_entry.place(x=150, y=60)

        self.pwd_verify_label = Label(text="Password: ", font=FONT4, bg="white")
        self.pwd_verify_label.place(x=70, y=100)

        self.pwd_verify_entry = Entry(font=FONT4, width=20, bg=GRAY, relief="solid", border=0,
                                      highlightcolor=LIGHT_BLUE, show="*")
        self.pwd_verify_entry.place(x=150, y=100)

        self.verify_button = Button(text="VERIFY", font=FONT2, width=10, relief="solid", borderwidth=0,
                                    bg=DEEP_BLUE, fg=LIGHT_BLUE, command=self.verify_user)
        self.verify_button.place(x=70, y=140)

        self.newuser_button = Button(text="NEW USER?", font=FONT2, width=10, relief="solid", borderwidth=0,
                                     bg=DEEP_BLUE, fg=LIGHT_BLUE, command=self.new_user)
        self.newuser_button.place(x=195, y=140)

        self.mainloop()

    def verify_user(self):
        global STATUS, USER

        username = self.uid_verify_entry.get("1.0", "end-1c")
        password = self.pwd_verify_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Fill out all required fields!")
            STATUS = False
        else:
            cursor.execute('''select userid from userverification where userid = ? and passwd = ?''',
                           (username, password,))
            if len(cursor.fetchall()) == 0:
                messagebox.showerror("Error", "Invalid Credentials!")
                STATUS = False
                self.pwd_verify_entry.delete("1.0", "end")
            else:
                messagebox.showinfo("Message", f"Welcome {username}! :D")
                STATUS = True
                USER = username
                self.after(1, self.destroy())

    def new_user(self):
        global STATUS, USER
        username = self.uid_verify_entry.get("1.0", "end-1c")
        password = self.pwd_verify_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Fill out all required fields!")
            STATUS = False
        else:
            try:
                cursor.execute('''insert into userverification values(?,?)''', (username, password))
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
            else:
                conn.commit()
                STATUS = True
                USER = username
                messagebox.showinfo("Message", f"Hello new user {USER}! :D")
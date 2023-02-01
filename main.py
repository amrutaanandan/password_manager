import csv
from tkinter import *
from tkinter import messagebox
import sqlite3
import random
import pyperclip
import userverify
from popup import Popup
from userverify import UserVerify
import os
import sys
import pandas as pd

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# --------------------CONSTANTS--------------------#

pass_logo = resource_path("password.png")
db = resource_path("password.db")

FONT = ('Arial', 25, 'italic')
FONT2 = ('Consolas', 12, 'bold')
FONT3 = ('Consolas', 12, 'bold')
FONT4 = ('Arial', 10, 'normal')

DEEP_BLUE = "#1b4b98"
LIGHT_BLUE = "#00bde4"
GRAY = "#c8d2db"

LETTERS = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j',
           'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't',
           'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z']
SYMBOLS = ['!' '@', '#', '$', '%', '^', '*', '&', '(', ')', '+', '=', '_', '/']
NUMS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

# --------------------QUERIES--------------------#

SEARCH_QUERY = '''select username, password from password where website =? and userid =?'''
INSERT_QUERY = '''insert into password values(?,?,?,?)'''
DELETE_QUERY = '''delete from password where website =? and userid =?'''
UPDATE_QUERY = '''update password set password =? where website=? and userid=?'''

# --------------------DATABASE CONNECTION--------------------#

conn = sqlite3.connect(db)
cursor = conn.cursor()

# --------------------SECURITY VERIFICATION--------------------#

user = UserVerify()
user.verify_credentials_window()
active_user = userverify.USER

if userverify.STATUS:

    # --------------------WINDOW SETUP--------------------#

    window = Tk()
    window.title("Password Manager")
    window.config(bg="white")
    window.minsize(height=600, width=500)
    canvas = Canvas(width=300, height=300, highlightthickness=0, bg="white")
    logo = PhotoImage(file=pass_logo)
    canvas.create_image(230, 150, image=logo)
    canvas.place(x=30, y=10)
    window.resizable(False, False)

    # --------------------LABELS--------------------#

    title = Label(text="Pass Manager", font=FONT, bg="white", fg=DEEP_BLUE)
    title.place(x=150, y=250)

    username_label = Label(text="USERNAME", font=FONT2, bg="white", fg=DEEP_BLUE, padx=10, pady=10)
    username_label.place(x=50, y=320)

    password_label = Label(text="PASSWORD", font=FONT2, bg="white", fg=DEEP_BLUE, padx=10, pady=10)
    password_label.place(x=50, y=360)

    website_label = Label(text="WEBSITE", font=FONT2, bg="white", fg=DEEP_BLUE, padx=10, pady=10)
    website_label.place(x=50, y=400)

    # --------------------TEXT BOXES--------------------#

    username_entry = Text(font=FONT4)
    username_entry.focus()
    username_entry.config(border=0, highlightcolor=LIGHT_BLUE, highlightthickness=2, width=39, height=0, bg=GRAY)
    username_entry.place(x=150, y=330)

    password_entry = Text(font=FONT4)
    password_entry.config(border=0, highlightcolor=LIGHT_BLUE, highlightthickness=2, width=25, height=0, bg=GRAY)
    password_entry.place(x=150, y=370)

    website_entry = Text(font=FONT4)
    website_entry.config(border=0, highlightcolor=LIGHT_BLUE, highlightthickness=2, width=25, height=0, bg=GRAY)
    website_entry.place(x=150, y=410)

    # --------------------BUTTON COMMANDS--------------------#

    # --------------------SEARCHING FOR ENTRIES--------------------#
    def entry_search():
        website_search = website_entry.get("1.0", "end-1c")
        username_entry.delete("1.0", "end")
        password_entry.delete("1.0", "end")
        user_info = cursor.execute(SEARCH_QUERY, (website_search.lower(), active_user,))
        if not website_search:
            messagebox.showerror("Error", "Fill out all required fields!")
        elif len(user_info.fetchall()) == 0:
            messagebox.showerror("Message", "No such entry exists!")
        else:
            user_info = cursor.execute(SEARCH_QUERY, (website_search.lower(), active_user,))
            user_tuple = user_info.fetchall()
            username = user_tuple[0][0]
            pwd = user_tuple[0][1]
            username_entry.insert(INSERT, username)
            password_entry.insert(INSERT, pwd)

    # --------------------INSERTING NEW PASSWORDS--------------------#

    def insert_passwd():
        website_search = website_entry.get("1.0", "end-1c")
        password_search = password_entry.get("1.0", "end-1c")
        username_search = username_entry.get("1.0", "end-1c")

        if not website_search or not password_search or not username_search:
            messagebox.showerror("Error", "Fill out all required fields!")
        else:
            try:
                cursor.execute(INSERT_QUERY,
                               (username_search.lower(), password_search.lower(), website_search.lower(), active_user,))
            except:
                messagebox.showerror("Error", "Some error has occurred or Website already exists!")
            else:
                popup = Popup()

                message_label1 = Label(popup, text=f"Username: {username_search}", font=FONT4)
                message_label1.place(x=30, y=10)
                message_label2 = Label(popup, text=f"Password: {password_search}", font=FONT4)
                message_label2.place(x=30, y=30)
                message_label3 = Label(popup, text=f"Website: {website_search}", font=FONT4)
                message_label3.place(x=30, y=50)
                confirm = Button(popup, text="CONFIRM?", font=FONT3, width=8, relief="solid", borderwidth=0,
                                 bg=DEEP_BLUE,
                                 fg=LIGHT_BLUE, command=lambda: confirm_query(popup))
                confirm.place(x=110, y=90)

    # --------------------DELETE PASSWORDS--------------------#

    def delete_password():
        website_search = website_entry.get("1.0", "end-1c")
        if not website_search:
            messagebox.showerror("Error", "Fill out all required fields!")
        else:
            try:
                cursor.execute(DELETE_QUERY, (website_search, active_user))
            except:
                messagebox.showerror("Error", "Some error has occurred")
            else:
                popup = Popup()
                message_label = Label(popup, text=f"This will delete {website_search}'s password", font=FONT4)
                message_label.place(x=35, y=40)

                confirm = Button(popup, text="CONFIRM?", font=FONT3, width=8, relief="solid", borderwidth=0,
                                 bg=DEEP_BLUE,
                                 fg=LIGHT_BLUE, command=lambda: confirm_query(popup))
                confirm.place(x=110, y=90)

    # --------------------UPDATE PASSWORDS--------------------#

    def update_password():
        website_search = website_entry.get("1.0", "end-1c")
        password_search = password_entry.get("1.0", "end-1c")
        cursor.execute(SEARCH_QUERY, (website_search.lower(), active_user))

        if not website_search or not password_search:
            messagebox.showerror("Error", "Fill out all required fields!")
        elif len(cursor.fetchall()) == 0:
            messagebox.showerror("Error", "Website entry does not exist!")
        else:
            try:
                cursor.execute(UPDATE_QUERY, (password_search, website_search, active_user))
            except:
                messagebox.showerror("Error", "Some error has occurred!")
            else:
                popup = Popup()
                message_label = Label(popup, text=f"This will update {website_search}'s password", font=FONT4)
                message_label.place(x=35, y=40)

                confirm = Button(popup, text="CONFIRM?", font=FONT3, width=8, relief="solid", borderwidth=0,
                                 bg=DEEP_BLUE,
                                 fg=LIGHT_BLUE, command=lambda: confirm_query(popup))
                confirm.place(x=110, y=90)

    # --------------------GENERATE PASSWORD--------------------#

    def generate_pass():
        password_entry.delete("1.0", "end")
        new_pass = random.sample(LETTERS, 4)
        new_pass.extend(random.sample(SYMBOLS, 4))
        new_pass.extend(random.sample(NUMS, 4))
        random.shuffle(new_pass)
        generated_pass = "".join(new_pass)

        password_entry.insert(INSERT, generated_pass)
        pyperclip.copy(generated_pass)


    def confirm_query(popup):
        conn.commit()
        popup.after(1, lambda: popup.destroy())
        password_entry.delete("1.0", "end")
        username_entry.delete("1.0", "end")
        website_entry.delete("1.0", "end")


    # --------------------GENERATE REPORT--------------------#

    def view_saved_pass():
        try:
            info = cursor.execute("select username, website, password from password where userid=?", (active_user,))
            if(len(info.fetchall()) == 0):
                messagebox.showerror("Error!", "No saved passwords for current users!")
            else:
                cursor.execute("select username, website, password from password where userid=?", (active_user, ))
                db_df = pd.DataFrame(cursor.fetchall())
                db_df.to_csv(f'{active_user}.csv', index=False)
                messagebox.showinfo("Exported!", "Data successfully exported to csv!")
        except:
            messagebox.showerror("Error","Some error has occurred")

    # --------------------BUTTONS--------------------#

    search_button = Button(text="SEARCH", font=FONT3, width=8, relief="solid", borderwidth=0, bg=DEEP_BLUE,
                           fg=LIGHT_BLUE,
                           command=entry_search, padx=5)
    search_button.place(x=338, y=407)

    generate_button = Button(text="GENERATE", font=FONT3, width=8, relief="solid", borderwidth=0, bg=DEEP_BLUE,
                             fg=LIGHT_BLUE, padx=5, command=generate_pass)
    generate_button.place(x=338, y=367)

    save_button = Button(text="SAVE", font=FONT3, width=12, relief="solid", borderwidth=0, bg=LIGHT_BLUE, fg=DEEP_BLUE,
                         command=insert_passwd)
    save_button.place(x=310, y=470)

    update_button = Button(text="UPDATE", font=FONT3, width=12, relief="solid", borderwidth=0, bg=LIGHT_BLUE,
                           fg=DEEP_BLUE,
                           command=update_password)
    update_button.place(x=62, y=470)

    delete_button = Button(text="DELETE", font=FONT3, width=12, relief="solid", borderwidth=0, bg=LIGHT_BLUE,
                           fg=DEEP_BLUE,
                           command=delete_password)
    delete_button.place(x=186, y=470)

    view_pass = Button(text="VIEW ALL SAVED PASSWORDS", font=FONT3, width=39, relief="solid", borderwidth=0,
                       bg=DEEP_BLUE, fg=LIGHT_BLUE, padx=2.5, command=view_saved_pass)
    view_pass.place(x=62, y=510)

    # conn.close()
    window.mainloop()

import sqlite3
conn = sqlite3.connect("password.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()
cursor.execute('''create table password(username varchar(50), password varchar(50), website varchar(100),
 userid varchar(50), foreign key (userid) references userverification(userid))''')
conn.commit()





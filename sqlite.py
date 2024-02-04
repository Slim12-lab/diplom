import sqlite3 as sq

async def db_start():
    global db, cur

    db = sq.connect('new3.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profiles (Personid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                                user TEXT, name TEXT, holiday TEXT, date TEXT)")

    db.commit()

async def create_profile(state, user_id): 
        async with state.proxy() as data:
            cur.execute("INSERT INTO profiles (user, name, holiday, date) VALUES (?,?,?,?)", ( user_id, data['name'], data['holiday'], data['date']))
            db.commit()

async def print_list(user_id):
     cur.execute("SELECT Personid, name, holiday, date FROM profiles WHERE user = ?", (user_id,))
     data = cur.fetchall()
     text = ''
     for row in data:
        text += f"{row[0]}. {row[1]} - {row[2]} - {row[3]}\n"

     return(f"Вот список твоих записей: \n\n{text}")

async def edit_profile(user_id, number, name, holiday, date):
     cur.execute("UPDATE profiles SET name = ?, holiday = ?, date = ? WHERE Personid = ?",
                   (name, holiday, date, number))
    
     db.commit()

async def delete_line(profile_id):
    cur.execute("DELETE FROM profiles WHERE Personid = ?", (profile_id,))
    
    db.commit()

     
import sqlite3 as sq

async def db_start():
    global db, cur

    db = sq.connect('new3.db')
    cur = db.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS profiles (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, \
                    user TEXT NOT NULL,
                    name TEXT NOT NULL,
                    holiday TEXT NOT NULL, 
                    date TEXT NOT NULL,
                    congrats TEXT NOT NULL)''')

    db.commit()

async def create_profile(state, user_id): 
        async with state.proxy() as data:
            cur.execute("INSERT INTO profiles (user, name, holiday, date, congrats) VALUES (?,?,?,?,?)", ( user_id, data['name'], data['holiday'], data['date'], data['text']))
            db.commit()

async def print_list(user_id):
     cur.execute("SELECT name, holiday, date FROM profiles WHERE user = ?", (user_id,))
     data = cur.fetchall()
     text = ''
     for idx, row in enumerate(data, start=1):
        text += f"{idx}. {row[0]} - {row[1]} - {row[2]}\n"
     return(f"Вот список твоих записей: \n\n{text}")

async def edit_profile(user_id, number, name, holiday, date):
     cur.execute("UPDATE profiles SET name = ?, holiday = ?, date = ? WHERE id = ?",
                   (name, holiday, date, number))
    
     db.commit()

async def delete_line(perm, idx):
    try:
        idx = int(idx)  # Преобразуем idx в целое число
    except ValueError:
        return False  # Вернем False, если idx не является целым числом

    cur.execute("SELECT id FROM profiles WHERE user=?", (perm,))
    data = cur.fetchall()
    print(data)

    if 1 <= idx <= len(data):
        task_id_to_delete = data[idx - 1][0]  # Получаем id задачи по номеру idx
        cur.execute("DELETE FROM profiles WHERE id=?", (task_id_to_delete,))
        db.commit()
        return True  # Успешное удаление
    else:
        return False  # Неверный номер задачи
    
    db.commit()

    # Ваша функция get_records_by_date
async def get_records_by_date(date):
    cur.execute("SELECT user, name, holiday, congrats FROM profiles WHERE date=?", (date,))
    records = cur.fetchall()

    result = []
    for record in records:
        user_id, name, holiday, congrats = record
        result.append({'user_id': user_id, 'name': name, 'holiday': holiday, 'congrats': congrats})

    return result
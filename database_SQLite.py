import sqlite3

conn = sqlite3.connect("elephanture.db")


def execute_database(query, arguments):
    conn = sqlite3.connect("elephanture.db")
    c = conn.cursor()
    c.execute(query, arguments)
    conn.commit()
    conn.close()


def multiple_execute_database(query, arguments):
    conn = sqlite3.connect("elephanture.db")
    c = conn.cursor()
    c.executemany(query, arguments)
    conn.commit()
    conn.close()


"""
save all the user who've played our game into "users" table. For example:
==========================================
user_id | user_name       | password     |
--------+-----------------+--------------+
1       | "Alex"          |"123456"      |
2       | "Johnson"       |"abcdef"      |
3       | "Sabrina"       |"elephanture" |
--------+-----------------+--------------+
"""


# find all information of players
def show_all_users():
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * FROM users"""
    c.execute(query)
    users = c.fetchall()
    for user in users:
        print(user)
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


# Check if the user_name and password is taken
def is_user_info_taken(username, password):
    new_username = username.lower()
    check_user = False
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * from users WHERE user_name = ? AND password = ?"""
    c.execute(query, (new_username, password))
    user = c.fetchone()
    if user is not None:
        check_user = True
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return check_user


# Add one record into users table
def insert_one_user(user_name, password):
    new_username = user_name.lower()
    query = """ INSERT INTO users values (?,?,?)"""
    if not is_user_info_taken(user_name, password):
        execute_database(query, (None, new_username, password))
    else:
        print("Those user_name and password is taken. Try another")


# Get id of user
def get_user_id(user_name, password):
    id_of_user = 0
    new_username = user_name.lower()
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT rowid from users WHERE user_name = ? AND password = ?"""
    c.execute(query, (new_username, password))
    user = c.fetchone()
    if user is not None:
        id_of_user = user[0]
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return id_of_user


def delete_user_by_username_and_password(user_name, password):
    new_username = user_name.lower()
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """DELETE FROM users WHERE user_name = ? AND password = ?"""
    c.execute(query, (new_username, password))
    print("information of that user is deleted")
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


def delete_user_by_id(user_id):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """DELETE FROM users WHERE user_id = ? """
    c.execute(query, (user_id,))
    print("information of that user is deleted")
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


"""
save all the items that the user needs to complete our game into the "items" table. For example:
===============================
item_id | item_name |room_id  |
--------+-----------+---------|
1       | "key"     | 0       |
2       | "key"     | 1       |
3       | "book"    | 4       |
4       | "map"     | 3       |
--------+-----------+---------+
"""


def find_all_items():
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * FROM items"""
    c.execute(query)
    users = c.fetchall()
    for user in users:
        print(user)
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


def find_item_by_roomId(room_id):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * FROM items WHERE room_id = ?"""
    c.execute(query, (room_id,))
    item = c.fetchone()
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return item


def is_room_empty(room_id):
    is_empty = False
    if find_item_by_roomId(room_id) is None:
        is_empty = True
    return is_empty


def insert_item(item_name, room_id):
    new_itemName = item_name.lower()
    query = "INSERT INTO items VALUES(?,?,?)"
    if is_room_empty(room_id):
        execute_database(query, (None, new_itemName, room_id))
    else:
        print("That room is not empty")


def delete_item(room_id):
    if not is_room_empty(room_id):
        # Query to database
        query = """DELETE FROM items WHERE room_id = ?"""
        execute_database(query, (room_id,))
        print("that item is deleted")
    else:
        print("there is nothing in room")


def get_item_id_byRoomId(room_id):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT rowid from users WHERE room_id = ?"""
    c.execute(query, (room_id,))
    user = c.fetchone()
    item_id = user[0]
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return item_id


def get_item_id(item_name, room_id):
    new_itemName = item_name.lower()
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT rowid from users WHERE item_name = ? AND room_id = ?"""
    c.execute(query, (new_itemName, room_id))
    user = c.fetchone()
    item_id = user[0]
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return item_id


"""
save all the items that the player collected during play into "items_users" table. For example:
=========================================
item_user_id |   item_id      | user_id | 
-------------+----------------+---------+
1            | 1              | 0       |
2            | 2              | 2       | 
-------------+----------------+---------+
"""


# Insert one record into items_users table
def insert_item_user(username, password, room_id, item_name):
    user_id = get_user_id(username, password)
    item_id = get_item_id(item_name, room_id)
    query = """INSERT INTO items_users VALUES (?,?,?)"""
    execute_database(query, (None, item_id, user_id))


# Find all items that user've collected
def find_All_Items_Users():
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * FROM items_users"""
    c.execute(query)
    items_users = c.fetchall()
    for user_item in items_users:
        print(user_item)
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


# Get list of items ids that not exists in items_users table. That means, our player needs to collect those items
def find_items_id():
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT item_id FROM items WHERE item_id EXCEPT SELECT item_id FROM items_users"""
    c.execute(query)
    items_users = c.fetchall()
    list = []
    for user_item in items_users:
        list.append(user_item[0])
    print(list)
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return list


"""
save all states
=======================
state_id | state_name | 
---------+------------+
1        | "level1"   |
2        | "level2"   |
3        | "level3"   |
4        | "level4"   |
5        | "level5"   |
---------+------------+ 
"""


def find_all_states():
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * FROM states"""
    c.execute(query)
    items_users = c.fetchall()
    for user_item in items_users:
        print(user_item)
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


def is_state_already_exists(state_name):
    new_stateName = state_name.lower()
    result = False
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * FROM states WHERE state_name = ?"""
    c.execute(query, (new_stateName,))
    item = c.fetchone()
    if item is not None:
        result = True
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return result


def insert_state(state_name):
    new_stateName = state_name.lower()
    if not is_state_already_exists(state_name):
        query = """INSERT INTO states VALUES (?,?)"""
        execute_database(query, (None, new_stateName))
    else:
        print("That state is already exists")


def get_state_id_by_name(state_name):
    new_stateName = state_name.lower()
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT state_id FROM states WHERE state_name = ?"""
    c.execute(query, (new_stateName,))
    id = c.fetchone()
    state_id = id[0]
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return state_id


"""
save 
==================================================
state_user_id | user_id | state_id | state_value |
--------------+---------+----------+-------------+
 1            | 1       | 2        | "False"     |
--------------+---------+----------+-------------+
"""


# Check if the user_name and password is taken
def is_state_user_info_taken(username, password, state_name):
    user_id = get_user_id(username, password)
    state_id = get_state_id_by_name(state_name)
    check_user = False
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * from states_users WHERE user_id = ? AND state_id = ?"""
    c.execute(query, (user_id, state_id))
    user = c.fetchone()
    if user is not None:
        check_user = True
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return check_user


def find_all_states_user_():
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * FROM states_users"""
    c.execute(query)
    states_users = c.fetchall()
    for state_user in states_users:
        print(state_user)
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


# Insert one record into items_users table
def insert_state_user(user_name, password, state_name, state_value):
    new_stateValue = state_value.lower()
    user_id = get_user_id(user_name, password)
    state_id = get_state_id_by_name(state_name)
    query = """INSERT INTO states_users VALUES (?,?,?,?)"""
    execute_database(query, (None, user_id, state_id, new_stateValue))


# Get state-user-id
def get_state_user_id(user_id, state_id):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT rowid from states_users WHERE user_id = ? AND state_id = ?"""
    c.execute(query, (user_id, state_id))
    user = c.fetchone()
    id_of_user = user[0]
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return id_of_user


# Update record in states_users table
def update_state_users(username, password, state_name, state_value):
    new_stateValue = state_value.lower()
    user_id = get_user_id(username, password)
    state_id = get_state_id_by_name(state_name)
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    if is_state_user_info_taken(username, password, state_name):
        query = f"""UPDATE states_users SET state_value = ? WHERE user_id=? AND state_id = ?"""
        data = (new_stateValue, user_id, state_id)
        c.execute(query, data)
        print("update-process is successful")
    elif is_user_info_taken(username, password):
        insert_state_user(username, password, state_name, new_stateValue)
        print("insert-process is successful")
    else:
        print("There is no one has the name like you")
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


def delete_state_user(state_user_id):
    query = """DELETE FROM states_users WHERE state_user_id = ?"""
    execute_database(query, (state_user_id,))
    print("delete-process is successful")

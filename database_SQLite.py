import sqlite3


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
0       | "Alex"          |"123456"      |
1       | "Johnson"       |"abcdef"      |
2       | "Sabrina"       |"elephanture" |
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
    check_user = False
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * from users WHERE user_name = ? AND password = ?"""
    c.execute(query, (username, password))
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
    query = """ INSERT INTO users values (?,?,?)"""
    if not is_user_info_taken(user_name, password):
        execute_database(query, (None, user_name, password))
    else:
        print("Those user_name and password is taken. Try another")


# Get id of user
def get_user_id(user_name, password):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT rowid from users WHERE user_name = ? AND password = ?"""
    c.execute(query, (user_name, password))
    user = c.fetchone()
    id_of_user = user[0]
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return id_of_user


def delete_user(user_name, password):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """DELETE FROM users WHERE user_name = ? AND password = ?"""
    c.execute(query, (user_name, password))
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
0       | "key"     | 0       |
1       | "key"     | 1       |
2       | "book"    | 4       |
3       | "map"     | 3       |
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
    query = "INSERT INTO items VALUES(?,?,?)"
    if is_room_empty(room_id):
        execute_database(query, (None, item_name, room_id))
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
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT rowid from users WHERE item_name = ? AND room_id = ?"""
    c.execute(query, (item_name, room_id))
    user = c.fetchone()
    item_id = user[0]
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return item_id


"""
save all the items that the player collected during play into "item_user" table. For example:
=========================================
item_user_id |   item_id      | user_id | 
-------------+----------------+---------+
0            | 1              | 0       |
1            | 2              | 2       | 
-------------+----------------+---------+
"""


# Insert one record into item_user table
def insert_item_user(username, password, room_id):
    user_id = get_user_id(username, password)
    item_id = get_user_id(room_id)
    query = """INSERT INTO item_user VALUES (?,?,?)"""
    execute_database(query, (None, item_id, user_id))


# Find all items that user've collected
def find_All_Item_User():
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT * FROM item_user"""
    c.execute(query)
    items_users = c.fetchall()
    for user_item in items_users:
        print(user_item)
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


# Get list of items ids that not exists in item_user_table. That means, our player needs to collect those items
def find_items_id():
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    # Query to database
    query = """SELECT item_id FROM items WHERE item_id EXCEPT SELECT item_id FROM item_user"""
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


# # Create items table
# conn = sqlite3.connect('elephanture.db')
# c = conn.cursor()
# c.execute("""CREATE TABLE item_user (
#     item_user_id integer,
#     item_id int,
#     user_id int,
#     room_id int
# )
# """)
# conn.commit()
# conn.close()

"""
save all states
=======================
state_id | state_name | 
---------+------------+
0        | "level1"   |
1        | "level2"   |
2        | "level3"   |
3        | "level4"   |
4        | "level5"   |
---------+------------+ 
"""

"""
save 
==================================================
state_user_id | user_id | state_id | state_value |
--------------+---------+----------+-------------+
 0            | 1       | 0        | "false"     |
--------------+---------+----------+-------------+
"""

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

    return users

# Check if the user_name and password is taken
def does_user_exist(username):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    query = """SELECT * FROM users WHERE user_name = ?"""
    c.execute(query, (username))
    user = c.fetchone()
    
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()

    if user is not None:
        return True
    else:
        return False


# Add one record into users table
def insert_user(username, password):
    query = """ INSERT INTO users VALUES (?,?,?)"""
    if not does_user_exist(username):
        if execute_database(query, (None, username, password)):
            print("succesfully added user")
        else:
            print("user was not added")
    else:
        print("This username is taken. Try another one.")


# Get id of user
def get_user_id(username):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    query = """SELECT rowid FROM users WHERE user_name = ?"""
    c.execute(query, username)
    user = c.fetchone()

    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()

    if user is not None:
        return user[0]


def delete_user(username, password):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    query = """DELETE FROM users WHERE user_name = ? AND password = ?"""
    if c.execute(query, (username, password)):
        print("information of that user is deleted")
    else:
        print("user could not be removed from database")

    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()


"""
save all the items that the player collected during play into "user_items" table. For example:
===================================================
user_item_id | user_id |   item_name    | room_id | 
-------------+---------+----------------+---------+
  1          | 1       | "key"          | 0       |
  2          | 1       | "key"          | 2       | 
-------------+---------+----------------+---------+
"""


# Insert one record into user_items table
def insert_item(username, room_id, item_name):
    user_id = get_user_id(username)

    query = """INSERT INTO user_items VALUES (?,?,?,?)"""
    if execute_database(query, (None, user_id, item_name, room_id)):
        print("succesfully added item")
    else:
        print("item was not added")


# Find all items that user has collected
def get_all_user_items(username):
    user_id = get_user_id(username)
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    query = """SELECT item_name, room_id FROM user_items WHERE user_id = ?"""
    c.execute(query, (user_id))
    items = c.fetchall()

    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()

    return items

# Find all items of one room, that user has collected
def get_user_items_by_roomId(room_id, username):
    user_id = get_user_id(username)

    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    query = """SELECT item_name FROM user_items WHERE room_id = ? AND user_id = ?"""
    c.execute(query, (room_id, user_id))
    items = c.fetchall()

    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()

    return items

# Find one specific item of a user
def does_user_item_exist(username, item_name, room_id):
    user_id = get_user_id(username)

    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    query = """SELECT item_name FROM user_items WHERE room_id = ? AND user_id = ? AND item_name = ?"""
    c.execute(query, (room_id, user_id, item_name))
    item = c.fetchone()

    if item is not None:
        return True
    else:
        return False

def delete_user_item(username, item_name, room_id):
    user_id = get_user_id(username)

    if does_user_item_exist(username, item_name, room_id):
        # Query to database
        query = """DELETE FROM user_items WHERE room_id = ? AND user_id = ? AND item_name = ?"""
        if execute_database(query, (room_id, user_id, item_name)):
            print("that item is deleted")
        else:
            print("item was not deleted")
    else:
        print("No such item was found from that player")


"""
save 
====================================================
user_state_id | user_id | state_name | state_value |
--------------+---------+------------+-------------+
 1            | 1       | level1     | 0           |
--------------+---------+------------+-------------+
"""

# Check if the user_name and password is taken
def does_user_state_exist(username, state_name):
    user_id = get_user_id(username)

    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    query = """SELECT * FROM user_states WHERE user_id = ? AND state_name = ?"""
    c.execute(query, (user_id, state_name))
    user = c.fetchone()
    
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()

    if user is not None:
        return True
    else:
        return False

# Returns all states of one user
def get_all_user_states(username):
    user_id = get_user_id(username)
    
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    query = """SELECT state_name, state_value FROM user_states WHERE user_id = ?"""
    c.execute(query, (user_id))
    user_states = c.fetchall()
    
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()

    return user_states

# Insert one state into user_states table
def insert_user_state(username, state_name, state_value):
    user_id = get_user_id(username)

    query = """INSERT INTO user_states VALUES (?,?,?,?)"""
    if execute_database(query, (None, user_id, state_name, state_value)):
        print("state was sucessfully added")
    else:
        print("state was not added")

# Get state-user-id
def get_user_state_id(user_id, state_name):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    query = """SELECT rowid FROM user_states WHERE user_id = ? AND state_name = ?"""
    c.execute(query, (user_id, state_name))
    user = c.fetchone()

    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()

    return user[0]

# Update record in user_states table
def update_user_state(username, state_name, state_value):
    user_id = get_user_id(username)

    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    if does_user_state_exist(username, state_name):
        query = """UPDATE user_states SET state_value = ? WHERE user_id = ? AND state_name = ?"""
        if c.execute(query, (state_value, user_id, state_name)):
            print("state was updated successful")
        else:
            print("state was not updated")

    elif does_user_exist(username):
        if insert_user_state(username, state_name, state_value):
            print("state was added successful")
        else:
            print("state was not added")

    else:
        print("There is no such user that can get a state")
    
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()

# Returns the value of a state in int
def get_user_state_value(username, state_name):
    user_id = get_user_id(username)

    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()

    # Query to database
    if does_user_state_exist(username, state_name):
        query = """SELECT state_value FROM user_states WHERE user_id = ? AND state_name = ?"""
        c.execute(query, (user_id, state_name))
        state_value = c.fetchone()

        if state_value[0] == 1:
            return True
        else:
            return False

    elif does_user_exist(username):
        if insert_user_state(username, state_name, 0):
            print("default state was added successful")
        else:
            print("default state was not added")
    
    return False

# Deletes one state of a user
def delete_user_state(username, state_name):
    user_id = get_user_id(username)

    query = """DELETE FROM user_states WHERE user_id = ? AND state_name = ?"""
    if execute_database(query, (user_id, state_name)):
        print("user state was deleted successful")
    else:
        print("user state was not deleted")

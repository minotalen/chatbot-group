import sqlite3


# ist not used, this is a global variable
# conn = sqlite3.connect("elephanture.db")


def execute_database(query, arguments):
    # Connect to database
    conn = sqlite3.connect("elephanture.db")
    # create a cursor
    c = conn.cursor()
    try:
        # execute the Query
        c.execute(query, arguments)
    except sqlite3.Error as error:
        return (error, None, None)

    # fetches SELECT  all returns
    data = c.fetchall()

    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return (None, data)


'''
    is not used
def multiple_execute_database(query, arguments):
    conn = sqlite3.connect("elephanture.db")
    c = conn.cursor()
    c.executemany(query, arguments)
    conn.commit()
    conn.close()
    return conn
'''

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
    # Query to database
    query = """SELECT * FROM users"""
    fetch = execute_database(query, None)
    e = fetch[0]
    if e is not None:
        print("Failed to get all users", e)
    else:
        print("succesfully got all users")
    users = fetch[1]
    return users


# Check if the user_name is taken
def does_user_exist(username):
    # Query to database
    query = """SELECT * FROM users WHERE user_name = ?"""
    fetch = execute_database(query, (username,))
    user = fetch[1]

    if user is None or not user:
        return False

    if user[0] is not None:
        return True
    else:
        return False

# Check if the password fits the username
def is_user_valid(username, password):
    query = """SELECT * FROM users WHERE user_name = ? AND password = ?"""
    fetch = execute_database(query, (username, password,))
    user = fetch[1]
    
    if user is None or not user:
        return False

    if user[0] is not None:
        return True
    else:
        return False

# Add one record into users table
def insert_user(username, password):
    query = """ INSERT INTO users VALUES (?,?,?)"""
    if not does_user_exist(username):
        fetch = execute_database(query, (None, username, password,))
        e = fetch[0]
        if e is not None:
            print("Failed to add user", e)
        else:
            print("succesfully added user")
    else:
        print("This username is taken. Try another one.")


# Get id of user
def get_user_id(username):
    # Query to database
    if not does_user_exist(username):
        return -1

    query = """SELECT rowid FROM users WHERE user_name = ?"""
    fetch = execute_database(query, (username,))
    user = fetch[1]

    if user is None or not user:
        return -1

    if user[0] is not None:
        return user[0][0]
    else:
        return -1


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

    if user_id is not None and not does_user_item_exist(username, item_name, room_id):
        query = """INSERT INTO user_items VALUES (?,?,?,?)"""
        fetch = execute_database(query, (None, user_id, item_name, room_id,))
        e = fetch[0]
        if e is not None:
            print("Failed to add item", e)
        else:
            print("succesfully added item")
    else:
        print("user not found")


# Find all items that user has collected
def get_all_user_items(username):
    user_id = get_user_id(username)
    # Query to database
    query = """SELECT item_name, room_id FROM user_items WHERE user_id = ?"""
    fetch = execute_database(query, (user_id,))
    items = fetch[1]
    e = fetch[0]
    if e is not None:
        print("Failed to get all user items", e)
    else:
        print("got all items")
    return items


# Find all items of one room, that user has collected
def get_user_items_by_roomId(room_id, username):
    user_id = get_user_id(username)
    # Query to database
    query = """SELECT item_name FROM user_items WHERE room_id = ? AND user_id = ?"""
    fetch = execute_database(query, (room_id, user_id,))
    items = fetch[1]
    e = fetch[0]
    if e is not None:
        print("Failed to get user items by roomID", e)
    else:
        print("got all items")
    return items


# Find one specific item of a user
def does_user_item_exist(username, item_name, room_id):
    user_id = get_user_id(username)
    # Query to database
    query = """SELECT item_name FROM user_items WHERE room_id = ? AND user_id = ? AND item_name = ?"""
    fetch = execute_database(query, (room_id, user_id, item_name,))
    item = fetch[1]
    e = fetch[0]
    if e is not None:
        print("Failed to check user items", e)
    else:
        print("checked user items")

    if item is None or not item:
        return False

    if item[0] is not None:
        return True
    else:
        return False


def delete_user_item(username, item_name, room_id):
    user_id = get_user_id(username)

    if does_user_item_exist(username, item_name, room_id):
        # Query to database
        query = """DELETE FROM user_items WHERE room_id = ? AND user_id = ? AND item_name = ?"""
        fetch = execute_database(query, (room_id, user_id, item_name,))
        e = fetch[0]
        if e is not None:
            print("Failed to delete item", e)
        else:
            print("that item is deleted")
    else:
        print("No such item was found from that player")


"""Just for fix bug"""


def delete_user_item_by_useritemid(user_item_id):
    query = """DELETE FROM user_items WHERE user_item_id = ? """
    execute_database(query, (user_item_id,))


def delete_user_item_by_username(username):
    user_id = get_user_id(username)
    if user_id is not None:
        query = """DELETE FROM user_items WHERE user_id = ?"""
        fetch = execute_database(query, (user_id,))
        e = fetch[0]
        if e is not None:
            print("Failed to delete item", e)
        else:
            print("that user_item is deleted by", username)
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
    # Query to database
    query = """SELECT * FROM user_states WHERE user_id = ? AND state_name = ?"""
    fetch = execute_database(query, (int(user_id), state_name,))
    user = fetch[1]
    e = fetch[0]
    if e is not None:
        print("Failed to check user_state", e)

    if user is None or not user:
        return False

    if user[0] is not None:
        return True
    else:
        return False


# Returns all states of one user
def get_all_user_states(username):
    user_id = get_user_id(username)
    # Query to database
    query = """SELECT state_name, state_value FROM user_states WHERE user_id = ?"""
    fetch = execute_database(query, (user_id,))
    user_states = fetch[1]
    e = fetch[0]
    if e is not None:
        print("Failed to get all user states", e)

    return user_states


# Insert one state into user_states table
def insert_user_state(username, state_name, state_value):
    user_id = get_user_id(username)

    if user_id is not None:
        query = """INSERT INTO user_states VALUES (?,?,?,?)"""
        fetch = execute_database(
            query, (None, int(user_id), state_name, state_value,))
        e = fetch[0]
        if e is not None:
            print("Failed to add state", e)
        else:
            print("state was sucessfully added")


# Get state-user-id
def get_user_state_id(user_id, state_name):
    # Query to database
    query = """SELECT rowid FROM user_states WHERE user_id = ? AND state_name = ?"""
    fetch = execute_database(query, (user_id, state_name,))
    e = fetch[0]
    if e is not None:
        print("Failed to get state-user-ID", e)
    user = fetch[1]

    if user is None or not user:
        return -1

    return user[0]


# Update record in user_states table
def update_user_state(username, state_name, state_value):
    user_id = get_user_id(username)
    # Query to database
    if does_user_state_exist(str(username), str(state_name)):
        query = """UPDATE user_states SET state_value = ? WHERE user_id = ? AND state_name = ?"""
        fetch = execute_database(query, (state_value, user_id, state_name,))
        e = fetch[0]
        if e is not None:
            print("Failed to update state", e)
        else:
            print("state was updated successful")

    elif does_user_exist(username):
        insert_user_state(username, state_name, state_value)
        print("state was added successful")

    else:
        print("There is no such user that can get a state")


# Returns the value of a state in int
def get_user_state_value(username, state_name, add_if_none=True):
    user_id = get_user_id(username)
    # Query to database
    if does_user_state_exist(username, state_name):
        query = """SELECT state_value FROM user_states WHERE user_id = ? AND state_name = ?"""
        fetch = execute_database(query, (int(user_id), state_name,))
        state_value = fetch[1]

        if state_value is None:
            return False

        if state_value[0][0] == 1:
            return True

    elif does_user_exist(username) and add_if_none:
        insert_user_state(username, state_name, 0)
        print("default state was added successful")

    return False


# Deletes one state of a user
def delete_user_state(username, state_name):
    user_id = get_user_id(username)

    if user_id is not None:
        query = """DELETE FROM user_states WHERE user_id = ? AND state_name = ?"""
        fetch = execute_database(query, (user_id, state_name,))
        e = fetch[0]
        if e is not None:
            print("Failed to delete user state", e)
        else:
            print("user state was deleted successful")


# Delete one state by user name
def delete_user_state_by_username(username):
    user_id = get_user_id(username)

    if user_id is not None:
        query = """DELETE FROM user_states WHERE user_id = ?"""
        fetch = execute_database(query, (user_id,))
        e = fetch[0]
        if e is not None:
            print("Failed to delete user state", e)
        else:
            print("user state was deleted successful")


"""just for fix bug"""


def delete_user_state_by_userstateid(user_state_id):
    query = """DELETE FROM user_states WHERE user_state_id = ?"""
    execute_database(query, (user_state_id,))


def delete_user(username, password):
    delete_user_item_by_username(username)
    delete_user_state_by_username(username)
    # Query to database
    query = """DELETE FROM users WHERE user_name = ? AND password = ?"""
    fetch = execute_database(query, (username, password,))
    e = fetch[0]
    if e is not None:
        print("Failed to delete user", e)
    else:
        print("information of that user is deleted")


"""
====================================================
user_recmessage_id | user_id | messages |
-------------------+---------+----------+
 1                 | 1       | level1   |
-------------------+---------+----------+
"""


def insert_user_recmessage(username: str, messages: int = -1):
    user_id = get_user_id(username)
    if user_id == -1:
        return False
    else:
        query = """INSERT INTO user_recmessage VALUES (?,?,?)"""
        execute_database(query, (None, user_id, messages,))
        return True


# Check if the user_name and password is taken
def does_user_recmessage_exist(username: str, message: int):
    user_id = get_user_id(username)
    # Query to database
    query = """SELECT * FROM user_recmessage WHERE user_id = ? AND messages = ?"""
    fetch = execute_database(query, (user_id, message,))
    user = fetch[1]
    if user is None or not user: return False
    if user[0] is not None:
        if user[0][1] == user_id and user[0][2] == message: return True
        else: return False
    else: return False


# Deletes one state of a user
def delete_user_recmessage(username: str, messages: int = -1):
    user_id = get_user_id(username)
    if does_user_recmessage_exist(username, messages):
        if user_id != -1:
            query = """DELETE FROM user_recmessage WHERE user_id = ? AND messages = ?"""
            fetch = execute_database(query, (user_id, messages,))
            e = fetch[0]
            if e is not None:
                print("unable to delete user haven't received message yet!", e)
                return False
            else:
                print("deleted receive message from user")
                return True
        else:
            return False
    else:
        print("nothing to delete")
        return False        

# insert_user("Max", "123456")
# insert_user("Jacobh", "123456")
# insert_user("a", "123456")
# insert_user("b", "123456")

# insert_user_recmessage("Max", 1)
# insert_user_recmessage("Jacobh", 3)
# insert_user_recmessage("a", 4)
# insert_user_recmessage("b", 5)

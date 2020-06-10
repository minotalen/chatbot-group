import sqlite3

# ist not used, this is a global variable
#conn = sqlite3.connect("elephanture.db")


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
        
    # fetches SELECT returns
    data0 = c.fetchone()
    # fetches SELECT all returns
    data1 = c.fetchall()
    # Commit our command
    conn.commit()
    # Close the connection
    conn.close()
    return (None, data0, data1)



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
    if (e != None):
        print("Failed to get all users", e)
    else: print("succesfully got all users")
    users = fetch[2]
    return users


# Check if the user_name and password is taken
def does_user_exist(username):
    
    # Query to database
    query = """SELECT * FROM users WHERE user_name = ?"""
    fetch = execute_database(query, (username,))
    user = fetch[1]
    
    if user is not None:
        return True
    else:
        return False


# Add one record into users table
def insert_user(username, password):
    query = """ INSERT INTO users VALUES (?,?,?)"""
    if not does_user_exist(username):
        fetch = execute_database(query, (None, username, password,))
        e = fetch[0]
        if (e != None):
            print("Failed to add user", e)
        else: print("succesfully added user")
    else:
        print("This username is taken. Try another one.")


# Get id of user
def get_user_id(username):

    # Query to database
    query = """SELECT rowid FROM users WHERE user_name = ?"""
    fetch = execute_database(query, (username,))
    user = fetch[1]
    if user is not None:
        return user


def delete_user(username, password):

    # Query to database
    query = """DELETE FROM users WHERE user_name = ? AND password = ?"""
    fetch = execute_database(query, (username, password,))
    e = fetch[0]
    if (e != None):
        print("Failed to delete user", e)
    else: print("information of that user is deleted")


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

    if user_id is not None:
        query = """INSERT INTO user_items VALUES (?,?,?,?)"""
        fetch = execute_database(query, (None, user_id, item_name, room_id,))
        e=fetch[0]
        if (e != None):
            print("Failed to add item", e)
        else: print("succesfully added item")
    else: print("user not found")
    


# Find all items that user has collected
def get_all_user_items(username):
    user_id = get_user_id(username)
    # Query to database
    query = """SELECT item_name, room_id FROM user_items WHERE user_id = ?"""
    fetch = execute_database(query, (user_id,))
    items = fetch[2]
    e = fetch[0]
    if (e != None):
        print("Failed to get all user items", e)
    else: print("")    
    return items

# Find all items of one room, that user has collected
def get_user_items_by_roomId(room_id, username):
    user_id = get_user_id(username)
    # Query to database
    query = """SELECT item_name FROM user_items WHERE room_id = ? AND user_id = ?"""
    fetch = execute_database(query, (room_id, user_id,))
    items = fetch[2]
    e = fetch[0]
    if (e != None):
        print("Failed to get user items by roomID", e)
    else: print("")
    return items

# Find one specific item of a user
def does_user_item_exist(username, item_name, room_id):
    user_id = get_user_id(username)
    # Query to database
    query = """SELECT item_name FROM user_items WHERE room_id = ? AND user_id = ? AND item_name = ?"""
    fetch = execute_database(query, (room_id, user_id, item_name,))
    item = fetch[1]
    e = fetch[0]
    if (e != None):
        print("Failed to check user items", e)
    else: print("")
    if item is not None:
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
        if (e != None):
            print("Failed to delete item", e)
        else: print("that item is deleted")
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
    fetch = execute_database(query, (user_id, state_name,))
    user = fetch[1]
    e = fetch[0]
    if (e != None):
        print("Failed to check user_state", e)
    else: print("")    
    if user is not None:
        return True
    else:
        return False


# Returns all states of one user
def get_all_user_states(username):
    user_id = get_user_id(username)   
    # Query to database
    query = """SELECT state_name, state_value FROM user_states WHERE user_id = ?"""
    fetch = execute_database(query, (user_id,))
    user_states = fetch[2]
    e = fetch[0]
    if (e != None):
        print("Failed to get all user states", e)
    else: print("")
    return user_states


# Insert one state into user_states table
def insert_user_state(username, state_name, state_value):
    user_id = get_user_id(username)

    if user_id is not None:
        query = """INSERT INTO user_states VALUES (?,?,?,?)"""
        fetch = execute_database(query, (None, user_id, state_name, state_value,))
        e = fetch[0]
        if (e != None):
            print("Failed to add state", e)
        else: print("state was sucessfully added")
    

# Get state-user-id
def get_user_state_id(user_id, state_name):
    # Query to database
    query = """SELECT rowid FROM user_states WHERE user_id = ? AND state_name = ?"""
    fetch = execute_database(query, (user_id, state_name,))
    e = fetch[0]
    if (e != None):
        print("Failed to get state-user-ID", e)
    else: print("")
    user = fetch[1]
    return user[0]
    

# Update record in user_states table
def update_user_state(username, state_name, state_value):
    user_id = get_user_id(username)
    # Query to database
    if does_user_state_exist(username, state_name):
        query = """UPDATE user_states SET state_value = ? WHERE user_id = ? AND state_name = ?"""
        fetch = execute_database(query, (state_value, user_id, state_name,))
        e = fetch[0]
        if (e != None):
            print("Failed to update state", e)
        else: print("state was updated successful")

    elif does_user_exist(username):
        insert_user_state(username, state_name, state_value)
        print("state was added successful")
        
    else:
        print("There is no such user that can get a state")
        

# Returns the value of a state in int
def get_user_state_value(username, state_name):
    user_id = get_user_id(username)
    # Query to database
    if does_user_state_exist(username, state_name):
        query = """SELECT state_value FROM user_states WHERE user_id = ? AND state_name = ?"""
        fetch = execute_database(query, (user_id, state_name,))
        state_value = fetch[1]

        if state_value[0] == 1:
            return True
        else:
            return False

    elif does_user_exist(username):
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
        if (e != None):
            print("Failed to delete user state", e)
        else: print("user state was deleted successful")
    
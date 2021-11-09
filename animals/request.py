# ⭕️ right now, we're hard-writing data.
# ⭕️ Eventually, we will fetch data from a server.
import sqlite3
import json

from models import Animal, Location, Customer

# ⭕️ ANIMALS : all capitalized means it's a "const". You can't change/overwite the list itself.
ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 4,
        "status": "Assessment"
    },
    {
        "id": 2,
        "name": "Gypsy",
        "species": "Dog",
        "location": 1,
        "customerId": 2,
        "status": "Admitted"
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 2,
        "customerId": 1,
        "status": "Treatment"
    }
]


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.db") as conn:
    #  keyword with will open a file connection fro you, 
    #  at line 102, the indentation stops, means the file connection is shut down.
    
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor() # ⭕️cursor prepares you to execute a statement, it will scan table for you⭕️

        # Write the SQL query (a multi-line string) to get the information you want
        # alias Animal and Location to a , l 
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name AS location_name,
            l.address AS location_address,
            c.name AS customer_name,
            c.address AS customer_address,
            c.email AS customer_email,
            c.password AS customer_password
        FROM Animal a 
        JOIN Location l
            ON a.location_id = l.id
        JOIN Customer c
            ON a.customer_id = c.id
        """)
        # the goal is to get sth like this:
            # "id": 6,
            # "name": "Daps",
            # "species": "Kennel",
            # "status": "Boxer",
            # "location_id": 2,
            # "customer_id": 2,
            # "location": {
            #     "name": "Nashville South",
            #     "address": "101 Penn Ave"
            # },
            # "customer": {
            #     "name": "Jenna",
            #     "address": "101 Penn Ave",
            #     "email": "jenna@solis.com",
            #     "password": "password"

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in exact order of the parameters defined in the Animal class above.
            # set debugger: import pdb; pdb.set_trace()
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])  
            #⭕️pass all these arguments into the Animal class in animal.py, return an object instance⭕️
            
            # import Location class from models, and Create a Location instance from the current row
            location = Location(row['id'], row['location_name'], row['location_address'])
            customer = Customer(row['id'], row['customer_name'], row['customer_address'],row['customer_email'],row['customer_password'])
            
            # We've added a self.location = None in the Animal class,
            # Now add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__
            
            animals.append(animal.__dict__)  #⭕️turn the object into a dictionary⭕️

    # Use `json` package to properly serialize list as JSON
    return json.dumps(animals)  #⭕️convert Python data type to a string.⭕️



# Function with a single parameter
def get_single_animal(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))
        # ⭕️⭕️⭕️ to prevent sqi-injection. By using this format (instead of just using f string to pass id in), 
        # we sanitize the input url.

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        return json.dumps(animal.__dict__)



def get_animal_by_status(status):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.status = ?
        """, ( status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'] , row['location_id'], row['customer_id'])
            # Animal(*row)  -- unpacking all the row values onto each slots of line 161-166. 
            animals.append(animal.__dict__)

    return json.dumps(animals)


def get_animals_by_location_id(location_id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.location_id = ?
        """, ( location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'] , row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)

    return json.dumps(animals)

#  post a new animal
def create_animal(new_animal):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['species'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], ))

        # The `lastrowid` property on the cursor will return the primary key of the last thing that got added to the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that was sent by the client so that 
        # the client sees the primary key in the response.
        new_animal['id'] = id


    return json.dumps(new_animal)



def delete_animal(id):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))


def update_animal(id, new_animal): 
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
        SET
            name = ?,
            breed = ?,
            status = ?,
            location_id = ?,
            customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # 🚫🚫🚫 Forces 404 response by main module
        return False
    else:
        # ⭕️⭕️⭕️ Forces 204 response (No) by main module
        return True







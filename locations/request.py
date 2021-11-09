import sqlite3
import json

from models import Location


LOCATIONS = [
    {
      "id": 1,
      "name": "Nashville North",
      "address": "8422 Johnson Pike"
    },
    {
      "id": 2,
      "name": "Nashville South",
      "address": "209 Emory Drive"
    }
]

def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query (a multi-line string) to get the information you want
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l  
        """)

        # Initialize an empty list to hold all animal representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            location = Location(row['id'], row['name'], row['address'])  
            #⭕️⭕️⭕️  pass all these arguments into the Animal class in animal.py, return an object instance
            
            locations.append(location.__dict__)  #⭕️⭕️⭕️ turn the object into a dictionary 

    # Use `json` package to properly serialize list as JSON
    return json.dumps(locations)  #⭕️⭕️⭕️ convert Python data type to a string.



def get_single_location(id):
   with sqlite3.connect("./kennel.db") as conn:
       conn.row_factory = sqlite3.Row
       db_cursor = conn.cursor()
       
       db_cursor.execute("""
       SELECT a.id,
              a.name,
              a.address
       FROM location a
       WHERE a.id = ?
       """, (id, ))
       
       data = db_cursor.fetchone()
       
       location = Location(data["id"], data["name"], data["address"])
       
       return json.dumps(location.__dict__)


def create_location(location):
    new_location_id = LOCATIONS[-1]["id"] + 1

    location["id"] = new_location_id

    LOCATIONS.append(location)

    return location


def delete_location(id):
    location_index = -1 # when index is not found, it's -1
    
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index
    
    if location_index > -1:
        LOCATIONS.pop(index)
        

def update_location(id, new_location):
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location      
            break
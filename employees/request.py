import sqlite3
import json

from models import Employee, Location

EMPLOYEES = [
    {
        "id": 1,
        "name": "Emma Beaton",
        "locationId": 1
    },
    {
        "id": 2,
        "name": "Tom Tommerson",
        "locationId": 2
    }
]


def get_all_employees():
    with sqlite3.connect("./kennel.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query (a multi-line string) to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.location_id,
            e.address,
            l.name AS location_name,
            l.address AS location_address
        FROM employee e
        JOIN location l
            ON e.location_id = l.id
        """)

        # Initialize an empty list to hold all animal representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])  
            #⭕️⭕️⭕️  pass all these arguments into the Animal class in animal.py, return an object instance
            
            location = Location(row["id"], row["location_name"], row["location_address"])
            
            employee.location = location.__dict__
            
            employees.append(employee.__dict__)  #⭕️⭕️⭕️ turn the object into a dictionary 

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)  #⭕️⭕️⭕️ convert Python data type to a string.



def get_single_employee(id):
   with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e,address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        employee = Employee(data['id'], data['name'], data['address'], data['location_id'])

        return json.dumps(employee.__dict__)


def get_employees_by_location_id(location_id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e,address,
            e.location_id
        FROM employee e
        WHERE e.location_id = ?
        """, ( location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
            employees.append(employee.__dict__)

    return json.dumps(employees)


def save_employee(new_employee):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO employee
            ( name, address, location_id )
        VALUES
            ( ?, ?, ?);
        """, (new_employee['name'],new_employee['address'], new_employee['location_id']))

        # The `lastrowid` property on the cursor will return the primary key of the last thing that got added to the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the employee dictionary that was sent by the client so that 
        # the client sees the primary key in the response.
        new_employee['id'] = id

    return json.dumps(new_employee)


def delete_employee(id):
    employee_index = -1
    
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"]  == id:
            employee_index = index
    
    if employee_index > 0:
        EMPLOYEES.pop(employee_index)
        
        
def update_employee(id, new_employee): 
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE employee
        SET
            name = ?,
            address = ?,
            location_id = ?,
        WHERE id = ?
        """, (new_employee['name'], new_employee['address'], new_employee['location_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # 🚫🚫🚫 Forces 404 response by main module
        return False
    else:
        # ⭕️⭕️⭕️ Forces 204 response (No) by main module
        return True
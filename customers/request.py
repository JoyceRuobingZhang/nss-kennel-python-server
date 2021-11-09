import sqlite3
import json

from models import Customer


CUSTOMERS = [
     {
      "id": 1,
      "name": "Hannah Hall",
      "address": "7002 Chestnut Ct"
    },
    {
      "id": 2,
      "name": "Bob Bobberson",
      "address": "200 Happy Dr",
      "email": "bob@nss.com"
    },
    {
      "id": 3,
      "name": "Jack Jackson",
      "address": "567 Harding Place"
    }
]

def get_all_customers():
    with sqlite3.connect("./kennel.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query (a multi-line string) to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.email
        FROM customer a
        """)

        # Initialize an empty list to hold all animal representations
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            customer = Customer(row['id'], row['name'], row['address'], row["email"])  
            #⭕️⭕️⭕️  pass all these arguments into the Animal class in animal.py, return an object instance
            
            customers.append(customer.__dict__)  #⭕️⭕️⭕️ turn the object into a dictionary 

    # Use `json` package to properly serialize list as JSON
    return json.dumps(customers)  #⭕️⭕️⭕️ convert Python data type to a string.


def get_single_customer(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        WHERE c.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        customer = Customer(data['id'], data['name'], data["address"], data["email"], data["password"])

        return json.dumps(customer.__dict__)


def get_customers_by_email(email):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)


def create_customer(customer):
    new_customer_id = CUSTOMERS[-1]["id"] + 1

    customer["id"] = new_customer_id

    CUSTOMERS.append(customer)

    return customer
  

def delete_customer(id):
  customer_index = -1
  
  for index, customer in enumerate(CUSTOMERS):
    if customer["id"] == id:
      customer_index = index
    
    if customer_index > -1:
      CUSTOMERS.pop(customer_index)
      
      
def update_customer(id, new_customer):
  for index, customer in enumerate(CUSTOMERS):
    if customer["id"]  == id:
      CUSTOMERS[index] = new_customer
      break
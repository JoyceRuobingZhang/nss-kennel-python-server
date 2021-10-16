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
    return CUSTOMERS


def get_single_customer(id):
    requested_customer = None
    
    for customer in CUSTOMERS:
        if customer["id"] == id:
            requested_customer = customer
    
    return requested_customer
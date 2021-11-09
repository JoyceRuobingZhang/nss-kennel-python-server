# import things from the standard library first. (order alphabetically)
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# 2nd: import thirdparty packages that are not from the standard library.

# 3rd: import modules we made.
from animals import (
    get_all_animals, 
    get_single_animal, 
    create_animal, 
    delete_animal, 
    update_animal, 
    get_animal_by_status, 
    get_animals_by_location_id)
from locations import (
    get_all_locations, 
    get_single_location, 
    create_location, 
    delete_location, 
    update_location)
from customers import (
    get_all_customers, 
    get_single_customer, 
    create_customer, 
    delete_customer, 
    update_customer, 
    get_customers_by_email)
from employees import (
    get_all_employees, 
    get_single_employee, 
    save_employee, 
    delete_employee, 
    update_employee, 
    get_employees_by_location_id)


# Here's a class. It inherits from another class.
# For now, think of a class as 📦 a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # ⭕️ we are creating our own class HandleRequests based on the BaseHTTPRequestHandler we imported.

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


    # Another method! This supports requests with the OPTIONS verb.
    # ⭕️ letting the clients know what it supports as a server.
    def do_OPTIONS(self):
        self.send_response(200) #Get
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


   
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)



    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2 items in it, 
        # which means the request was for`/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"

                else:
                    response = f"{get_all_animals()}"
            
            if resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"                  
                else:
                    response = f"{get_all_locations()}"

            if resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
                    
            if resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
            
            #  Response from parse_url() is a tuple with 3
            # items in it, which means the request was for
            # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

                # Is the resource `customers` and was there a
                # query parameter that specified the customer
                # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)
            else:
                response = get_all_customers()  
                #⭕️just to give it a fall back if the key or value has sth wrong
                # ??? will also need to give get_all_customers a default parameter: location_id = None

            if resource == "animals":
                if key == "status":
                    response = get_animal_by_status(value)
                elif key == "location_id":
                    response = get_animals_by_location_id(value)
                
            
            if key == "location_id" and resource == "employees":
                response = get_employees_by_location_id(value)

        self.wfile.write(response.encode())
        #⭕️⭕️⭕️ to fetch the response and use it in frontend: 
        # 示例: fetch("http://localhost:8000/posts").then(response => response.json()).then(setFeed)


    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201) #Created
        content_len = int(self.headers.get('content-length', 0))
        # ⭕️headers are key-value pairs, like dictionary, but it's an object。⭕️
        post_body = self.rfile.read(content_len)

        # ⭕️Convert JSON string to a Python dictionary. (content was a string, cuz string is easy to send.)⭕️
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_customer = None 
        new_location = None
        new_employee = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)
            # Encode the new animal and send in response
            self.wfile.write(f"{new_animal}".encode())

        elif resource == "customers":
            new_customer = create_customer(post_body)
            self.wfile.write(f"{new_customer}".encode())


        elif resource == "locations":
            new_location = create_location(post_body)
            self.wfile.write(f"{new_location}".encode())

        elif resource == "employees":
            new_employee = save_employee(post_body)
            self.wfile.write(f"{new_employee}".encode())
            
            
    # Here's a method on the class that overrides the parent's method. * It handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # rest of the elif's
            
        # if resource == "locations":
        #     success = update_location(id, post_body)
            
        # if resource == "customers":
        #     success = update_customer(id, post_body)
            
        if resource == "employees":
            success = update_employee(id, post_body)
        
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the new animal and send in response
        self.wfile.write("".encode())
            
    
    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        
        if resource == "locations":
            delete_location(id)
            
        if resource == "customers":
            delete_customer(id)
            
        if resource == "employees":
            delete_employee(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()
    # ⭕️ every time HTTPServer is called, it created a new instance to handle the new request.

if __name__ == "__main__":
    main()

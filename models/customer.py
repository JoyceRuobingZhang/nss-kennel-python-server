

class Customer():
    
# ⭕️ when create some Customer instances to send back the client, sending the password in the response is a bad idea. 
# Also, there's no reason to send the email in the case since the client obviously already has the email address to reference.
    def __init__(self, id, name, address,  email = "", password = ""):
        self.id = id
        self.name = name
        self.address = address
        self.email = email
        self.password = password
        
        
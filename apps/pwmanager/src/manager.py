
import json, os, string, random
import sys
sys.path.append('../applications-of-aes') # path to aes

# local packages
from aes import AES
from apps.utils import load_encryption_settings

class Manager:
    def __init__(self, manager_path: str, encrypted_path: str) -> None:
        self.manager_path = manager_path # manager json path
        self.encrypted_path = encrypted_path # encrypted password path 

        self.key, self.cbc, self.iv = load_encryption_settings() # load encryption settings
        self.aes = AES(self.key) # aes object

    def load_manage_data(self) -> dict:
        """Loads the json data to instance of class."""
        return json.load(open(self.manager_path))
    
    def save_data(self, data: dict()) -> None:
        """Saves the json data to manager.json"""
        json_object = json.dumps({"manage": data}, indent=4)

        with open(self.manager_path, "w") as FILE:
            FILE.write(json_object)

    def add_data(self, location: str, username: str, password: str) -> None:
        """Creates the encrypted data and stores it in the manager."""
        encrypted_password = self.encrypt_data(password) # encrypted password data
        
        # writes encrypted data to the path 
        random_fname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))  # random name to encrypt location
        encrypted_path = self.encrypted_path + f"/{random_fname}.bin" # encrypted file path 
        
        # creates and writes to the file with the encrypted password
        with open(encrypted_path, "wb") as FILE:
            FILE.write(encrypted_password)

        # adds new data to the manager json
        updated_data = self.load_manage_data()["manage"] # grabs data
        data_scheme = {username: encrypted_path}

        if location in updated_data.keys():
            updated_data[location].append(data_scheme) # if the location has multiple logins 
        else:
            updated_data[location] = [data_scheme] # new location 

        self.save_data(updated_data) # save

    def remove_data(self, location: str) -> None:
        """Deletes the file and removes from manager."""
        data = self.load_manage_data()["manage"] # grabs data 

        if location not in data.keys():
            print("Location does not exist...") # location to remove does not exist
        else: # removes the files assocated with the location
            location_path = data[location]
            for info in location_path:
                for remove_location in info.values():
                    os.remove(remove_location)
            
            del data[location] # removes from location from manager json

            self.save_data(data) # save data

    def encrypt_data(self, data: str) -> bytes:
        """This takes a string and encrypts it based on blocks."""
        encrypted_data = self.aes.encrypt(data, self.cbc, self.iv)

        return encrypted_data # returns the encrypted byte variable
    
    def decrypt_data(self, data: bytes) -> str:
        """This takes a string and decrypts it based on blocks."""
        # NOTE: This method only works with single line bin files which is applicable...for file conversion a while loop must be used
        decrypted_data = self.aes.decrypt(data, self.cbc, self.iv)

        return decrypted_data # returns the decrypted string variable
    
    def display_locations(self) -> None:
        """Gets list of locations from manage.json"""
        data = list(self.load_manage_data()["manage"]) # gets a list of the locations

        if len(data) == 0:
            print(None) # prints none if manager is empty
        else:
            print(", ".join(data)) # prints location

    def display_data(self, detailed: bool) -> None:
        """Displays data from manager based."""
        data = self.load_manage_data()["manage"] # grabs manager json data 

        if not detailed: # simple format
            self.display_locations()
        else: # detailed format
            for location, information in data.items(): # location and info assocated with location
                # get the encrypted data
                print(f"\t__{location}__") 
                for index, info in enumerate(information): # each profile in location
                    for username, path in info.items(): # username and path holding the encrypted password
                        with open(path, "rb") as FILE:
                            password = self.decrypt_data(FILE.read()) # decrypts password                      

                        print(f"\tUsername ({index + 1}): {username}\n\tPassword ({index + 1}): {password}")


def main() -> None:
    # config
    manager_path = "apps/pwmanager/data/manage.json" # path to json manager
    encrypted_path = "apps/pwmanager/data/encrypted" # path to encrypted password folder

    manager = Manager(manager_path, encrypted_path) # manager object
    commands = "\n# 0: add data, 1: remove data, 2: view data, 3: exit" # string of commands for user

    print("### PASSWORD MANAGER ###")

    while True:
        try:
            # manages the user commands
            print(commands)
            user_input = int(input("> "))
            # add data to manager based on location, username, and password
            if user_input == 0:
                print("\n# Add data #")
                location = input("> (Location) ")
                username = input("> (Username) ")
                password = input("> (Password) ")
                manager.add_data(location, username, password)
            # removes data from manager based on a location
            elif user_input == 1:
                print("\n# Enter location to remove data #")
                manager.display_locations()
                location = input("> (Location) ")
                manager.remove_data(location)
            # display's the users location, username, and password dara 
            elif user_input == 2:
                print("\n# Displayed simple or detailed (S/D) #")
                config = input("> (S/D) ").upper()
                manager.display_data(config == "D")
            # exits the user from the programs
            elif user_input == 3:
                print("\n# Goodbye! #")
                break
            # invalid input
            else: print("\n# Must input 0, 1, 2, or 3...")
        except Exception as e:
            print(f"{e}\nPossible errors with en/decryption are differing use of Key/IV.")


if __name__ == "__main__":
    main() # main loop

import json, os, string, random
import sys
sys.path.append('../applications-of-aes') # path to aes

# local packages
from aes import AES
from apps.utils import load_encryption_key, load_chunks

class Manager:
    def __init__(self, manager_path: str, encrypted_path: str) -> None:
        self.manager_path = manager_path
        self.encrypted_path = encrypted_path
        self.aes = AES(load_encryption_key())

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
        # encrypted data
        encrypted_password = self.encrypt_data(password)
        
        # writes encrypted data to the path 
        random_fname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))  # random name to encrypt location
        encrypted_path = self.encrypted_path + f"/{random_fname}.bin" # encrypted path 
        
        with open(encrypted_path, "wb") as FILE:
            FILE.write(encrypted_password)

        updated_data = self.load_manage_data()["manage"]
        data_scheme = {username: encrypted_path}

        if location in updated_data.keys():
            updated_data[location].append(data_scheme)
        else:
            updated_data[location] = [data_scheme]

        self.save_data(updated_data)

    def remove_data(self, location: str) -> None:
        """Deletes the file and removes from manager."""
        data = self.load_manage_data()["manage"]

        if location not in data.keys():
            print("Location does not exist...")
        else: # removes file
            location_path = data[location]
            for info in location_path:
                for remove_location in info.values():
                    os.remove(remove_location)
            
            del data[location] # removes from location

            self.save_data(data) # save data

    def encrypt_data(self, data: str) -> bytes:
        """This takes a string and encrypts it based on blocks."""
        encrypt_data = bytes()

        data_blocks = load_chunks(data)
        for block in data_blocks:
            encrypt_data += self.aes.encrypt(block)

        return encrypt_data
    
    def decrypt_data(self, data: bytes) -> str:
        """This takes a string and decrypts it based on blocks."""
        decrypt_data = str()

        data_blocks = load_chunks(data)
        for block in data_blocks:
            decrypt_data += self.aes.decrypt(block)

        return decrypt_data
    
    def display_locations(self) -> None:
        """Gets list of locations from manage.json"""
        data = list(self.load_manage_data()["manage"])

        if len(data) == 0:
            print(None)
        else:
            print(", ".join(data))

    def display_data(self, detailed: bool) -> None:
        """Displays data from manager based."""
        data = self.load_manage_data()["manage"]

        if not detailed: # simple format
            self.display_locations()
        else: # detailed format
            for location, information in data.items():
                # get the encrypted data
                print(f"\t__{location}__") 
                for index, info in enumerate(information):
                    for username, path in info.items():
                        with open(path, "rb") as FILE:
                            password = self.decrypt_data(FILE.read())                            

                        print(f"\tUsername ({index + 1}): {username}\n\tPassword ({index + 1}): {password}")


def main() -> None:
    manager_path = "apps/password_manager/data/manage.json"
    encrypted_path = "apps/password_manager/data/encrypted"

    manager = Manager(manager_path, encrypted_path)
    commands = "\n# 0: add data, 1: remove data, 2: view data, 3: exit"

    print("### PASSWORD MANAGER ###")

    run = True
    while run:
        # try:
        print(commands)
        user_input = int(input("> "))
        
        if user_input == 0: # add data to manager
            print("\n# Add data #")
            location = input("> (Location) ")
            username = input("> (Username) ")
            password = input("> (Password) ")

            manager.add_data(location, username, password)

        elif user_input == 1: # removes data from manager
            print("\n# Enter location to remove data #")
            manager.display_locations()

            location = input("> Location: ")
            manager.remove_data(location)

        elif user_input == 2: # display data from manager
            print("\n# Displayed simple or detailed (S/D) #")
            config = input("> ").upper()

            manager.display_data(config == "D")

        elif user_input == 3: # exits 
            print("\n# Goodbye! #")
            run = False

        else: # invalid input
            print("\n# Must input 0, 1, 2, or 3...")
        # except Exception as e:
        #     print(e)


if __name__ == "__main__":
    main()
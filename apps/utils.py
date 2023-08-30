import json

def load_encryption_settings() -> tuple:
    """This method fetches the key written in config.json"""
    file = open("config.json")
    data = json.load(file)
    return (data['Key'], data['CBC'], data['IV'])
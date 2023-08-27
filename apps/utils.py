import json, time

def load_encryption_key() -> str:
    """This method fetches the key written in config.json"""
    file = open("config.json")
    return json.load(file)['Key']

def load_chunks(input) -> list:
    """Creates blocks of data in chunks of 16 characters of bytes."""
    chunks = []
    for index in range(0, len(input), 16):
        chunks.append(input[index: index + 16])
    return chunks
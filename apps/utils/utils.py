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

def record_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"* {func.__name__}:\t{execution_time:.6f} seconds")
        return result
    return wrapper
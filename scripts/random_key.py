import os
import base64

def main(password_length: int) -> None:
    """Creates a high quality password based on a given length."""
    assert password_length in [16, 24, 32]

    random_key = base64.b64encode(os.urandom(password_length)).decode("utf-8")
    print(f"Random Key: {random_key}")

if __name__ == "__main__":
    password_length = 16

    main()
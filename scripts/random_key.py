import argparse, base64, os

def main(password_length: int) -> None:
    """Creates a high quality password based on a given length."""

    random_key = base64.b64encode(os.urandom(password_length)).decode("utf-8")
    print(f"Random Key: {random_key}")

if __name__ == "__main__":
    """Run the file by copying into your terminal: python3 scripts/random_key.py --len {chose 16, 24, 32}"""
    # create the parser
    parser = argparse.ArgumentParser(description='Generate a random key.')
    # add arguments
    parser.add_argument("--len", type=int, help="key length (16, 24, 32)", required=False)
    # parse the arguments
    try:
        args = parser.parse_args()
    except:
        exit()
    # password length
    password_length = 16 if (args.len == None) else args.len
    assert password_length in [16, 24, 32]

    main(password_length)
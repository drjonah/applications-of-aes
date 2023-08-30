import argparse, random, string

def gen_iv(length):
    """Generates a random string for an IV."""
    # NOTE: This is not as "random" as the key generation

    char_list = list(string.ascii_letters + string.digits) # character set list

    # Creates result and adds until there are no repeats
    result = random.choice(char_list)

    while len(result) < length:
        next_char = random.choice(char_list) # gen random choice
        if next_char != result[-1]: result += next_char # adds if unique

    return result

def main(iv_length: int) -> None:
    """Creates a high IV based on a given length."""

    print(f"Random IV: {gen_iv(iv_length)}")

if __name__ == "__main__":
    """Run the file by copying into your terminal: python3 scripts/random_key.py --len {chose 16, 24, 32}"""
    # create the parser
    parser = argparse.ArgumentParser(description='Generate a random IV.')
    # add arguments
    parser.add_argument("--len", type=int, help="key length (16, 24, 32)", required=False)
    # parse the arguments
    try:
        args = parser.parse_args()
    except:
        exit()
    # password length
    iv_length = 16 if (args.len == None) else args.len
    assert iv_length in [16, 24, 32]

    main(iv_length) # main
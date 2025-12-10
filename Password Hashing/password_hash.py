import bcrypt


def encrypt(input_string):
    # converts into an array of bites
    byte_convert = input_string.encode('utf-8')

    # generates a salt
    salt = bcrypt.gensalt()

    # hashes the password
    full_hash = bcrypt.hashpw(byte_convert, salt)
    return full_hash


to_hash = input("Enter a string to hash: ")
hashed = encrypt(to_hash)
print(f"{to_hash} after being encrypted becomes {hashed}")

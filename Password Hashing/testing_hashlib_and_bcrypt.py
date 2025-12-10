import bcrypt
import hashlib


def string_hasher(input_string):
    '''Takes the input string, encodes it into utf-8 byte format, and
    applies SHA-256 hashing algorithm. THe result is then converted into
    a readable hexadecimal string using hexdigest() method, which can be
    used to securely store or compare sensative information'''
    hashed_string = hashlib.sha256(input_string.encode()).hexdigest()
    return hashed_string


hashed1 = string_hasher("This is sensative text")
hased2 = string_hasher("_pasword-123_")

print(f"\'_password-123_\' \t--> Hash Function --> \t {hashed1}")

####################################################################

password = 'password123'

# converts to array of bytes
bytes = password.encode('utf-8')

# generating a salt
salt = bcrypt.gensalt()

# hashing the password
hash = bcrypt.hashpw(bytes, salt)

print(hash)

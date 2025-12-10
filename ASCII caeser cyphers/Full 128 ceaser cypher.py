'''Creating a full ceasar cyper style encoding program'''


def caesar_full_ascii_cypher(text, shift=15):
    '''works as a full caeser cypher, by shifting all ASCII values 15
    ahead and using % 128 to keep it within the 128 characters of the ASCII
    set of symbols, letters and numbers'''

    # creates an empty string to add cyphered characters too
    result = ""
    # iterates through each character in the input string
    for ch in text:
        # converts the character to the ASCII number
        ascii_val = ord(ch)
        # moves the ASCII number forward 15 but loops at 128 due to the
        # limit of the ASCII numbers
        shifted = (ascii_val + shift) % 128
        # converts the ASCII number back to a character and adds to the
        # final string
        result += chr(shifted)

    return result


def caesar_full_ascii_decrypt(text, shift=15):
    '''This function decodes a caeser style encryption input using 128
    ASCII values and a 15 digit shift'''
    result = ""

    for ch in text:
        ascii_val = ord(ch)
        shifted = (ascii_val - shift) % 128
        result += chr(shifted)

    return result


text_to_encode = input("enter a string of letters and numbers: ")
encoded = caesar_full_ascii_cypher(text_to_encode)
print(encoded)
decoded = caesar_full_ascii_decrypt(encoded)
print(decoded)

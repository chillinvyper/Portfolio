'''Creating a partial ceasar cyper style encoding program'''


def caesar_cypher(input_string, shift=15):
    '''works as a ceaser cypher by moving each character 15 ahead in
    value'''
    # create an empty string to add changed characters too
    result = ""
    # iterates through each character in the string
    for character in input_string:
        ascii_val = ord(character)

        # handles uppercase letters, by seperating out these letters by
        # ASCII numbers
        if 65 <= ascii_val <= 90:
            shifted = ((ascii_val - 65 + shift) % 26) + 65
            result += chr(shifted)

        # handles lowercase letters, by seperating out these letters by
        # ASCII numbers
        elif 97 <= ascii_val <= 122:
            shifted = ((ascii_val - 97 + shift) % 26) + 97
            result += chr(shifted)

        # Numbers 0–9, by seperating out these numbers by
        # ASCII numbers
        elif 48 <= ascii_val <= 57:
            shifted = ((ascii_val - 48 + shift) % 10) + 48
            result += chr(shifted)

        # Other characters stay the same
        else:
            result += character

    return result


to_cyper = str(input("Enter some letter and numbers: "))
hidden_message = caesar_cypher(to_cyper)
print(hidden_message)
